def validate_semantic(case: dict) -> dict:
    errors = []

    patient = case.get("patient", {})
    drug = case.get("drug", {})

    if drug.get("drug_role__v") == "Suspect":
        if not drug.get("dose_value__v"):
            errors.append("Suspect drug missing dose")

    if not patient.get("weight_value__v"):
        errors.append("Patient weight missing")

    if not patient.get("height_value__v"):
        errors.append("Patient height missing")

    if "statin" in (drug.get("product_reported__v") or "").lower():
        if not case.get("labs"):
            errors.append("Statin adverse event without CK lab")

    return {
        "semantic_valid": len(errors) == 0,
        "errors": errors
    }
