# app/nlp/biobert_ner.py

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

MODEL_NAME = "dslim/bert-base-NER"   # stable public model

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)

nlp = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)

def bio_bert_extract(text: str):
    try:
        outputs = nlp(text)
        entities = []
        for ent in outputs:
            entities.append({
                "text": ent["word"],
                "label": ent["entity_group"]
            })
        return entities
    except Exception as e:
        print("BioBERT Error:", e)
        return []
