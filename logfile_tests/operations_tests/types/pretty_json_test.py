"""
Module contains tests for PrettyJson class
"""
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

def test_no_valid_workfolder():
    """
    Testing run returns false if there is no workfolder
    """
    var = PrettyJson()
    result = var.run()

    assert not result, "The workfolder is None, this should return False"

def test_pretty_print(file_system):
    """
    Testing pretty print is working
    """
    var = PrettyJson()
    var.workfolder = file_system["main"]["dir"].as_posix()
    result = var.run()

    assert result, "This should be able to run"

    assert file_system["main"]["file1"].exists(), "Main file1 should exists"

    expected = ["{", "\"hello\": \"Main\"", "}"]

    with open(file_system["main"]["file1"].as_posix()) as filecontent:
        for counter, line in enumerate(filecontent):
            assert expected[counter] == line.strip(), "Not expected result"
