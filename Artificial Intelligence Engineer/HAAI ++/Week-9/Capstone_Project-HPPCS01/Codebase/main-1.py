"""HAAI++ HPPCS01 - CV Creation using LLMs.

Fine-tuned version:
- Gemma 3 is used for candidate-fact extraction and CV generation.
- Llama 3.2 is used as an independent CV reviewer.
- Candidate-specific CV content is never hard-coded.
- Source facts are preserved and obvious contact fields are verified deterministically.
- LLM output is constrained with JSON/plain-text instructions and bounded generation.
- Empty ACHIEVEMENTS/PROJECTS sections are omitted when the source has no content.
- Input resumes may be TXT, PDF, DOCX, DOC, RTF or MD.
- One controlled regeneration is performed only when the reviewer identifies a problem.
"""

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List

try:
    import requests
except ImportError:
    requests = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    Document = None


# ---------------------------------------------------------------------------
# Input document ingestion
# ---------------------------------------------------------------------------

# SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx", ".doc", ".rtf", ".md"}
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc"}


def extract_text_from_file(file_path: Path) -> str:
    """Read a supported resume format and normalize it to plain text."""
    ext = file_path.suffix.lower()

    if ext in {".txt", ".md"}:
        return file_path.read_text(encoding="utf-8", errors="replace")

    if ext == ".pdf":
        if PdfReader is None:
            raise RuntimeError("PDF support requires pypdf. Run: pip install pypdf")
        reader = PdfReader(str(file_path))
        pages = [(page.extract_text() or "").strip() for page in reader.pages]
        text = "\n\n".join(page for page in pages if page)
        if not text.strip():
            raise RuntimeError(
                f"No text could be extracted from {file_path.name}. "
                "The PDF may be scanned/image-only; OCR support is required for that file."
            )
        return text

    if ext == ".docx":
        if Document is None:
            raise RuntimeError("DOCX support requires python-docx. Run: pip install python-docx")
        doc = Document(str(file_path))
        parts = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]
                if any(cells):
                    parts.append(" | ".join(cells))
        return "\n".join(parts)

    if ext == ".rtf":
        raw = file_path.read_text(encoding="utf-8", errors="replace")
        raw = re.sub(r"\\'[0-9a-fA-F]{2}", " ", raw)
        raw = re.sub(r"\\[a-zA-Z]+-?\d* ?", " ", raw)
        raw = re.sub(r"[{}]", " ", raw)
        return re.sub(r"\s+", " ", raw).strip()

    if ext == ".doc":
        soffice = shutil.which("soffice") or shutil.which("libreoffice")
        if not soffice:
            raise RuntimeError(
                "DOC support requires LibreOffice (soffice) in PATH."
            )
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [soffice, "--headless", "--convert-to", "txt:Text", "--outdir", tmp, str(file_path)],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode != 0:
                raise RuntimeError(f"LibreOffice failed for {file_path.name}: {result.stderr.strip()}")
            candidates = list(Path(tmp).glob("*.txt"))
            if not candidates:
                raise RuntimeError(f"No text output produced for {file_path.name}")
            return candidates[0].read_text(encoding="utf-8", errors="replace")

    raise ValueError(f"Unsupported input format: {file_path.suffix}")


def discover_input_files(input_dir: Path) -> List[Path]:
    """Discover supported resume documents, including PDF, DOC, DOCX and TXT."""
    candidates = [
        p for p in input_dir.iterdir()
        if p.is_file()
        and p.suffix.lower() in SUPPORTED_EXTENSIONS
        and p.stem.lower().startswith("profile_")
    ]
    # If the same candidate exists in multiple formats (for example profile_01.txt
    # and profile_01.pdf), process only one. PDF/DOCX are preferred over TXT so a
    # real resume document is not silently ignored during a multi-format test.
    priority = {".pdf": 0, ".docx": 1, ".doc": 2, ".rtf": 3, ".txt": 4, ".md": 5}
    selected = {}
    for p in candidates:
        key = p.stem.lower()
        if key not in selected or priority[p.suffix.lower()] < priority[selected[key].suffix.lower()]:
            selected[key] = p
    return sorted(selected.values(), key=lambda p: p.name.lower())


