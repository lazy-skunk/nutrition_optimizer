from dataclasses import dataclass


@dataclass(frozen=True)
class Constraint:
    min_max: str
    nutritional_component: str
    unit: str
    value: int
