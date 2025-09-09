"""
Hugging Face Transformers 기반 KoAlpaca 모델 문맥형 프롬프트 테스트 샘플
필수 패키지: transformers, torch
사전 설치: pip install transformers torch
모델명 예시: beomi/KoAlpaca-Polyglot-12.8B
"""


import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def query_koalpaca(prompt, model_name="kLGAI-EXAONE/EXAONE-3.5-2.4B-Instruct", max_new_tokens=256, device=None):
	print("[1] 모델/토크나이저 준비 시작")
	try:
		# 4bit quantization(GPU, bitsandbytes)로 로딩 시도
		device = "cuda" if torch.cuda.is_available() else "cpu"
		token = os.getenv("HF_TOKEN", "")
		if not token:
			raise ValueError("HF_TOKEN 환경변수가 설정되어 있지 않습니다.")
		model_name = "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct"
		print("[2] 토크나이저 로딩 중...")
		tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False, token=token)
		if device == "cuda":
			print("[3] 모델 로딩 중... (4bit quantization, device_map='auto', GPU)")
			model = AutoModelForCausalLM.from_pretrained(
				model_name,
				token=token,
				device_map="auto",
				load_in_4bit=True,
				trust_remote_code=True
			)
			print("[3-1] 모델 로딩 완료 (4bit, GPU)")
		else:
			print("[3] 모델 로딩 중... (4bit quantization 없이, device_map=None, CPU)")
			model = AutoModelForCausalLM.from_pretrained(
				model_name,
				token=token,
				device_map=None,
				trust_remote_code=True
			)
			print("[3-1] 모델 로딩 완료 (4bit 미사용, CPU)")

		# 아주 짧은 프롬프트로 추론 테스트
		short_prompt = "안녕?"
		print(f"[4] 입력 토큰화 중... (짧은 프롬프트: {short_prompt})")
		input_ids = tokenizer(short_prompt, return_tensors="pt").input_ids.to(device)
		print("[5] 추론 시작 (짧은 프롬프트)")
		try:
			with torch.no_grad():
				output = model.generate(input_ids, max_new_tokens=32, do_sample=True, top_p=0.95, temperature=0.8)
			print("[6] 결과 디코딩 (짧은 프롬프트)")
			result = tokenizer.decode(output[0], skip_special_tokens=True)
			print(f"[7] 짧은 프롬프트 결과: {result}")
		except Exception as e:
			print(f"[에러] 짧은 프롬프트 추론 실패: {e}")

		# 원래 프롬프트로도 추가 테스트
		print("[8] 입력 토큰화 중... (원래 프롬프트)")
		input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
		print("[9] 추론 시작 (원래 프롬프트)")
		try:
			with torch.no_grad():
				output = model.generate(input_ids, max_new_tokens=max_new_tokens, do_sample=True, top_p=0.95, temperature=0.8)
			print("[10] 결과 디코딩 (원래 프롬프트)")
			result = tokenizer.decode(output[0], skip_special_tokens=True)
			print(f"[11] 원래 프롬프트 결과: {result}")
			return result
		except Exception as e:
			print(f"[에러] 원래 프롬프트 추론 실패: {e}")
			return None
	except Exception as e:
		print("[에러 발생]", e)
		print(traceback.format_exc())
		return None

import traceback

if __name__ == "__main__":
	print("[KoAlpaca 문맥형 응답 테스트]")
	prompt = "장기요양기관 평가의 목적을 설명하라."
	result = query_koalpaca(prompt)
	print("[최종 결과]", result)
	print("[실행 완료]")
