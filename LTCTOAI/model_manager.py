from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os

def load_model(model_name="distilbert-base-uncased"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return model, tokenizer

def save_model(model, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    model.save_pretrained(save_dir)

def load_local_model(save_dir):
    model = AutoModelForSequenceClassification.from_pretrained(save_dir)
    tokenizer = AutoTokenizer.from_pretrained(save_dir)
    return model, tokenizer
