def generate_narrative(entities):
    age = entities.get("ages", ["Unknown"])[0]
    gender = entities.get("genders", ["Unknown"])[0]
    drug = entities.get("drugs", ["Unknown drug"])[0]
    event = entities.get("events", ["No adverse event reported"])[0]
    freq = entities.get("dose_info", {}).get("frequency", "")
    dose = entities.get("dose_info", {}).get("dose", "")
    route = entities.get("route", "")

    narrative = (
        f"A {age}-year-old {gender} patient was treated with {drug}. "
        f"The therapy involved a dose of {dose} administered {route} {freq}. "
        f"Following the treatment, the patient experienced {event}. "
        "Further evaluation and management were performed accordingly."
    )

    return narrative
