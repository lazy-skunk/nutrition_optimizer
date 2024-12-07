from dataclasses import dataclass


@dataclass(frozen=True)
class Objective:
    problem: str
    nutritional_component: str

    def __post_init__(self) -> None:
        self._validate_problem_type()
        self._validate_nutritional_component()

    def _validate_problem_type(self) -> None:
        # TODO: getattr で呼び出せる形式にしたいかも。LpMaximize と LpMinimize で指定するのがいいかな。
        if self.problem not in ["minimize", "maximize"]:
            raise ValueError(
                f"Invalid problem type: {self.problem}."
                " Valid values are 'minimize' or 'maximize'."
            )

    def _validate_nutritional_component(self) -> None:
        valid_components = ["energy", "protein", "fat", "carbohydrates"]
        if self.nutritional_component not in valid_components:
            raise ValueError(
                f"Invalid nutritional component: {self.nutritional_component}."
                f" Valid components are {valid_components}."
            )
