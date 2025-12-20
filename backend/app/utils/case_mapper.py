def map_case(ner: dict, regex_data: dict) -> dict:
    drugs = ner.get("drugs", []) if isinstance(ner, dict) else []
    events = ner.get("events", []) if isinstance(ner, dict) else []

    primary_drug = (
        regex_data.get("drug_name")
        or (drugs[0] if drugs else "")
    )

    primary_event = events[0] if events else ""

    return {
        "patient": {
            "patient_onset_age__v": regex_data.get("patient_onset_age__v", ""),
            "patient_age_unit__v": regex_data.get("patient_age_unit__v", ""),
            "gender__v": regex_data.get("gender__v", ""),
            "weight_value__v": regex_data.get("weight_value__v", ""),
            "weight_unit__v": regex_data.get("weight_unit__v", ""),
            "height_value__v": regex_data.get("height_value__v", ""),
            "height_unit__v": regex_data.get("height_unit__v", ""),
            "patient_medical_history__v": ""
        },
        "drug": {
    "product_reported__v": primary_drug,
    "dose_value__v": regex_data.get("dose_value__v", ""),
    "dose_unit__v": regex_data.get("dose_unit__v", ""),
    "frequency_value__v": regex_data.get("frequency_value__v", ""),
    "drug_route__v": regex_data.get("drug_route__v", ""),
    "therapy_start_date__v": regex_data.get("therapy_start_date__v", ""),
    "therapy_end_date__v": regex_data.get("therapy_end_date__v", ""),
    "drug_role__v": "Suspect" if primary_drug else ""
},

        "event": {
    "event_reported__v": regex_data.get("event_reported__v", ""),
    "onset_idate__v": regex_data.get("onset_idate__v", ""),
    "seriousness__v": "Non-serious",
    "hospitalization_required__v": "No",
    "outcome__v": regex_data.get("outcome__v", "")
},

        "labs": [],
        "narrative": ""
    }
