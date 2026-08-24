"""
HPPCS[05] - Sports Commentator from Video

Project input:
    - train_video*.mp4 : training/reference sports videos with commentary
    - test_video.mp4   : test sports video without commentary

Project output:
    - JSON containing timeline-based generated commentary.

Two-LLM architecture:
    LLM #1 (vision model) -> visual/event understanding
    LLM #2 (text model)  -> sports commentary generation

The program automatically discovers train_video*.mp4 in the project directory.
The training videos are used to build a compact visual/event reference profile.
The optional training_commentary_example.txt is also used as a language/style
reference when present.

All files remain in one directory for capstone submission compatibility.
"""

import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import requests


# ---------------------------------------------------------------------------
# Command-line arguments
# ---------------------------------------------------------------------------

def parse_args():
    """Parse command-line arguments for the capstone application."""
    parser = argparse.ArgumentParser(
        description="HPPCS[05] Sports Commentator from Video"
    )

    parser.add_argument(
        "--test_video",
        default="./test_video.mp4",
        help="Testing video without commentary."
    )

    parser.add_argument(
        "--training_dir",
        default=".",
        help="Directory containing train_video*.mp4 reference videos."
    )

    parser.add_argument(
        "--training_pattern",
        default="train_video*.mp4",
        help="Filename pattern used to discover training/reference videos."
    )

    parser.add_argument(
        "--training_commentary",
        default="./training_commentary_example.txt",
        help="Optional text commentary/style reference."
    )

    parser.add_argument(
        "--output",
        default="./commentary_output.json",
        help="Output JSON file."
    )

    parser.add_argument(
        "--window",
        type=float,
        default=5.0,
        help="Test-video analysis window in seconds."
    )

    parser.add_argument(
        "--max_windows",
        type=int,
        default=0,
        help="Maximum test windows. 0 means all windows."
    )

    parser.add_argument(
        "--training_samples",
        type=int,
        default=3,
        help="Number of representative windows sampled from each training video."
    )

    parser.add_argument(
        "--fps_sample",
        type=int,
        default=1,
        help="Frames sampled per second from each analysis window."
    )

    # LLM #1 MUST be vision-capable because it receives images.
    parser.add_argument(
        "--llm1_url",
        default=os.getenv("LLM1_URL", "http://localhost:11434"),
        help="Ollama base URL for LLM #1, e.g. http://localhost:11434."
    )

    parser.add_argument(
        "--llm1_model",
        default=os.getenv("LLM1_MODEL", "gemma3:4b"),
        help="Vision-capable model for LLM #1."
    )

    # LLM #2 can be text-only and receives structured event data.
    parser.add_argument(
        "--llm2_url",
        default=os.getenv("LLM2_URL", "http://localhost:11434"),
        help="Ollama base URL for LLM #2, e.g. http://localhost:11434."
    )

    parser.add_argument(
        "--llm2_model",
        default=os.getenv("LLM2_MODEL", "llama3.2:3b"),
        help="Text model for LLM #2."
    )

    parser.add_argument(
        "--api_key",
        default=os.getenv("LLM_API_KEY", ""),
        help="Optional API key for an OpenAI-compatible hosted endpoint."
    )

    return parser.parse_args()


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS.mmm format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def safe_json(text: str) -> Optional[Dict]:
    """Extract a JSON object from a model response."""
    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    # Remove common Markdown JSON fences.
    text = re.sub(r"```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    try:
        return json.loads(text.strip())
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return None

    return None


def get_video_metadata(video_path: str) -> Dict:
    """Read basic metadata from a video file."""
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps else 0.0

    cap.release()

    return {
        "filename": Path(video_path).name,
        "fps": round(fps, 3),
        "frame_count": frame_count,
        "width": width,
        "height": height,
        "duration_seconds": round(duration, 3)
    }


def sample_frames(
    video_path: str,
    start: float,
    end: float,
    fps_sample: int = 1,
    max_frames: int = 6
) -> List[Tuple[float, object]]:
    """Sample representative frames from a time interval."""
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    frames = []
    step = 1.0 / max(1, fps_sample)
    current = start

    while current < end and len(frames) < max_frames:
        cap.set(cv2.CAP_PROP_POS_MSEC, current * 1000)
        ok, frame = cap.read()

        if ok:
            frames.append((current, frame))

        current += step

    cap.release()
    return frames


def frame_to_data_url(frame) -> str:
    """Convert an OpenCV frame into a JPEG data URL."""
    ok, encoded = cv2.imencode(
        ".jpg",
        frame,
        [int(cv2.IMWRITE_JPEG_QUALITY), 70]
    )

    if not ok:
        raise RuntimeError("Failed to encode video frame.")

    encoded_bytes = encoded.tobytes()
    base64_data = base64.b64encode(encoded_bytes).decode("utf-8")

    return "data:image/jpeg;base64," + base64_data


def build_visual_context(frames: List[Tuple[float, object]]) -> Dict:
    """Create image and basic motion information for an analysis window."""
    images = []
    motion_scores = []
    previous_gray = None

    for frame_time, frame in frames:
        images.append({
            "time": round(frame_time, 3),
            "image": frame_to_data_url(frame)
        })

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if previous_gray is not None:
            diff = cv2.absdiff(previous_gray, gray)
            motion_scores.append(float(diff.mean()))

        previous_gray = gray

    average_motion = (
        sum(motion_scores) / len(motion_scores)
        if motion_scores else 0.0
    )

    return {
        "sample_count": len(frames),
        "average_motion_score": round(average_motion, 3),
        "images": images
    }


def discover_training_videos(training_dir: str, pattern: str) -> List[str]:
    """Discover training/reference MP4 files such as train_video1.mp4."""
    directory = Path(training_dir)

    if not directory.exists():
        raise FileNotFoundError(
            f"Training directory does not exist: {training_dir}"
        )

    videos = sorted(
        str(path)
        for path in directory.glob(pattern)
        if path.is_file()
    )

    return videos


def read_commentary_reference(path: str) -> str:
    """Read the optional training commentary/style reference text."""
    file_path = Path(path)

    if not file_path.exists():
        return ""

    try:
        return file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        ).strip()[:6000]
    except OSError:
        return ""


