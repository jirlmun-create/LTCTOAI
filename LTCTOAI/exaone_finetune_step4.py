from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset
import torch

# 1. 모델/토크나이저 준비
model_name = "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    load_in_4bit=True,
    trust_remote_code=True
)

# 2. 데이터셋 로딩 및 전처리
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

dataset = load_dataset("json", data_files="c:/Working/LTCTOAI/LTCTOAI/2026_daycare_eval.jsonl")
dataset = dataset["train"].map(preprocess)

# 3. 트레이닝 인자 설정
training_args = TrainingArguments(
    output_dir="./exaone_finetune_result",
    per_device_train_batch_size=1,
    num_train_epochs=1,
    fp16=True,
    save_steps=10,
    logging_steps=2,
    report_to="none"
)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# 4. Trainer로 파인튜닝
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator,
)

trainer.train()
print("[완료] 파인튜닝이 끝났습니다. ./exaone_finetune_result 폴더를 확인하세요.")
