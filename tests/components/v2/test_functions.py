from typing import Dict, List

import marvin.v2
import pytest
from pydantic import BaseModel

from tests.utils import pytest_mark_class


@marvin.v2.fn
def list_fruit(n: int = 2) -> list[str]:
    """Returns a list of `n` fruit"""


@marvin.v2.fn
def list_fruit_color(n: int, color: str = None) -> list[str]:
    """Returns a list of `n` fruit that all have the provided `color`"""


@pytest_mark_class("llm")
class TestFunctions:
    class TestBasics:
        def test_list_fruit(self):
            result = list_fruit()
            assert len(result) == 2

        def test_list_fruit_argument(self):
            result = list_fruit(5)
            assert len(result) == 5

    class TestAnnotations:
        def test_no_annotations(self):
            @marvin.v2.fn
            def f(x):
                """returns x + 1"""

            result = f(3)
            assert result == "4"

        def test_arg_annotations(self):
            @marvin.v2.fn
            def f(x: int):
                """returns x + 1"""

            result = f(3)
            assert result == "4"

        def test_return_annotations(self):
            @marvin.v2.fn
            def f(x) -> int:
                """returns x + 1"""

            result = f("3")
            assert result == 4

        def test_list_fruit_with_generic_type_hints(self):
            @marvin.v2.fn
            def list_fruit(n: int) -> List[str]:
                """Returns a list of `n` fruit"""

            result = list_fruit(3)
            assert len(result) == 3

        def test_basemodel_return_annotation(self):
            class Fruit(BaseModel):
                name: str
                color: str

            @marvin.v2.fn
            def get_fruit(description: str) -> Fruit:
                """Returns a fruit with the provided description"""

            fruit = get_fruit("loved by monkeys")
            assert fruit.name.lower() == "banana"
            assert fruit.color.lower() == "yellow"

        @pytest.mark.parametrize("name,expected", [("banana", True), ("car", False)])
        def test_bool_return_annotation(self, name, expected):
            @marvin.v2.fn
            def is_fruit(name: str) -> bool:
                """Returns True if the provided name is a fruit"""

            assert is_fruit(name) == expected

        @pytest.mark.skipif(
            marvin.settings.openai.llms.model.startswith("gpt-3.5"),
            reason="3.5 turbo doesn't do well with unknown schemas",
        )
        def test_plain_dict_return_type(self):
            @marvin.v2.fn
            def describe_fruit(description: str) -> dict:
                """guess the fruit and return the name and color"""

            fruit = describe_fruit("the one thats loved by monkeys")
            assert fruit["name"].lower() == "banana"
            assert fruit["color"].lower() == "yellow"

        @pytest.mark.skipif(
            marvin.settings.openai.llms.model.startswith("gpt-3.5"),
            reason="3.5 turbo doesn't do well with unknown schemas",
        )
        def test_annotated_dict_return_type(self):
            @marvin.v2.fn
            def describe_fruit(description: str) -> dict[str, str]:
                """guess the fruit and return the name and color"""

            fruit = describe_fruit("the one thats loved by monkeys")
            assert fruit["name"].lower() == "banana"
            assert fruit["color"].lower() == "yellow"

        @pytest.mark.skipif(
            marvin.settings.openai.llms.model.startswith("gpt-3.5"),
            reason="3.5 turbo doesn't do well with unknown schemas",
        )
        def test_generic_dict_return_type(self):
            @marvin.v2.fn
            def describe_fruit(description: str) -> Dict[str, str]:
                """guess the fruit and return the name and color"""

            fruit = describe_fruit("the one thats loved by monkeys")
            assert fruit["name"].lower() == "banana"
            assert fruit["color"].lower() == "yellow"

        def test_typed_dict_return_type(self):
            from typing_extensions import TypedDict

            class Fruit(TypedDict):
                name: str
                color: str

            @marvin.v2.fn
            def describe_fruit(description: str) -> Fruit:
                """guess the fruit and return the name and color"""

            fruit = describe_fruit("the one thats loved by monkeys")
            assert fruit["name"].lower() == "banana"
            assert fruit["color"].lower() == "yellow"

        def test_int_return_type(self):
            @marvin.v2.fn
            def get_fruit(name: str) -> int:
                """Returns the number of letters in the alluded fruit name"""

            assert get_fruit("banana") == 6

        def test_float_return_type(self):
            @marvin.v2.fn
            def get_pi(n: int) -> float:
                """Return the first n decimals of pi"""

            assert get_pi(5) == 3.14159

        def test_tuple_return_type(self):
            @marvin.v2.fn
            def get_fruit(name: str) -> tuple:
                """Returns a tuple of fruit"""

            assert get_fruit("alphabet of fruit, first 3, singular") == (
                "apple",
                "banana",
                "cherry",
            )

        def test_set_return_type(self):
            @marvin.v2.fn
            def get_fruit_letters(name: str) -> set:
                """Returns the letters in the provided fruit name"""

            assert get_fruit_letters("banana") == {"a", "b", "n"}

        def test_frozenset_return_type(self):
            @marvin.v2.fn
            def get_fruit_letters(name: str) -> frozenset:
                """Returns the letters in the provided fruit name"""

            assert get_fruit_letters("orange") == frozenset(
                {"a", "e", "g", "n", "o", "r"}
            )
