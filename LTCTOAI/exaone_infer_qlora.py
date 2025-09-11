from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# QLoRA 파인튜닝 결과 폴더
base_model = "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct"
qlora_dir = "./exaone_qlora_result"

# 1. 토크나이저/모델 로딩
print("[1] 토크나이저 로딩 중...")
tokenizer = AutoTokenizer.from_pretrained(base_model, use_fast=False)
print("[2] 베이스 모델 로딩 중... (4bit)")
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    device_map="auto",
    load_in_4bit=True,
    trust_remote_code=True
)
print("[3] QLoRA 어댑터 로딩 중...")
model = PeftModel.from_pretrained(model, qlora_dir)

# 2. 추론 프롬프트 예시
prompt = """
<|system|>
당신은 2026년도 주간보호 평가 전문가입니다.
<|user|>
평가지표 1번(운영규정) 요약 및 주의점 설명
<|assistant|>
"""
input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
print("[4] 추론 시작...")
with torch.no_grad():
    output = model.generate(input_ids, max_new_tokens=128, do_sample=True, top_p=0.95, temperature=0.8)
result = tokenizer.decode(output[0], skip_special_tokens=True)
print("[5] 추론 결과:")
print(result)
