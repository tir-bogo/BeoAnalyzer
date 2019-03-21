"""
Testing OperationBase class
"""
import pytest
from logfile.operations.operation_base import OperationBase

# pylint: disable=redefined-outer-name

class MockOperationBase(OperationBase):
    """
    Class is a mock to access methods/properties within OperationBase
    """
    def run(self) -> bool:
        return True

@pytest.fixture
def file_system(tmp_path):
    """
    Setup directory with files

    Args:
        tmp_path(Path): pathlib/pathlib2.Path object

    Help:
        https://docs.pytest.org/en/latest/tmpdir.html

    Returns:
        dict: Filesystem inside dictionary
    """
    main_dir = tmp_path / "main"
    main_file1 = main_dir / "file1.txt"

    sub_dir = main_dir / "sub"
    sub_file1 = sub_dir / "file1.txt"

    sub_sub_dir = sub_dir / "sub"
    sub_sub_file1 = sub_sub_dir / "file1.txt"


    file_content = "test"

    main_dir.mkdir()
    sub_dir.mkdir()
    sub_sub_dir.mkdir()

    main_file1.write_text(file_content)
    sub_file1.write_text(file_content)
    sub_sub_file1.write_text(file_content)

    return {
        "main": {
            "dir": main_dir,
            "file1": main_file1
        },
        "sub": {
            "dir": sub_dir,
            "file1": sub_file1
        },
        "subsub":{
            "dir": sub_sub_dir,
            "file1": sub_sub_file1
        }
    }

def test_directory_instruction():
    """
    Testing direction_instruction
    """
    instructions = {"Directory": "sub"}
    var = MockOperationBase("test", instructions)
    assert var.directory_instruction == "sub"

def test_directory_instruction_is_none():
    """
    Testing direction_instruction default value
    """
    var = MockOperationBase("test", None)
    assert var.directory_instruction == "*"

def test_recursive_instruction():
    """
    Testing recursive_instruction
    """
    instructions = {"Recursive": "True"}
    var = MockOperationBase("test", instructions)
    assert var.recursive_instruction

def test_recursive_instruction_is_none():
    """
    Testing recursive_instruction default value
    """
    var = MockOperationBase("test", None)
    assert not var.recursive_instruction

def test_exclude_files_instruction():
    """
    Testing exclude_files_instruction
    """
    instructions = {"ExcludeFiles": "test.html|message.0"}
    var = MockOperationBase("test", instructions)
    assert var.exclude_files_instruction == ["test.html", "message.0"]

def test_exclude_files_instruction_is_none():
    """
    Testing exclude_files_instruction default value
    """
    var = MockOperationBase("test", None)
    assert var.exclude_files_instruction == []

def test_exclude_extensions_instruction():
    """
    Testing exclude_extensions_instruction
    """
    instructions = {"ExcludeExtensions": ".html|.log"}
    var = MockOperationBase("test", instructions)
    assert var.exclude_extensions_instruction == [".html", ".log"]

def test_exclude_extensions_instruction_is_none():
    """
    Testing exclude_extensions_instruction default value
    """
    var = MockOperationBase("test", None)
    assert var.exclude_extensions_instruction == []

def test_new_file_extension_instruction():
    """
    Testing new_file_extensions_instruction
    """
    instructions = {"NewFileExtension": ".html"}
    var = MockOperationBase("test", instructions)
    assert var.new_file_extension_instruction == ".html"

def test_new_file_extension_instruction_is_none():
    """
    Testing new_file_extensions_instruction default value
    """
    var = MockOperationBase("test", None)
    assert var.new_file_extension_instruction == ".log"

def test_make_directory_path():
    """
    Testing testing it can combine workfolder and relative path
    """
    var = MockOperationBase("c:", None)
    assert var.make_directory_path("windows") == "c:/windows"

def test_make_directory_path_arg_is_none():
    """
    Test it returns workfolder
    """
    var = MockOperationBase("c:", None)
    assert var.make_directory_path(None) == "c:"