# ---------------------------------------------------------------------------
# Ollama
# ---------------------------------------------------------------------------

def call_ollama(
    model: str,
    prompt: str,
    host: str,
    timeout: int = 180,
    json_mode: bool = False,
    num_predict: int = 400,
) -> str:
    """Call Ollama with bounded generation so one profile cannot hang indefinitely."""
    if requests is None:
        raise RuntimeError("Install requests first: pip install requests")

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "5m",
        "options": {
            "temperature": 0.1,
            "top_p": 0.9,
            "num_predict": num_predict,
        },
    }

    # Ollama supports JSON-constrained output with format=json.
    if json_mode:
        payload["format"] = "json"

    response = requests.post(
        f"{host.rstrip('/')}/api/generate",
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()

    result = response.json()
    text = result.get("response", "")
    if not text.strip():
        raise ValueError(f"Ollama returned an empty response for model {model}.")
    return text.strip()


def extract_json(text: str) -> Dict[str, Any]:
    """Parse JSON even when a small model accidentally adds a markdown fence."""
    text = text.strip()

    try:
        value = json.loads(text)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass

    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text).strip()

    try:
        value = json.loads(text)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        value = json.loads(text[start:end + 1])
        if isinstance(value, dict):
            return value

    raise ValueError("Model did not return a valid JSON object.")


# ---------------------------------------------------------------------------
# Source-grounding helpers
# ---------------------------------------------------------------------------

def first_email(raw: str) -> str:
    match = re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", raw)
    return match.group(0) if match else ""


def first_phone(raw: str) -> str:
    # Handles examples such as 555-1234 and +91-90000-10002.
    matches = re.findall(r"(?<!\w)(?:\+?\d[\d\s().-]{6,}\d)(?!\w)", raw)
    return matches[0].strip() if matches else ""


def extract_name_from_source(raw: str) -> str:
    # Labeled profiles: "Name: Priya Menon"
    match = re.search(r"(?im)^\s*name\s*:\s*([^\n,]+)", raw)
    if match:
        return match.group(1).strip()

    # Free-form profile: "John Doe, phone ..."
    match = re.match(
        r"\s*([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z.'-]+){1,3})\s*,",
        raw,
    )
    return match.group(1).strip() if match else ""


def extract_location_from_source(raw: str) -> str:
    # Labeled contact field.
    match = re.search(r"(?im)^\s*contact\s*:\s*.*,\s*([^,\n]+)\s*$", raw)
    if match:
        return match.group(1).strip()

    # Explicit location/city labels.
    match = re.search(r"(?im)^\s*(?:location|city)\s*:\s*([^\n]+)", raw)
    return match.group(1).strip() if match else ""


