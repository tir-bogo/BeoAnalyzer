"""
Module contains tests for ReaderBase
"""

import pytest
from logfile.readers.reader_base import ReaderBase

# pylint: disable=redefined-outer-name


class MockReaderBase(ReaderBase):
    """
    Mock for ReaderBase
    """
    def read(self):
        """
        Mock for abstract method
        """


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
    main_file1.write_text("Beolab_50")

    return {
        "main": {
            "dir": main_dir,
            "file1": main_file1
        }
    }


def test_file_path(file_system):
    """
    Test get filepath
    """
    workfolder = file_system["main"]["dir"].as_posix()
    rel_path = file_system["main"]["file1"].name
    var = MockReaderBase(workfolder, rel_path, None)

    expected = file_system["main"]["file1"].as_posix()
    assert var.file_path == expected


def test_file_path_relative_path_none(file_system):
    """
    Test file_path returns "" when relative path is none
    """
    workfolder = file_system["main"]["dir"].as_posix()
    rel_path = None
    var = MockReaderBase(workfolder, rel_path, None)

    assert not var.file_path


def test_file_path_workfolder_none():
    """
    Test file_path returns "" when workfolder path is none
    """
    workfolder = None
    rel_path = "test.txt"
    var = MockReaderBase(workfolder, rel_path, None)

    assert not var.file_path


def test_file_path_invalid_path():
    """
    Test file_path returns "" when path do not exists
    """
    workfolder = "Invalid/path/"
    rel_path = "test.txt"
    var = MockReaderBase(workfolder, rel_path, None)

    assert not var.file_path


def test_key_name_instruction():
    """
    Test can get key name from instructions
    """
    expected = "Host name"
    instructions = {
        "KeyName": expected
    }
    var = MockReaderBase(None, None, instructions)
    assert var.key_name_instruction == expected


def test_key_name_instruction_default_value():
    """
    Test can get default key name
    """
    expected = ""
    instructions = {
        "not valid instruction": expected
    }
    var = MockReaderBase(None, None, instructions)
    assert var.key_name_instruction == expected


def test_key_name_instruction_instructions_none():
    """
    Test can get default key name when instructions is none
    """
    expected = ""
    var = MockReaderBase(None, None, None)
    assert var.key_name_instruction == expected


def test_enable_linenumber_instruction():
    """
    Test can get enable line number
    """
    expected = True
    instructions = {
        "EnableLineNumber": "true"
    }
    var = MockReaderBase(None, None, instructions)
    assert var.enable_linenumber_instruction == expected


def test_enable_linenumber_instruction_default_value():
    """
    Test can get enable line number default value
    """
    expected = False
    instructions = {
        "regex": "true"
    }
    var = MockReaderBase(None, None, instructions)
    assert var.enable_linenumber_instruction == expected


def test_enable_linenumber_instruction_instructions_none():
    """
    Test can get enable line number default value when instructions is none
    """
    expected = False
    var = MockReaderBase(None, None, None)
    assert var.enable_linenumber_instruction == expected