def build_training_windows(
    video_path: str,
    sample_count: int
) -> List[Tuple[float, float]]:
    """Select evenly distributed representative windows from a training video."""
    metadata = get_video_metadata(video_path)
    duration = metadata["duration_seconds"]

    if duration <= 0:
        return []

    count = max(1, sample_count)
    window_size = min(5.0, max(1.0, duration / count))

    if count == 1:
        starts = [0.0]
    else:
        max_start = max(0.0, duration - window_size)
        starts = [
            max_start * i / (count - 1)
            for i in range(count)
        ]

    return [
        (round(start, 3), round(min(duration, start + window_size), 3))
        for start in starts
    ]


# ---------------------------------------------------------------------------
# LLM calls
# ---------------------------------------------------------------------------

def call_ollama_chat(
    url: str,
    model: str,
    prompt: str,
    api_key: str = "",
    images: Optional[List[str]] = None,
    timeout: int = 180
) -> str:
    """
    Call Ollama's native /api/chat endpoint.

    Ollama vision requests use a raw Base64 string in the message's
    "images" array, rather than OpenAI image_url/data-URL objects.
    """
    base_url = url.rstrip("/")

    if base_url.endswith("/api/chat"):
        endpoint = base_url
    elif base_url.endswith("/api"):
        endpoint = base_url + "/chat"
    else:
        endpoint = base_url + "/api/chat"

    message = {
        "role": "user",
        "content": prompt
    }

    if images:
        # frame_to_data_url() returns data:image/jpeg;base64,<payload>.
        # Ollama /api/chat wants only the Base64 payload.
        message["images"] = [
            image.split(",", 1)[1] if "," in image else image
            for image in images[:6]
        ]

    payload = {
        "model": model,
        "messages": [message],
        "stream": False,
        "options": {
            "temperature": 0.3
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = requests.post(
        endpoint,
        headers=headers,
        json=payload,
        timeout=timeout
    )
    response.raise_for_status()

    data = response.json()

    try:
        return data["message"]["content"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError(
            f"Unexpected Ollama response from {endpoint}: {data}"
        ) from exc


def call_openai_compatible(
    url: str,
    model: str,
    prompt: str,
    api_key: str = "",
    images: Optional[List[str]] = None,
    timeout: int = 180
) -> str:
    """
    Backward-compatible wrapper.

    The application now uses Ollama's native /api/chat endpoint.
    """
    return call_ollama_chat(
        url=url,
        model=model,
        prompt=prompt,
        api_key=api_key,
        images=images,
        timeout=timeout
    )


# ---------------------------------------------------------------------------
# Training/reference phase
# ---------------------------------------------------------------------------

def analyze_training_video(
    args,
    video_path: str,
    commentary_reference: str
) -> List[Dict]:
    """
    Analyze representative portions of one training video.

    The training videos are not fine-tuned. Instead, their visual/event
    characteristics are converted into a compact reference profile that is
    supplied to the test-video analysis and commentary prompts.
    """
    print(f"\n[TRAINING] Processing: {Path(video_path).name}")

    training_events = []

    for index, (start, end) in enumerate(
        build_training_windows(video_path, args.training_samples),
        start=1
    ):
        frames = sample_frames(
            video_path,
            start,
            end,
            fps_sample=args.fps_sample,
            max_frames=4
        )

        if not frames:
            continue

        visual = build_visual_context(frames)

        prompt = f"""
You are the visual event-analysis model in a sports commentary capstone.

This is a TRAINING/REFERENCE video segment.
Analyze only what is visibly supported by the frames.

Training video: {Path(video_path).name}
Time: {timestamp(start)} - {timestamp(end)}
Motion score: {visual["average_motion_score"]}

Optional human commentary reference:
{commentary_reference[:2500]}

Return ONLY valid JSON:
{{
  "sport": "football|cricket|kabaddi|other|unknown",
  "event": "observable event",
  "visual_cues": ["cue1", "cue2"],
  "commentary_style": "brief description",
  "confidence": 0.0
}}

Do not invent names, scores, statistics, or outcomes.
"""

        try:
            raw = call_openai_compatible(
                args.llm1_url,
                args.llm1_model,
                prompt,
                args.api_key,
                images=[x["image"] for x in visual["images"]]
            )

            result = safe_json(raw)

            if result:
                result["source_video"] = Path(video_path).name
                result["source_start"] = timestamp(start)
                result["source_end"] = timestamp(end)
                training_events.append(result)

        except Exception as exc:
            print(
                f"[WARN] Training analysis failed for "
                f"{Path(video_path).name} window {index}: {exc}"
            )

    return training_events


def build_training_profile(
    args,
    training_videos: List[str],
    commentary_reference: str
) -> Dict:
    """Build a compact reference profile from all training videos."""
    profile = []

    for video in training_videos:
        profile.extend(
            analyze_training_video(
                args,
                video,
                commentary_reference
            )
        )

    return {
        "training_video_count": len(training_videos),
        "training_videos": [
            Path(video).name for video in training_videos
        ],
        "reference_events": profile[:30],
        "commentary_reference_available": bool(commentary_reference)
    }


# ---------------------------------------------------------------------------
# Test-video analysis
# ---------------------------------------------------------------------------

def fallback_event(
    visual: Dict,
    start: float,
    end: float
) -> Dict:
    """Return a safe event when the vision model is unavailable."""
    motion = visual.get("average_motion_score", 0.0)

    if motion > 18:
        event = "High-motion sports action is visible."
    elif motion > 8:
        event = "Players or the ball are moving during active play."
    else:
        event = "A relatively stable sports sequence is visible."

    return {
        "sport": "unknown",
        "event": event,
        "players": [],
        "score": "",
        "game_context": "",
        "confidence": 0.35
    }


def llm1_analyze_test_window(
    args,
    visual: Dict,
    start: float,
    end: float,
    training_profile: Dict
) -> Dict:
    """
    LLM #1: analyze the test-video frames and identify the event.

    LLM #1 is intentionally a vision-capable model. The default is Gemma 3 4B.
    """
    prompt = f"""
You are LLM #1 in a two-LLM sports commentary system.

Analyze the TEST video segment using the supplied images.

Time window: {timestamp(start)} - {timestamp(end)}
Motion score: {visual["average_motion_score"]}

Reference information learned from training videos:
{json.dumps(training_profile, ensure_ascii=False)[:7000]}

Return ONLY valid JSON:
{{
  "sport": "football|cricket|kabaddi|other|unknown",
  "event": "specific observable event",
  "players": [],
  "score": "",
  "game_context": "",
  "visual_evidence": ["observable cue"],
  "confidence": 0.0
}}

Rules:
- Use the training videos only as reference/context.
- Base the actual event on the TEST video frames.
- Never invent player names, score, statistics, or outcomes.
- If something is uncertain, write "unknown" or leave it empty.
- Prefer events such as pass, shot, goal, tackle, raid, wicket, run,
  serve, rally, catch, foul, celebration, timeout, or restart when visibly supported.
"""

    try:
        raw = call_openai_compatible(
            args.llm1_url,
            args.llm1_model,
            prompt,
            args.api_key,
            images=[x["image"] for x in visual["images"]]
        )

        result = safe_json(raw)

        if result:
            return result

    except Exception as exc:
        print(f"[WARN] LLM #1 failed for {timestamp(start)}: {exc}")

    return fallback_event(visual, start, end)


def llm2_generate_commentary(
    args,
    event: Dict,
    start: float,
    end: float,
    training_profile: Dict,
    commentary_reference: str
) -> Dict:
    """
    LLM #2: generate final broadcast commentary from the structured event.
    """
    prompt = f"""
You are LLM #2, the final sports commentator.

Generate concise, natural sports commentary from the structured event
identified by LLM #1.

Segment: {timestamp(start)} - {timestamp(end)}

Detected event:
{json.dumps(event, ensure_ascii=False, indent=2)}

Training/reference event examples:
{json.dumps(training_profile.get("reference_events", [])[:8],
            ensure_ascii=False, indent=2)[:6000]}

Optional commentary style reference:
{commentary_reference[:2500]}

Return ONLY valid JSON:
{{
  "commentary": "one or two broadcast-style sentences",
  "tone": "excited|neutral|dramatic|informative",
  "confidence": 0.0
}}

Rules:
- Commentary must be grounded in the detected event.
- Never invent a player, team, score, statistic, or final result.
- Use excitement only through language, not unsupported facts.
- Keep it suitable for a sports broadcast.
"""

    try:
        raw = call_openai_compatible(
            args.llm2_url,
            args.llm2_model,
            prompt,
            args.api_key
        )

        result = safe_json(raw)

        if result and result.get("commentary"):
            return result

    except Exception as exc:
        print(f"[WARN] LLM #2 failed for {timestamp(start)}: {exc}")

    # Safe fallback.
    event_text = event.get("event", "The action continues.")
    return {
        "commentary": f"{event_text} The play continues through this sequence.",
        "tone": "informative",
        "confidence": 0.35
    }


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def build_test_windows(
    duration: float,
    window: float,
    max_windows: int
) -> List[Tuple[float, float]]:
    """Create sequential windows across the test video."""
    windows = []
    start = 0.0

    while start < duration:
        end = min(duration, start + window)
        windows.append((start, end))

        if max_windows and len(windows) >= max_windows:
            break

        start = end

    return windows


def run(args) -> Dict:
    """Run training/reference processing and test commentary generation."""
    test_video = Path(args.test_video)

    if not test_video.exists():
        raise FileNotFoundError(
            f"Test video not found: {test_video}"
        )

    # Automatically discover train_video1.mp4, train_video2.mp4, etc.
    training_videos = discover_training_videos(
        args.training_dir,
        args.training_pattern
    )

    if not training_videos:
        raise FileNotFoundError(
            "No training videos were found. Expected files such as "
            "train_video1.mp4, train_video2.mp4, train_video3.mp4."
        )

    if str(test_video.resolve()) in {
        str(Path(v).resolve()) for v in training_videos
    }:
        raise ValueError(
            "The test video must not also be treated as a training video."
        )

    commentary_reference = read_commentary_reference(
        args.training_commentary
    )

    print("\n===================================================")
    print("HPPCS[05] SPORTS COMMENTATOR FROM VIDEO")
    print("===================================================")
    print(f"Test video       : {test_video.name}")
    print(f"Training videos  : {len(training_videos)}")
    for video in training_videos:
        print(f"  - {Path(video).name}")
    print(f"LLM #1 (Vision)  : {args.llm1_model}")
    print(f"LLM #2 (Text)    : {args.llm2_model}")
    print("===================================================")

    # Phase 1: training/reference analysis.
    training_profile = build_training_profile(
        args,
        training_videos,
        commentary_reference
    )

    # Phase 2: test video.
    test_metadata = get_video_metadata(str(test_video))
    windows = build_test_windows(
        test_metadata["duration_seconds"],
        args.window,
        args.max_windows
    )

    timeline = []

    for index, (start, end) in enumerate(windows, start=1):
        print(
            f"\n[TEST {index}/{len(windows)}] "
            f"{timestamp(start)} -> {timestamp(end)}"
        )

        frames = sample_frames(
            str(test_video),
            start,
            end,
            fps_sample=args.fps_sample,
            max_frames=6
        )

        if not frames:
            print("[WARN] No frames found; skipping window.")
            continue

        visual = build_visual_context(frames)

        event = llm1_analyze_test_window(
            args,
            visual,
            start,
            end,
            training_profile
        )

        commentary = llm2_generate_commentary(
            args,
            event,
            start,
            end,
            training_profile,
            commentary_reference
        )

        timeline.append({
            "segment_id": index,
            "start_time": timestamp(start),
            "end_time": timestamp(end),
            "sport": event.get("sport", "unknown"),
            "event": event.get("event", "unknown"),
            "players": event.get("players", []),
            "score": event.get("score", ""),
            "game_context": event.get("game_context", ""),
            "visual_evidence": event.get("visual_evidence", []),
            "event_confidence": event.get("confidence", 0.0),
            "commentary": commentary.get("commentary", ""),
            "tone": commentary.get("tone", "informative"),
            "commentary_confidence": commentary.get("confidence", 0.0)
        })

    return {
        "project": "HPPCS[05] Sports Commentator from Video",
        "input": {
            "training_videos": [
                Path(video).name for video in training_videos
            ],
            "test_video": test_video.name,
            "test_video_metadata": test_metadata
        },
        "training_reference": training_profile,
        "models": {
            "llm_1": args.llm1_model,
            "llm_2": args.llm2_model,
            "roles": {
                "llm_1": "vision-based sports event understanding",
                "llm_2": "sports commentary generation"
            }
        },
        "timeline_commentary": timeline
    }


def main():
    """Required capstone entry point."""
    args = parse_args()

    try:
        result = run(args)

        output_path = Path(args.output)
        output_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        print("\n===================================================")
        print("COMPLETED")
        print(f"Output: {output_path.resolve()}")
        print(f"Timeline segments: {len(result['timeline_commentary'])}")
        print("===================================================")

    except Exception as exc:
        print(f"\n[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()