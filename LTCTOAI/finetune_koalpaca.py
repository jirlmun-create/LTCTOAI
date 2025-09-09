# KoAlpaca 파인튜닝 파이프라인 예시 (실습용)

import os
import argparse
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer

MODEL_NAME = "beomi/KoAlpaca-Polyglot-12.8B"

def main(train_file, output_dir):
    # 데이터셋 로드 (KoAlpaca 포맷: instruction/output)
    dataset = load_dataset('json', data_files={'train': train_file})
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    def preprocess(example):
        prompt = example["instruction"]
        completion = example["output"]
        text = f"### 질문: {prompt}\n### 답변: {completion}"
        return tokenizer(text, truncation=True, max_length=512)

    tokenized = dataset["train"].map(preprocess)

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=1,
        per_device_train_batch_size=2,
        save_steps=50,
        logging_steps=10,
        fp16=True,
        report_to=[],
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
    )
    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"파인튜닝 완료: {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_file', type=str, default='datasets/koalpaca_train.jsonl')
    parser.add_argument('--output_dir', type=str, default='output/koalpaca_finetuned')
    args = parser.parse_args()
    main(args.train_file, args.output_dir)
