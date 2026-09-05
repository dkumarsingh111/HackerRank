# HPPCS[05] Sports Commentator from Video

## Project files
- main.py
- execution.txt
- requirements.txt
- README.md
- sample_output.json
- training_commentary_example.txt
- train_video1.mp4
- train_video2.mp4
- train_video3.mp4
- test_video.mp4

## Pipeline
The program automatically discovers `train_video*.mp4` in the current directory.
These are processed as training/reference videos. Representative windows are
analyzed by LLM #1 to create a compact visual/event reference profile.

`test_video.mp4` is then split into time windows. LLM #1 analyzes the test
frames, and LLM #2 converts the structured event into broadcast-style
commentary. The result is written to `commentary_output.json`.

## Two LLMs
- LLM #1: `gemma3:4b` — vision/event understanding.
- LLM #2: `llama3.2:3b` — text-based commentary generation.

## Setup
```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install the local Ollama models:
```cmd
ollama pull gemma3:4b
ollama pull llama3.2:3b
```

## Run
```cmd
python main.py --test_video ./test_video.mp4 --training_dir . --training_pattern "train_video*.mp4" --training_commentary ./training_commentary_example.txt --output ./commentary_output.json --window 5 --training_samples 3 --fps_sample 1 --llm1_url http://localhost:11434/v1 --llm1_model gemma3:4b --llm2_url http://localhost:11434/v1 --llm2_model llama3.2:3b
```

The training videos are used as reference examples; this is an inference-based
two-LLM pipeline, not model fine-tuning.
