import re


class Utilities:
    @staticmethod
    def camel_to_snake(camel_case_str: str) -> str:
        return re.sub(r"([a-z])([A-Z])", r"\1_\2", camel_case_str).lower()
