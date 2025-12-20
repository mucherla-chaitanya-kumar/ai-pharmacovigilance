"""
NER Pipeline
-------------
Responsible ONLY for:
- Drug names
- Events / symptoms
- Lab mentions (entity-level, not values)

Explicitly DOES NOT extract:
- Dose
- Weight / Height
- Route
- Dates

Those are handled by regex extractors.
"""

from app.nlp.biobert_ner import bio_bert_extract


# Terms that should NEVER be treated as drugs
LAB_BLACKLIST = {
    "creatine",
    "creatine kinase",
    "ck",
    "ast",
    "alt"
}

def run_ner(text: str) -> dict:
    """
    Runs BioBERT / ClinicalBERT NER and returns raw entities
    """
    return bio_bert_extract(text)


def postprocess_entities(entities):
    """
    Accepts either:
    - list of entities
    - dict with key 'raw_entities'
    """

    # Normalize input
    if isinstance(entities, list):
        raw_entities = entities
    elif isinstance(entities, dict):
        raw_entities = entities.get("raw_entities", [])
    else:
        raw_entities = []

    drugs = []
    events = []
    labs = []

    for ent in raw_entities:
        text = ent.get("text", "").strip()
        label = ent.get("label", "").upper()

        if not text:
            continue

        if label == "CHEMICAL":
            if text.lower() in LAB_BLACKLIST:
                labs.append(text)
            else:
                drugs.append(text)

        elif label in {"DISEASE", "SYMPTOM"}:
            events.append(text)

    return {
        "primary_drug": drugs[0] if drugs else "",
        "drugs": list(set(drugs)),
        "events": list(set(events)),
        "labs": list(set(labs))
    }

