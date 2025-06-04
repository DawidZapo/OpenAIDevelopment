import json
import os.path

from utils.utils import openai_client


def load_lines(filepath):
    with open(filepath, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def create_jsonl_for_fine_tune_if_not_exists():

    if os.path.exists('./fine_tune_util.py'):
        return

    correct_lines = load_lines("../text_files/fine_tune/correct.txt")
    incorrect_lines = load_lines("../text_files/fine_tune/incorect.txt")

    with open("fine_tune_data.jsonl", "w", encoding="utf-8") as f_out:
        for line in correct_lines:
            json.dump({
                "messages": [
                    {"role": "user", "content": line},
                    {"role": "assistant", "content": "1"}
                ]
            }, f_out, ensure_ascii=False)
            f_out.write("\n")

        for line in incorrect_lines:
            json.dump({
                "messages": [
                    {"role": "user", "content": line},
                    {"role": "assistant", "content": "0"}
                ]
            }, f_out, ensure_ascii=False)
            f_out.write("\n")

def fine_tune():

    file = openai_client.files.create(
        file=open('./fine_tune_data.jsonl', 'rb'),
        purpose='fine-tune'
    )

    job = openai_client.fine_tuning.jobs.create(
        training_file=file.id,
        model="gpt-4o-mini-2024-07-18",
        suffix="MINE_FINE_TUNE"
    )