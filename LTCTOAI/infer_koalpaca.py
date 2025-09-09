# KoAlpaca 추론(테스트) 파이프라인 예시

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_PATH = "output/koalpaca_finetuned"  # 파인튜닝된 모델 경로

def infer(prompt, model_path=MODEL_PATH):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    input_text = f"### 질문: {prompt}\n### 답변:"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    with torch.no_grad():
        output_ids = model.generate(input_ids, max_new_tokens=128, do_sample=True)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # 답변 부분만 추출
    answer = output_text.split('### 답변:')[-1].strip()
    return answer

if __name__ == "__main__":
    test_prompt = "파이썬에서 리스트를 정렬하는 방법을 알려줘."
    result = infer(test_prompt)
    print(f"질문: {test_prompt}\n답변: {result}")
