descriptions_of_columns = [
    ("age", "Age"),
    ("systolic_bp", "Systolic blood pressure"),
    ("diastolic_bp", "Diastolic blood pressure"),
    ("blood_sugar", "Blood sugar"),
    ("body_temperature", "Body temperature"),
    ("heart_rate", "Heart rate"),
    ("risk_level", "Risk level"),
]


def columns_labels() -> list[str]:
    return [label for label, _ in descriptions_of_columns]


def columns_names() -> list[str]:
    return [name for _, name in descriptions_of_columns]


name_of_column = dict(descriptions_of_columns)


def get_name_of_column(label: str) -> str:
    return name_of_column[label]
