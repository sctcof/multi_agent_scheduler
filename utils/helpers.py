# utils/helpers.py
import json

def load_json(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: dict, filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)