import csv
import json
from dataclasses import fields
from pathlib import Path
from typing import TypeGuard

from features import (
    Condition,
    MouthCondition,
    Patient,
    conditions,
    mouth_conditions,
)


def condition_to_field(condition: Condition) -> str:
    """Convert e.g. 'M3f' -> 'amount_of_m3f'."""
    return f"amount_of_{condition.label.lower()}"


def is_mouth_condition(value: str) -> TypeGuard[MouthCondition]:
    return value in mouth_conditions


def extract_patients(data: dict) -> list[Patient]:
    patients: dict[int, Patient] = {
        image["id"]: Patient(
            id=image["id"],
            age=int(image["age"]),
            sex=image["sex"],
        )
        for image in data["images"]
    }

    for annotation in data["annotations"]:
        image_id = annotation["image_id"]
        category_id = annotation["category_id"]

        patient = patients[image_id]
        condition = conditions[category_id]

        if is_mouth_condition(condition.label):
            patient.mouth_condition = condition.label
        else:
            field_name = condition_to_field(condition)
            setattr(
                patient,
                field_name,
                getattr(patient, field_name) + 1,
            )

    return list(patients.values())


def write_csv(
    patients: list[Patient],
    output_path: Path,
) -> None:
    field_names = [field.name for field in fields(Patient)]

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=field_names,
        )
        writer.writeheader()

        for patient in patients:
            row = {
                field.name: getattr(patient, field.name) for field in fields(Patient)
            }
            writer.writerow(row)


def main() -> None:
    input_path = Path("data/mouth_and_teeth_labels.json")
    output_path = Path("data/patients.csv")

    with input_path.open(encoding="utf-8") as file:
        data = json.load(file)

    patients = extract_patients(data)
    write_csv(patients, output_path)


if __name__ == "__main__":
    main()
