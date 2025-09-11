from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, BitsAndBytesConfig
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch

# 1. 모델/토크나이저 준비 (QLoRA)
model_name = "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=bnb_config,
    trust_remote_code=True
)

model = prepare_model_for_kbit_training(model)
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# 2. 데이터셋 로딩 및 전처리
def tokenize_and_label(example):
    prompt = ""
    for msg in example["messages"]:
        if msg["role"] == "system":
            prompt += f"<|system|>\n{msg['content']}\n"
        elif msg["role"] == "user":
            prompt += f"<|user|>\n{msg['content']}\n"
        elif msg["role"] == "assistant":
            prompt += f"<|assistant|>\n{msg['content']}\n"
    tokenized = tokenizer(prompt, truncation=True, max_length=1024, padding="max_length")
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

dataset = load_dataset("json", data_files="c:/Working/LTCTOAI/LTCTOAI/2026_daycare_eval.jsonl")
dataset = dataset["train"].map(tokenize_and_label, remove_columns=dataset["train"].column_names)

# 3. 트레이닝 인자 설정
training_args = TrainingArguments(
    output_dir="./exaone_qlora_result",
    per_device_train_batch_size=1,
    num_train_epochs=1,
    fp16=True,
    save_steps=10,
    logging_steps=2,
    report_to="none",
    remove_unused_columns=False
)

from transformers import DataCollatorForLanguageModeling
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# 4. Trainer로 QLoRA 파인튜닝
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator,
)

trainer.train()
print("[완료] QLoRA 파인튜닝이 끝났습니다. ./exaone_qlora_result 폴더를 확인하세요.")