def test_make_directory_path_start():
    """
    Test it returns workfolder
    """
    var = MockOperationBase("c:", None)
    assert var.make_directory_path("*") == "c:"

def test_get_files(file_system):
    """
    Test can get files
    """
    files = MockOperationBase.get_files(file_system["main"]["dir"], False)
    assert len(files) == 1, "Not expected count"
    assert file_system["main"]["file1"].as_posix() == files[0], "Not expected file"

def test_get_files_recursive(file_system):
    """
    Test can get files recursive
    """
    files = MockOperationBase.get_files(file_system["main"]["dir"], True)
    assert len(files) == 3, "Not expected count"
    assert file_system["main"]["file1"].as_posix() == files[0], "Not expected file"
    assert file_system["sub"]["file1"].as_posix() == files[1], "Not expected file"
    assert file_system["subsub"]["file1"].as_posix() == files[2], "Not expected file"

def test_get_files_arg_none():
    """
    Test it return empty list if arg is none
    """
    files = MockOperationBase.get_files(None, True)
    assert files == [], "There should not be found any file"

def test_get_files_dir_do_not_exists():
    """
    Test it returns empty list if dir do not exists
    """
    files = MockOperationBase.get_files("Invalid/path", True)
    assert files == [], "There should not be found any file"

def test_get_directories(file_system):
    """
    Test can get sub directories from directory
    """
    directories = MockOperationBase.get_directories(file_system["main"]["dir"], False)
    assert len(directories) == 1, "Should find 1 sub directory"
    assert file_system["sub"]["dir"].as_posix() == directories[0]

def test_get_directories_recursive(file_system):
    """
    Test can get sub directories from directory recursive
    """
    directories = MockOperationBase.get_directories(file_system["main"]["dir"], True)
    assert len(directories) == 2, "Should find 2 sub directory"
    assert file_system["sub"]["dir"].as_posix() == directories[0]
    assert file_system["subsub"]["dir"].as_posix() == directories[1]

def test_get_directories_arg_none():
    """
    Test returns empty list if arg is none
    """
    directories = MockOperationBase.get_directories(None, False)
    assert directories == [], "Should find 0 sub directories"

def test_get_directories_dir_do_not_exists():
    """
    Test returns empty list if directory do not exists
    """
    directories = MockOperationBase.get_directories("Invalid/path", False)
    assert directories == [], "Should find 0 sub directories"

def test_output_name_instruction():
    """
    Testing get output name
    """
    test_instructions = {
        "OutputName":"file.txt"
    }

    var = MockOperationBase(None, test_instructions)
    assert var.output_name_instruction == "file.txt", "Not expected value"

def test_output_name_instruction_is_none():
    """
    Testing get default output name
    """
    var = MockOperationBase(None, None)
    assert var.output_name_instruction == "", "Not expected value"

def test_regex_expression_instruction():
    """
    Testing get output name
    """
    test_instructions = {
        "RegexExpression": "^[.*]"
    }

    var = MockOperationBase(None, test_instructions)
    assert var.regex_expression_instruction == "^[.*]", "Not expected value"

def test_regex_expression_instruction_is_none():
    """
    Testing get default output name
    """
    var = MockOperationBase(None, None)
    assert var.regex_expression_instruction == "", "Not expected value"

def test_delete_instruction():
    """
    Testing get delete instruction
    """
    test_instructions = {
        "Delete": "True"
    }

    var = MockOperationBase(None, test_instructions)
    assert var.delete_instruction, "Not expected value"

def test_delete_instruction_is_none():
    """
    Testing get delete instruction
    """
    var = MockOperationBase(None, None)
    assert not var.delete_instruction, "Not expected value"

def test_sort_type_instruction():
    """
    Testing get SortType
    """
    test_instructions = {
        "SortType": "High-Low"
    }

    var = MockOperationBase(None, test_instructions)
    assert var.sort_type_instruction == "High-Low", "Not expected value"

def test_sort_type_instruction_is_none():
    """
    Testing get default SortType
    """
    var = MockOperationBase(None, None)
    assert var.sort_type_instruction == "None", "Not expected value"
    