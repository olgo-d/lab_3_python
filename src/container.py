from dataclasses import dataclass

from src.math_func import MathFunc
from src.sorting import SortFunc


@dataclass
class Container:
    math_function: MathFunc
    sort_function: SortFunc


def build_container() -> Container:
    return Container(
        math_function=MathFunc(),
        sort_function=SortFunc(),
    )
