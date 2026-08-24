# CV Creation using LLMs - HPPCS01

## Overview
This capstone project converts unstructured candidate profiles into polished, ATS-friendly CVs using two local open-source LLMs through Ollama.

- `Gemma 3 1B` handles profile extraction and CV generation.
- `Llama 3.2 1B` performs independent resume review.
- Optional job-description support is available for keyword alignment and tailoring.

## Features
- Batch processing of `profile_*` files.
- Supports `TXT`, `MD`, `PDF`, `DOCX`, `DOC`, and `RTF` inputs.
- Extracts structured candidate facts into JSON.
- Generates final CV text and DOCX outputs.
- Produces reviewer feedback and an overall evaluation summary.
- Optionally generates PDF when LibreOffice is installed.
- Prevents unsupported claims with deterministic validation plus LLM review.

## Expected Outputs
For each profile, the pipeline generates:

- `profile_xx_source_text.txt`
- `profile_xx_structured.json`
- `profile_xx_final_cv.txt`
- `profile_xx_final_cv.docx`
- `profile_xx_review.json`
- `profile_xx_ats_analysis.json` when a job description is supplied

It also generates:

- `evaluation_summary.json`
- `job_description.json` when a job description is supplied

## Installation
```bash
python -m pip install -r requirements.txt
ollama pull gemma3:1b
ollama pull llama3.2:1b
ollama serve
```

## Usage

### Default capstone run
Processes up to 10 `profile_*` files from the current directory and writes outputs back to the same directory.

```bash
python main.py --gemma-model gemma3:1b --llama-model llama3.2:1b
```

### Write outputs to a separate folder
```bash
python main.py --input-dir . --output-dir output --gemma-model gemma3:1b --llama-model llama3.2:1b
```

### Run with a target job description
```bash
python main.py --jd-file job_description.txt --output-dir output
```

## Notes
- `DOC` to text conversion and optional PDF export require LibreOffice or `soffice` in `PATH`.
- If both `PDF` and `TXT` exist for the same profile, the pipeline prefers the richer document format.
- The script is backward-compatible with `--review-model`, but `--llama-model` is the preferred argument.
