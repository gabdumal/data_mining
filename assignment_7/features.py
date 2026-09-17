from dataclasses import dataclass
from enum import Enum


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


class Sex(Enum):
    M = "Masculine"
    F = "Feminine"


@dataclass
class Patient:
    id: int
    age: int
    sex: Sex
    amount_of_ed: int
    amount_of_m3f: int
    amount_of_h: int
    amount_of_de: int
    amount_of_r: int
    amount_of_m3i: int
    amount_of_cpum: int
    amount_of_te: int
    amount_of_di: int
    amount_of_c: int
    amount_of_p: int
    amount_of_me: int
    amount_of_im: int
    amount_of_rr: int
    amount_of_dc: int
    amount_of_i: int
    amount_of_mne: int
    amount_of_ri: int
    amount_of_rim: int
    amount_of_tem: int
    amount_of_cp: int
