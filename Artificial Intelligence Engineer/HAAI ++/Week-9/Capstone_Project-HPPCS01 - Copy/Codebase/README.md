# CV Creation using LLMs - HPPCS01

## Objective
Convert 10 unstructured candidate profiles into ATS-friendly CVs using two local open-source LLMs.

## Two-LLM design
- Gemma 3 1B via Ollama: extraction and CV generation.
- Llama 3.2 1B via Ollama: independent ATS/relevance/factual review.

## Pipeline
Unstructured profile -> Gemma extraction -> structured JSON -> Gemma generation -> Llama review -> DOCX CV + evaluation JSON.

## Required run
Install dependencies, install the two Ollama models, start Ollama, then execute `python main.py`.

## Submission structure
This directory contains only the required flat Codebase and Report directories at the package level. All executable/data files inside Codebase are in one directory; no Codebase subdirectories are used.
