"""
Module contains test for ReadFullDocument
"""

import pytest
from logfile.readers.types.read_full_document import ReadFullDocument

# pylint: disable=redefined-outer-name


@pytest.fixture
def file_system(tmp_path):
    """
    Making test files

    Returns:
        dict: Files and folders created
    """
    main_dir = tmp_path / "main"
    main_file1 = main_dir / "file1.txt"

    main_dir.mkdir()
    main_file1.write_text("Beolab90")

    return {
        "main": {
            "dir": main_dir,
            "file1": main_file1
        }
    }


def test_read(file_system):
    """
    Test read full document
    """
    workfolder = file_system["main"]["dir"]
    target = file_system["main"]["file1"].name
    instructions = {
        "KeyName": "Host Name",
        "EnableLineNumber": "False"
    }
    var = ReadFullDocument(workfolder, target, instructions)
    result = var.read()

    assert len(result.container) == 1
    data = result.container[0]

    assert data.key == "Host Name"
    assert data.values == ("Beolab90",)


def test_read_invalid_workfolder():
    """
    Test read full document dont run
    """
    workfolder = "invalid/path"
    target = "file1.txt"
    instructions = {
        "KeyName": "Host Name",
        "EnableLineNumber": "False"
    }
    var = ReadFullDocument(workfolder, target, instructions)
    result = var.read()

    assert not result.container


def test_read_with_linenumber(file_system):
    """
    Test read full document with linenumber
    """
    workfolder = file_system["main"]["dir"]
    target = file_system["main"]["file1"].name
    instructions = {
        "KeyName": "Host Name",
        "EnableLineNumber": "True"
    }
    var = ReadFullDocument(workfolder, target, instructions)
    result = var.read()

    assert len(result.container) == 1
    data = result.container[0]

    assert data.key == "Host Name"
    assert data.values == ("1", "Beolab90")


def test_read_invalid_instructions(file_system):
    """
    Test run without KeyName instruction set
    """
    workfolder = file_system["main"]["dir"]
    target = file_system["main"]["file1"].name
    instructions = {
        "no": "Host Name"
    }
    var = ReadFullDocument(workfolder, target, instructions)
    result = var.read()

    assert not result.container
