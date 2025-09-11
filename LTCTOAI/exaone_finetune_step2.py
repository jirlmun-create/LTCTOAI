from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# EXAONE-3.5-2.4B-Instruct 모델명 (Hugging Face)
model_name = "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct"

print("[1] 토크나이저 로딩 중...")
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

print("[2] 모델 로딩 중... (4bit quantization, device_map='auto', GPU)")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    load_in_4bit=True,
    trust_remote_code=True
)

print("[3] 모델/토크나이저 준비 완료!")
print(f"모델: {model.__class__.__name__}")
print(f"토크나이저: {tokenizer.__class__.__name__}")