def clean_string(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def clean_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []
    result = []
    for item in value:
        text = clean_string(item)
        if text and text not in result:
            result.append(text)
    return result


def normalize_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize model JSON into the schema used by the rest of the pipeline."""
    contact = profile.get("contact")
    if not isinstance(contact, dict):
        contact = {}

    normalized = {
        "name": clean_string(profile.get("name")),
        "contact": {
            "email": clean_string(contact.get("email")),
            "phone": clean_string(contact.get("phone")),
            "location": clean_string(contact.get("location")),
        },
        "summary": clean_string(profile.get("summary")),
        "education": clean_list(profile.get("education")),
        "experience": clean_list(profile.get("experience")),
        "skills": clean_list(profile.get("skills")),
        "achievements": clean_list(profile.get("achievements")),
        "projects": clean_list(profile.get("projects")),
    }
    return normalized


def merge_obvious_source_facts(profile: Dict[str, Any], raw: str) -> Dict[str, Any]:
    """Protect obvious source facts from a weak extraction model."""
    profile = normalize_profile(profile)

    source_name = extract_name_from_source(raw)
    source_email = first_email(raw)
    source_phone = first_phone(raw)
    source_location = extract_location_from_source(raw)

    if source_name:
        profile["name"] = source_name
    if source_email:
        profile["contact"]["email"] = source_email
    if source_phone:
        profile["contact"]["phone"] = source_phone
    if source_location:
        profile["contact"]["location"] = source_location

    return profile


def fallback_extract(raw: str) -> Dict[str, Any]:
    """Safe fallback when Gemma is unavailable or times out."""
    lines = [x.strip() for x in raw.splitlines() if x.strip()]

    name = extract_name_from_source(raw) or "Candidate"
    email = first_email(raw)
    phone = first_phone(raw)
    location = extract_location_from_source(raw)

    summary = ""
    for line in lines:
        if re.match(r"(?i)^(profile|summary|professional background)\s*:", line):
            summary = line.split(":", 1)[1].strip()
            break

    skills = []
    for line in lines:
        if re.match(r"(?i)^skills\s*:", line):
            skills = [x.strip() for x in line.split(":", 1)[1].split(",")]
            break

    education = []
    achievements = []
    projects = []

    for line in lines:
        low = line.lower()
        if low.startswith("education:"):
            education.append(line.split(":", 1)[1].strip())
        elif low.startswith("achievements:"):
            achievements.append(line.split(":", 1)[1].strip())
        elif low.startswith("projects:"):
            projects.append(line.split(":", 1)[1].strip())

    # Keep complete experience sentences as source evidence in fallback mode.
    experience = []
    for line in lines:
        low = line.lower()
        if any(
            marker in low
            for marker in (
                "worked at ",
                "current employer:",
                "previous:",
                "experience:",
            )
        ):
            experience.append(line)

    return normalize_profile(
        {
            "name": name,
            "contact": {
                "email": email,
                "phone": phone,
                "location": location,
            },
            "summary": summary,
            "education": education,
            "experience": experience,
            "skills": skills,
            "achievements": achievements,
            "projects": projects,
        }
    )


# ---------------------------------------------------------------------------
# Gemma: extraction
# ---------------------------------------------------------------------------

def extract_profile(
    raw: str,
    model: str,
    host: str,
    timeout: int,
) -> Dict[str, Any]:
    """Use Gemma to structure facts without inventing or improving them."""
    prompt = f"""You are a strict information extraction system.

Extract ONLY information explicitly present in SOURCE PROFILE.
Do not infer, improve, paraphrase, or invent facts.

Return JSON only:
{{
  "name": "",
  "contact": {{"email": "", "phone": "", "location": ""}},
  "summary": "",
  "education": [],
  "experience": [],
  "skills": [],
  "achievements": [],
  "projects": []
}}

Rules:
- Copy names, employers, dates, skills, education, achievements and projects from the source.
- If a field is not present, use "" or [].
- Keep experience as source-supported statements.
- Do NOT create job titles that are not stated.
- Do NOT create metrics or accomplishments.
- Do NOT add technologies, degrees or responsibilities that are absent.
- Return JSON only. No markdown.

SOURCE PROFILE:
{raw}
"""

    try:
        result = call_ollama(
            model,
            prompt,
            host,
            timeout=timeout,
            json_mode=True,
            num_predict=300,
        )
        profile = extract_json(result)
        return merge_obvious_source_facts(profile, raw)
    except Exception as exc:
        print(f"[WARN] Extraction fallback: {exc}")
        return fallback_extract(raw)


# ---------------------------------------------------------------------------
# Gemma: CV generation
# ---------------------------------------------------------------------------

def generation_prompt(
    profile: Dict[str, Any],
    raw: str,
    regeneration_reason: str = "",
) -> str:
    reason = ""
    if regeneration_reason:
        reason = f"""
A previous draft failed review for these reasons:
{regeneration_reason}

Correct those issues while keeping every statement source-grounded.
"""

    return f"""You are a professional resume writer.

Create an ATS-friendly resume from the candidate source below.

CRITICAL GROUNDING RULE:
Every factual claim in the resume MUST be supported by SOURCE PROFILE.
You may professionally rewrite wording, but you must not add facts.

Allowed:
- "talked to clients" -> "Client communication"
- "cash register work" -> "Cash register operations"
- "updated the old computer system" -> "Updated the computer system"

Not allowed:
- "sold products" -> "exceeded sales targets"
- "talked to clients" -> "built long-term client relationships"
- "worked in sales" -> "prospected and closed deals"
unless the source explicitly says so.

Rules:
1. Do not invent employers, job titles, dates, achievements, metrics, degrees,
   certifications, technologies or responsibilities.
2. Do not add placeholders such as [Location], [Specify], "N/A", or examples.
3. Do not add "Achievements" if the source has no achievements.
4. Do not add "Projects" if the source has no projects.
5. Do not add interests unless they are explicitly present in the source.
6. Preserve all available contact information.
7. Keep the resume concise and professional.
8. Use these headings only when they contain data:
   PROFESSIONAL SUMMARY
   SKILLS
   PROFESSIONAL EXPERIENCE
   EDUCATION
   ACHIEVEMENTS
   PROJECTS
   INTERESTS
9. Return plain text only.
10. Do not use Markdown **, tables, code fences, or commentary.

STRUCTURED FACTS:
{json.dumps(profile, indent=2)}

SOURCE PROFILE:
{raw}
{reason}
"""


def generate_cv(
    profile: Dict[str, Any],
    raw: str,
    model: str,
    host: str,
    timeout: int,
    regeneration_reason: str = "",
) -> str:
    """Generate a grounded CV with bounded output."""
    prompt = generation_prompt(profile, raw, regeneration_reason)

    try:
        cv = call_ollama(
            model,
            prompt,
            host,
            timeout=timeout,
            json_mode=False,
            num_predict=650,
        )
        return clean_cv_text(cv)
    except Exception as exc:
        print(f"[WARN] Generation fallback: {exc}")
        return deterministic_cv(profile)


def clean_cv_text(text: str) -> str:
    """Remove model wrappers/placeholders without changing candidate facts."""
    text = text.strip()
    text = re.sub(r"^```(?:text|markdown)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text).strip()

    # Remove common model chatter.
    text = re.sub(
        r"^(here(?:'s| is) (?:a|the) .*?(?:resume|cv).*?:)\s*",
        "",
        text,
        flags=re.I | re.S,
    )

    # Remove Markdown emphasis around headings/bullets.
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"(?m)^\s*[-*]\s*", "• ", text)

    # Remove obvious placeholder lines.
    lines = []
    placeholder_patterns = (
        r"\[.*(?:specify|location|include|add|available).*?\]",
        r"^\s*n/?a\s*$",
        r"^\s*none\s*$",
    )
    for line in text.splitlines():
        if any(re.search(p, line, flags=re.I) for p in placeholder_patterns):
            continue
        lines.append(line.rstrip())

    return "\n".join(lines).strip()


# ---------------------------------------------------------------------------
# Deterministic fallback
# ---------------------------------------------------------------------------

def deterministic_cv(profile: Dict[str, Any]) -> str:
    """Fallback CV using only already-extracted candidate facts."""
    c = profile.get("contact", {})

    lines = [
        profile.get("name") or "Candidate",
        " | ".join(
            x
            for x in (
                c.get("email", ""),
                c.get("phone", ""),
                c.get("location", ""),
            )
            if x
        ),
    ]

    if profile.get("summary"):
        lines += ["", "PROFESSIONAL SUMMARY", profile["summary"]]

    if profile.get("skills"):
        lines += ["", "SKILLS"]
        lines += [f"• {x}" for x in profile["skills"]]

    if profile.get("experience"):
        lines += ["", "PROFESSIONAL EXPERIENCE"]
        lines += [f"• {x}" for x in profile["experience"]]

    if profile.get("education"):
        lines += ["", "EDUCATION"]
        lines += [f"• {x}" for x in profile["education"]]

    if profile.get("achievements"):
        lines += ["", "ACHIEVEMENTS"]
        lines += [f"• {x}" for x in profile["achievements"]]

    if profile.get("projects"):
        lines += ["", "PROJECTS"]
        lines += [f"• {x}" for x in profile["projects"]]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Independent Llama review
# ---------------------------------------------------------------------------

def review_cv(
    cv: str,
    profile: Dict[str, Any],
    raw: str,
    model: str,
    host: str,
    timeout: int,
) -> Dict[str, Any]:
    """Use Llama for independent review."""
    prompt = f"""You are an independent resume quality reviewer.

Compare the generated CV against the SOURCE PROFILE.

Return JSON only:
{{
  "score": 0,
  "keyword_coverage": 0,
  "factual_consistency": 0,
  "format_score": 0,
  "missing_keywords": [],
  "issues": [],
  "recommendation": "PASS or REGENERATE"
}}

Scoring:
- keyword_coverage: how much important source information appears in the CV.
- factual_consistency: whether every factual claim is supported by the source.
- format_score: readability and ATS structure.
- score: overall score.

Important:
- Missing phone, email, employer, date, education, skill, achievement or project
  that exists in SOURCE PROFILE is an issue.
- Unsupported achievements, metrics, responsibilities, job titles or skills are
  an issue.
- Empty sections or placeholders are an issue.
- Do not give credit for information that is not in the source.
- If factual consistency is below 90 OR important source information is missing,
  recommendation must be REGENERATE.
- A score of 0 cannot be PASS.
- Return JSON only.

SOURCE PROFILE:
{raw}

STRUCTURED FACTS:
{json.dumps(profile, indent=2)}

GENERATED CV:
{cv}
"""

    try:
        result = extract_json(
            call_ollama(
                model,
                prompt,
                host,
                timeout=timeout,
                json_mode=True,
                num_predict=300,
            )
        )
        return normalize_review(result)
    except Exception as exc:
        print(f"[WARN] Reviewer fallback: {exc}")
        return deterministic_review(cv, profile, raw, str(exc))


def normalize_review(review: Dict[str, Any]) -> Dict[str, Any]:
    """Make reviewer output safe and ensure PASS cannot have score 0."""
    def score(key: str, default: int = 0) -> int:
        try:
            value = int(float(review.get(key, default)))
        except (TypeError, ValueError):
            value = default
        return max(0, min(100, value))

    result = {
        "score": score("score"),
        "keyword_coverage": score("keyword_coverage"),
        "factual_consistency": score("factual_consistency"),
        "format_score": score("format_score"),
        "missing_keywords": clean_list(review.get("missing_keywords")),
        "issues": clean_list(review.get("issues")),
        "recommendation": clean_string(review.get("recommendation")).upper(),
    }

    if result["recommendation"] not in {"PASS", "REGENERATE"}:
        result["recommendation"] = (
            "PASS"
            if result["score"] >= 90 and result["factual_consistency"] >= 90
            else "REGENERATE"
        )

    if result["score"] <= 0 or result["factual_consistency"] < 90:
        result["recommendation"] = "REGENERATE"

    return result


def deterministic_review(
    cv: str,
    profile: Dict[str, Any],
    raw: str,
    error_message: str,
) -> Dict[str, Any]:
    """Safety-net review when Llama cannot be reached."""
    low = cv.lower()
    missing = []

    important_values = [
        profile.get("name", ""),
        profile.get("contact", {}).get("email", ""),
        profile.get("contact", {}).get("phone", ""),
        profile.get("contact", {}).get("location", ""),
    ]

    for value in important_values:
        if value and value.lower() not in low:
            missing.append(value)

    for skill in profile.get("skills", []):
        if skill and skill.lower() not in low:
            missing.append(skill)

    coverage_items = [x for x in important_values + profile.get("skills", []) if x]
    coverage = round(
        100 * (len(coverage_items) - len(set(missing))) / max(1, len(coverage_items))
    )

    # Reviewer fallback must be conservative.
    score = min(coverage, 80)

    return {
        "score": score,
        "keyword_coverage": coverage,
        "factual_consistency": 0,
        "format_score": 80,
        "missing_keywords": sorted(set(missing)),
        "issues": [f"Independent reviewer unavailable: {error_message}"],
        "recommendation": "REGENERATE",
    }


# ---------------------------------------------------------------------------
# Simple source-coverage guard
# ---------------------------------------------------------------------------

def source_coverage_check(cv: str, profile: Dict[str, Any]) -> List[str]:
    """Deterministically check critical source facts before accepting a CV."""
    low = cv.lower()
    missing = []

    contact = profile.get("contact", {})

    for label, value in (
        ("name", profile.get("name", "")),
        ("email", contact.get("email", "")),
        ("phone", contact.get("phone", "")),
        ("location", contact.get("location", "")),
    ):
        if value and value.lower() not in low:
            missing.append(f"Missing {label}: {value}")

    for item in profile.get("education", []):
        # Check only distinctive source text; LLM may professionally rephrase.
        tokens = [t for t in re.findall(r"[A-Za-z0-9]+", item.lower()) if len(t) >= 5]
        if tokens and not any(token in low for token in tokens):
            missing.append(f"Education may be missing: {item}")

    for item in profile.get("achievements", []):
        tokens = [t for t in re.findall(r"[A-Za-z0-9]+", item.lower()) if len(t) >= 6]
        if tokens and not any(token in low for token in tokens):
            missing.append(f"Achievement may be missing: {item}")

    for item in profile.get("projects", []):
        tokens = [t for t in re.findall(r"[A-Za-z0-9]+", item.lower()) if len(t) >= 6]
        if tokens and not any(token in low for token in tokens):
            missing.append(f"Project may be missing: {item}")

    return missing


# ---------------------------------------------------------------------------
# DOCX
# ---------------------------------------------------------------------------

SECTION_NAMES = {
    "SUMMARY": "PROFESSIONAL SUMMARY",
    "PROFESSIONAL SUMMARY": "PROFESSIONAL SUMMARY",
    "SKILLS": "SKILLS",
    "EXPERIENCE": "PROFESSIONAL EXPERIENCE",
    "PROFESSIONAL EXPERIENCE": "PROFESSIONAL EXPERIENCE",
    "EDUCATION": "EDUCATION",
    "ACHIEVEMENTS": "ACHIEVEMENTS",
    "PROJECTS": "PROJECTS",
    "INTERESTS": "INTERESTS",
}


def save_docx(text: str, path: Path) -> None:
    """Create a clean ATS-friendly DOCX from the generated plain text."""
    if Document is None:
        raise RuntimeError("Install python-docx first: pip install python-docx")

    doc = Document()
    section = doc.sections[0]
    section.top_margin = section.bottom_margin = Pt(45)
    section.left_margin = section.right_margin = Pt(50)

    lines = [x.strip() for x in text.splitlines()]

    for index, line in enumerate(lines):
        if not line:
            continue

        normalized = re.sub(r"^[•*-]\s*", "", line).strip()
        key = normalized.upper().rstrip(":")

        if index == 0:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(normalized)
            r.bold = True
            r.font.name = "Arial"
            r.font.size = Pt(18)
            continue

        if key in SECTION_NAMES:
            p = doc.add_paragraph()
            r = p.add_run(SECTION_NAMES[key])
            r.bold = True
            r.font.name = "Arial"
            r.font.size = Pt(11.5)
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            continue

        p = doc.add_paragraph()
        if line.startswith("•") or re.match(r"^[*-]\s+", line):
            p.style = doc.styles["List Bullet"]
            content = re.sub(r"^[•*-]\s*", "", line)
        else:
            content = normalized

        r = p.add_run(content)
        r.font.name = "Arial"
        r.font.size = Pt(10.5)

    doc.save(path)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def process_profile(
    file_path: Path,
    output_dir: Path,
    args: argparse.Namespace,
) -> Dict[str, Any]:
    print(f"\n[INFO] Processing {file_path.name}")

    raw = extract_text_from_file(file_path)

    print("[1/4] Extracting source facts with Gemma...")
    profile = extract_profile(
        raw,
        args.gemma_model,
        args.ollama_host,
        args.timeout,
    )

    print("[2/4] Generating ATS-friendly CV with Gemma...")
    cv = generate_cv(
        profile,
        raw,
        args.gemma_model,
        args.ollama_host,
        args.timeout,
    )

    print("[3/4] Reviewing CV independently with Llama...")
    review = review_cv(
        cv,
        profile,
        raw,
        args.llama_model,
        args.ollama_host,
        args.timeout,
    )

    coverage_issues = source_coverage_check(cv, profile)
    if coverage_issues:
        review.setdefault("issues", [])
        review["issues"].extend(coverage_issues)
        review["recommendation"] = "REGENERATE"

    # One and only one controlled regeneration.
    if review.get("recommendation") == "REGENERATE":
        reasons = "\n".join(
            review.get("issues", [])[:8]
            + review.get("missing_keywords", [])[:8]
        )

        print("[4/4] Review requested regeneration; retrying Gemma once...")
        regenerated = generate_cv(
            profile,
            raw,
            args.gemma_model,
            args.ollama_host,
            args.timeout,
            regeneration_reason=reasons,
        )

        # Keep the regeneration only if it is non-empty and different.
        if regenerated.strip():
            cv = regenerated

        print("[INFO] Running final Llama review...")
        review = review_cv(
            cv,
            profile,
            raw,
            args.llama_model,
            args.ollama_host,
            args.timeout,
        )

        coverage_issues = source_coverage_check(cv, profile)
        if coverage_issues:
            review.setdefault("issues", [])
            review["issues"].extend(coverage_issues)
            review["recommendation"] = "REGENERATE"

    stem = file_path.stem

    (output_dir / f"{stem}_structured.json").write_text(
        json.dumps(profile, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    (output_dir / f"{stem}_review.json").write_text(
        json.dumps(review, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    save_docx(cv, output_dir / f"{stem}_final_cv.docx")

    print(
        f"[RESULT] {file_path.name}: "
        f"status={review.get('recommendation')}, "
        f"score={review.get('score', 0)}"
    )

    return {
        "input": file_path.name,
        "output_cv": f"{stem}_final_cv.docx",
        "score": review.get("score", 0),
        "keyword_coverage": review.get("keyword_coverage", 0),
        "factual_consistency": review.get("factual_consistency", 0),
        "format_score": review.get("format_score", 0),
        "status": review.get("recommendation", "REGENERATE"),
        "issues": review.get("issues", []),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="HPPCS01 - CV Creation using two local LLMs"
    )
    parser.add_argument("--input-dir", default=".")
    parser.add_argument("--output-dir", default=".")
    # Keep 1B as the default because this is the currently reverted working setup.
    # Use --gemma-model gemma3:4b when you intentionally want the 4B model.
    parser.add_argument("--gemma-model", default="gemma3:1b")
    parser.add_argument("--llama-model", default="llama3.2:1b")
    parser.add_argument("--ollama-host", default="http://localhost:11434")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = discover_input_files(input_dir)[: args.limit]
    if not files:
        raise SystemExit("No supported resume files found. Supported: TXT, PDF, DOC, DOCX, RTF, MD.")

    print("=" * 70)
    print("HPPCS[01] - CV Creation using LLMs")
    print("=" * 70)
    print(f"Input directory : {input_dir.resolve()}")
    print(f"Output directory: {output_dir.resolve()}")
    print(f"Gemma model     : {args.gemma_model}")
    print(f"Review model    : {args.llama_model}")
    print(f"Timeout         : {args.timeout}s")
    print(f"Supported input : {", ".join(sorted(SUPPORTED_EXTENSIONS))}")
    print(f"Files discovered : {len(files)}")

    results = []

    for file_path in files:
        try:
            results.append(process_profile(file_path, output_dir, args))
        except Exception as exc:
            print(f"[ERROR] Failed to process {file_path.name}: {exc}")
            results.append(
                {
                    "input": file_path.name,
                    "output_cv": "",
                    "score": 0,
                    "keyword_coverage": 0,
                    "factual_consistency": 0,
                    "format_score": 0,
                    "status": "ERROR",
                    "issues": [str(exc)],
                }
            )

    summary = {
        "project": "CV Creation using LLMs",
        "models": {
            "generation": args.gemma_model,
            "review": args.llama_model,
        },
        "profiles_processed": len(results),
        "results": results,
    }

    (output_dir / "evaluation_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n" + "=" * 70)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("=" * 70)


if __name__ == "__main__":
    main()