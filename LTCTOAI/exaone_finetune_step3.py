from datasets import load_dataset

# 1. 데이터셋 로딩 (jsonl, messages 포맷)
dataset = load_dataset("json", data_files="c:/Working/LTCTOAI/LTCTOAI/2026_daycare_eval.jsonl")
print("[1] 원본 데이터셋 샘플:")
print(dataset["train"][0])

# 2. messages 배열을 ChatML 스타일 프롬프트로 변환
def preprocess(example):
    prompt = ""
    for msg in example["messages"]:
        if msg["role"] == "system":
            prompt += f"<|system|>\n{msg['content']}\n"
        elif msg["role"] == "user":
            prompt += f"<|user|>\n{msg['content']}\n"
        elif msg["role"] == "assistant":
            prompt += f"<|assistant|>\n{msg['content']}\n"
    return {"text": prompt}

processed = dataset["train"].map(preprocess)
print("[2] 전처리된 데이터셋 샘플:")
print(processed[0]["text"])
