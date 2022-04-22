import pytest
import base64


def test_convert_file_to_b64_string():
    from patient_side_gui import convert_file_to_b64_string
    b64str = convert_file_to_b64_string("test_image.jpg")
    assert b64str[0:20] == "/9j/4RUfRXhpZgAATU0A"


@pytest.mark.parametrize("input_id, expected", [
    [70, 70],
    ["Hello", False],
])
def test_verify_GUI_inputs(input_id, expected):
    from patient_side_gui import verify_GUI_inputs
    answer = verify_GUI_inputs(input_id)
    assert answer == expected


@pytest.mark.parametrize("input_name, expected", [
    ["Ben", True],
    [25, False],
])
def test_verify_GUI_name_inputs(input_name, expected):
    from patient_side_gui import verify_GUI_name_input
    answer = verify_GUI_name_input(input_name)
    assert answer == expected


@pytest.mark.parametrize("input_name, expected", [
    ["Ben", "Ben"],
    ["Enter a name here", ""],
])
def test_is_name_empty(input_name, expected):
    from patient_side_gui import is_name_empty
    answer = is_name_empty(input_name)
    assert answer == expected
