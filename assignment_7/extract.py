import csv
import json
from dataclasses import fields
from pathlib import Path

from features import Condition, Patient, Sex, conditions


def condition_to_field(condition: Condition) -> str:
    """Convert e.g. 'M3f' -> 'amount_of_m3f'."""
    return f"amount_of_{condition.label.lower()}"


def extract_patients(data: dict) -> list[Patient]:
    # First create one Patient for every image.
    patients: dict[int, Patient] = {
        image["id"]: Patient(
            id=image["id"],
            age=int(image["age"]),
            sex=Sex(image["sex"]),
        )
        for image in data["images"]
    }

    # Then accumulate annotation counts into the appropriate patient.
    for annotation in data["annotations"]:
        image_id = annotation["image_id"]
        category_id = annotation["category_id"]

        patient = patients[image_id]
        condition = conditions[category_id]

        field_name = condition_to_field(condition)
        setattr(patient, field_name, getattr(patient, field_name) + 1)

    return list(patients.values())


def write_csv(patients: list[Patient], output_path: Path) -> None:
    field_names = [field.name for field in fields(Patient)]

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()

        for patient in patients:
            row = {
                field.name: (
                    patient.sex.name
                    if field.name == "sex"
                    else getattr(patient, field.name)
                )
                for field in fields(Patient)
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
