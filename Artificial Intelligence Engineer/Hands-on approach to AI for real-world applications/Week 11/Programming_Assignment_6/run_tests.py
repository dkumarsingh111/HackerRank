import json
import subprocess

with open("test_cases.json") as f:
    data = json.load(f)

for i, case in enumerate(data["test_cases"], 1):
    sentence = case["input"].strip()
    print(f"\nTest Case {i}")
    subprocess.run(
        ["python", "template_code.py"] + sentence.split(),
        shell=True
    )
    print("Expected:", case["output"])