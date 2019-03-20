"""
Module contains tests for PrettyJson class
"""
from pathlib import Path
import pytest
from logfile.operations.types.pretty_json import PrettyJson

# pylint: disable=redefined-outer-name

@pytest.fixture
def file_system(tmp_path):
    """
    Setup test file

    Returns:
        dict: Paths
    """
    main_dir = tmp_path / "main"
    main_file1 = main_dir / "file1.log"

    main_dir.mkdir()
    file_content = '{"hello":"Main"}'
    main_file1.write_text(file_content)

    return {
        "main": {
            "dir": main_dir,
            "file1": main_file1
        }
    }

def test_pretty_print_file(file_system):
    """
    """
    target = file_system["main"]["file1"].as_posix()
    result = PrettyJson.pretty_print_file(target)

    assert result, "Not expected return"
    assert Path(target).exists(), "File should not be deleted"

    expected = ["{", "\"hello\": \"Main\"", "}"]

    with open(target) as filecontent:
        for counter, line in enumerate(filecontent):
            assert expected[counter] == line.strip(), "Not expected result"


def test_pretty_print_file_arg_none():
    """
    """
    target = None
    result = PrettyJson.pretty_print_file(target)

    assert not result, "Not expected return"

def test_pretty_print_file_invalid_path():
    """
    """
    target = "Invalid/path/test.txt"
    result = PrettyJson.pretty_print_file(target)

    assert not result, "Not expected return"

def test_run_workfolder_none():
    """
    """
    var = PrettyJson(None, None)
    assert not var.run(), "This should not be able to run"

def test_run_invalid_workfolder():
    """
    """
    target = "Invalid/path/test.txt"
    var = PrettyJson(target, None)
    assert not var.run(), "This should not be able to run"

def test_run(file_system):
    """
    """
    target = file_system["main"]["dir"].as_posix()
    var = PrettyJson(target, None)
    assert var.run(), "This should be able to run"