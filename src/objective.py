from dataclasses import dataclass


@dataclass(frozen=True)
class Objective:
    problem: str
    nutritional_component: str
