import re

def extract_dose_fields(text: str) -> dict:
    data = {}

    dose = re.search(r"Dose:\s*(\d+)\s*(mg)", text, re.IGNORECASE)
    freq = re.search(r"(once daily|twice daily|daily)", text, re.IGNORECASE)
    route = re.search(r"Route:\s*(Oral|IV|Intravenous)", text, re.IGNORECASE)

    if dose:
        data["dose_value__v"] = dose.group(1)
        data["dose_unit__v"] = dose.group(2)

    if freq:
        data["frequency_value__v"] = freq.group(1)

    if route:
        data["drug_route__v"] = route.group(1)

    start = re.search(r"Therapy Start Date:\s*(.+)", text)
    end = re.search(r"Therapy End Date:\s*(.+)", text)

    if start:
        data["therapy_start_date__v"] = start.group(1).strip()
    if end:
        data["therapy_end_date__v"] = end.group(1).strip()

    return data
