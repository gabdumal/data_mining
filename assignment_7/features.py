from dataclasses import dataclass
from enum import Enum
from typing import Literal

# # Data on JSON


class SuperCategory(Enum):
    Mouth = "Mouth"
    Artificial = "Artificial Teeth"
    Natural = "Natural Teeth"
    Mixed = "Mix Teeth"


@dataclass
class Condition:
    label: str
    name: str
    super_category: SuperCategory


conditions: dict[int, Condition] = {
    1: Condition(label="Ed", name="Edentulous", super_category=SuperCategory.Mouth),
    2: Condition(
        label="M3f",
        name="Developing third molar",
        super_category=SuperCategory.Natural,
    ),
    3: Condition(
        label="H",
        name="Healthy",
        super_category=SuperCategory.Natural,
    ),
    4: Condition(
        label="De",
        name="Dentate",
        super_category=SuperCategory.Mouth,
    ),
    5: Condition(
        label="R",
        name="Restored",
        super_category=SuperCategory.Natural,
    ),
    6: Condition(
        label="M3i",
        name="Impacted third molar",
        super_category=SuperCategory.Natural,
    ),
    7: Condition(
        label="CpuM",
        name="Single prosthetic crown (mixed)",
        super_category=SuperCategory.Mixed,
    ),
    8: Condition(
        label="Te",
        name="Endodontic treatment",
        super_category=SuperCategory.Natural,
    ),
    9: Condition(
        label="Di",
        name="Incisal wear",
        super_category=SuperCategory.Natural,
    ),
    10: Condition(
        label="C",
        name="Caries",
        super_category=SuperCategory.Natural,
    ),
    11: Condition(
        label="P",
        name="Pontic",
        super_category=SuperCategory.Artificial,
    ),
    12: Condition(
        label="Me",
        name="Maxilla edentulous",
        super_category=SuperCategory.Mouth,
    ),
    13: Condition(
        label="Im",
        name="Implant",
        super_category=SuperCategory.Artificial,
    ),
    14: Condition(
        label="Rr",
        name="Residual root",
        super_category=SuperCategory.Natural,
    ),
    15: Condition(
        label="Dc",
        name="Crown destruction",
        super_category=SuperCategory.Natural,
    ),
    16: Condition(
        label="I",
        name="Impacted",
        super_category=SuperCategory.Natural,
    ),
    17: Condition(
        label="Mne",
        name="Mandible edentulous",
        super_category=SuperCategory.Mouth,
    ),
    18: Condition(
        label="Ri",
        name="Intraradicular post",
        super_category=SuperCategory.Natural,
    ),
    19: Condition(
        label="RiM",
        name="Intraradicular post (mixed)",
        super_category=SuperCategory.Mixed,
    ),
    20: Condition(
        label="TeM",
        name="Endodontic treatment (mixed)",
        super_category=SuperCategory.Mixed,
    ),
    21: Condition(
        label="Cp",
        name="Single prosthetic crown",
        super_category=SuperCategory.Artificial,
    ),
}


# # Records

Sex = Literal["M", "F"]


@dataclass
class Patient:
    id: int
    age: int
    sex: Sex
    amount_of_ed: int = 0
    amount_of_m3f: int = 0
    amount_of_h: int = 0
    amount_of_de: int = 0
    amount_of_r: int = 0
    amount_of_m3i: int = 0
    amount_of_cpum: int = 0
    amount_of_te: int = 0
    amount_of_di: int = 0
    amount_of_c: int = 0
    amount_of_p: int = 0
    amount_of_me: int = 0
    amount_of_im: int = 0
    amount_of_rr: int = 0
    amount_of_dc: int = 0
    amount_of_i: int = 0
    amount_of_mne: int = 0
    amount_of_ri: int = 0
    amount_of_rim: int = 0
    amount_of_tem: int = 0
    amount_of_cp: int = 0


# # Features

descriptions_of_columns = [
    ("id", "ID"),
    ("age", "Age"),
    ("sex", "Sex"),
    ("amount_of_ed", "Am. Ed"),
    ("amount_of_m3f", "Am. M3f"),
    ("amount_of_h", "Am. H"),
    ("amount_of_de", "Am. De"),
    ("amount_of_r", "Am. R"),
    ("amount_of_m3i", "Am. M3i"),
    ("amount_of_cpum", "Am. CpuM"),
    ("amount_of_te", "Am. Te"),
    ("amount_of_di", "Am. Di"),
    ("amount_of_c", "Am. C"),
    ("amount_of_p", "Am. P"),
    ("amount_of_me", "Am. Me"),
    ("amount_of_im", "Am. Im"),
    ("amount_of_rr", "Am. Rr"),
    ("amount_of_dc", "Am. Dc"),
    ("amount_of_i", "Am. I"),
    ("amount_of_mne", "Am. Mne"),
    ("amount_of_ri", "Am. Ri"),
    ("amount_of_rim", "Am. RiM"),
    ("amount_of_tem", "Am. TeM"),
    ("amount_of_cp", "Am. Cp"),
]


def columns_labels() -> list[str]:
    return [label for label, _ in descriptions_of_columns]


def columns_names() -> list[str]:
    return [name for _, name in descriptions_of_columns]


name_of_column = dict(descriptions_of_columns)


def get_name_of_column(label: str) -> str:
    return name_of_column[label]
