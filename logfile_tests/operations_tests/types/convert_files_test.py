"""
Module contains tests for ConvertFiles class
"""
from pathlib import Path
import pytest
from logfile.operations.types.convert_files import ConvertFiles

# pylint: disable=redefined-outer-name

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
    main_file2 = main_dir / "file2.log"
    main_file3 = main_dir / "file3.txt"

    sub_dir = main_dir / "sub"
    sub_file1 = sub_dir / "file1.txt"
    sub_file2 = sub_dir / "file2.log"
    sub_file3 = sub_dir / "file3.txt"

    file_content = "test"

    main_dir.mkdir()
    sub_dir.mkdir()

    main_file1.write_text(file_content)
    main_file2.write_text(file_content)
    main_file3.write_text(file_content)

    sub_file1.write_text(file_content)
    sub_file2.write_text(file_content)
    sub_file3.write_text(file_content)

    return {
        "main": {
            "dir": main_dir,
            "file1": main_file1,
            "file2": main_file2,
            "file3": main_file3
        },
        "sub": {
            "dir": sub_dir,
            "file1": sub_file1,
            "file2": sub_file2,
            "file3": sub_file3
        }
    }

def test_list_item_in_string_match():
    """
    Testing correct return for list_item_in_string
    """
    test_item = "c:/test/path/file.txt"
    test_arr = [".txt", ".log", ".exe"]
    assert ConvertFiles.list_item_in_string(test_arr, test_item), "Expected to be found"

def test_list_item_in_string_no_match():
    """
    Testing correct return for list_item_in_string
    """
    test_item = "c:/test/path/file.txt"
    test_arr = [".log", ".exe"]
    assert not ConvertFiles.list_item_in_string(test_arr, test_item), "Expected not to be found"

def test_list_item_in_string_arg_item_none():
    """
    Testing correct return for list_item_in_string
    """
    test_arr = [".log", ".exe"]
    assert not ConvertFiles.list_item_in_string(test_arr, None), "Expected not to be found"

def test_list_item_in_string_arg_arr_none():
    """
    Testing correct return for list_item_in_string
    """
    test_item = "c:/test/path/file.txt"
    assert not ConvertFiles.list_item_in_string(None, test_item), "Expected not to be found"

def test_convert_file(file_system):
    """
    Testing convert_file can convert file
    """
    filepath = file_system["main"]["file1"].as_posix()
    result = ConvertFiles.convert_file(filepath, ".log")
    main_file1 = file_system["main"]["file1"].parent / (file_system["main"]["file1"].name + ".log")

    assert result, "This should be able to run"
    assert main_file1.exists(), "File is not converted correct"

def test_convert_file_do_not_exists():
    """
    Testing convert_file returns False when file dont exists
    """
    result = ConvertFiles.convert_file("path/invalid/test.txt", ".log")
    assert not result, "Cant convert that do not exists"

def test_convert_file_arg_filepath_none():
    """
    Testing convert_file returns False arg is none
    """
    result = ConvertFiles.convert_file(None, ".log")
    assert not result, "Cant convert that do not exists"

def test_convert_file_arg_new_extension_none(file_system):
    """
    Testing convert_file returns False arg is none
    """
    filepath = file_system["main"]["file1"].as_posix()
    result = ConvertFiles.convert_file(filepath, None)
    assert not result, "Cant convert that do not have a new extension"

def test_sort_files_match():
    """
    Testing sort_files work as expected
    """
    test_filter = [".txt", ".exe"]
    test_filepaths = ["c:/test.txt", "c:/test2.exe", "c:/test3.log", "c:/test4.mov"]
    result = ConvertFiles.sort_files(test_filepaths, test_filter)
    assert len(result) == 2, "Expected 2 items"
    assert result[0] == test_filepaths[2], "Not expected string"
    assert result[1] == test_filepaths[3], "Not expected string"

def test_sort_files_no_match():
    """
    Testing sort_files work as expected
    """
    test_filter = [".dox", ".email"]
    test_filepaths = ["c:/test.txt", "c:/test2.exe", "c:/test3.log", "c:/test4.mov"]
    result = ConvertFiles.sort_files(test_filepaths, test_filter)
    assert len(result) == 4, "Expected 4 items"

def test_sort_files_arg_files_none():
    """
    Testing sort_files work as expected when arg is none
    """
    test_filter = [".dox", ".email"]
    result = ConvertFiles.sort_files(None, test_filter)
    assert result == [], "Expected 0 items"

def test_sort_files_arg_items_none():
    """
    Testing sort_files work as expected when arg is none
    """
    test_filepaths = ["c:/test.txt", "c:/test2.exe", "c:/test3.log", "c:/test4.mov"]
    result = ConvertFiles.sort_files(test_filepaths, None)
    assert len(result) == 4, "Expected 4 items"

def test_run_invalid_workfolder():
    """
    Testing run returns false when workfolder invalid
    """
    test_workfolder = None
    test_instructions = {
        "Directory" : "*",
        "Recursive" : "True",
        "NewExtension" : ".log"
    }
    var = ConvertFiles(test_workfolder, test_instructions)
    assert not var.run(), "This should return False"

def test_run_recursive(file_system):
    """
    Testing run can run recursively
    """
    test_workfolder = file_system["main"]["dir"]
    test_instructions = {
        "Directory" : "*",
        "Recursive" : "True",
        "NewExtension" : ".log"
    }
    var = ConvertFiles(test_workfolder, test_instructions)
    assert var.run(), "This should return True"

    main_file1 = Path(file_system["main"]["file1"].as_posix() + ".log")
    sub_file1 = Path(file_system["sub"]["file1"].as_posix() + ".log")

    assert main_file1.exists(), "This should exists"
    assert sub_file1.exists(), "This should exists"

def test_run_not_recursive(file_system):
    """
    Testing run can run not recursively
    """
    test_workfolder = file_system["main"]["dir"]
    test_instructions = {
        "Directory" : "*",
        "Recursive" : "False",
        "NewExtension" : ".log"
    }
    var = ConvertFiles(test_workfolder, test_instructions)
    assert var.run(), "This should return True"

    main_file1 = Path(file_system["main"]["file1"].as_posix() + ".log")
    sub_file1 = Path(file_system["sub"]["file1"].as_posix() + ".log")

    assert main_file1.exists(), "This should exists"
    assert not sub_file1.exists(), "This should not exists"

def test_run_instruction_none(file_system):
    """
    Testing default instructions is used when instructions is none
    """
    test_workfolder = file_system["main"]["dir"]
    test_instructions = None
    var = ConvertFiles(test_workfolder, test_instructions)

    assert var.run(), "This should return True"

    main_file1 = Path(file_system["main"]["file1"].as_posix() + ".log")
    main_file2 = Path(file_system["main"]["file2"].as_posix() + ".log")
    main_file3 = Path(file_system["main"]["file3"].as_posix() + ".log")

    assert main_file1.exists(), "This should exists"
    assert main_file2.exists(), "This should exists"
    assert main_file3.exists(), "This should exists"

def test_run_relative_dir(file_system):
    """
    Testing relative dir is working
    """
    test_workfolder = file_system["main"]["dir"]
    test_instructions = {
        "Directory" : "sub",
        "Recursive" : "False",
        "NewExtension" : ".log"
    }
    var = ConvertFiles(test_workfolder, test_instructions)
    assert var.run(), "This should return True"

    sub_file1 = Path(file_system["sub"]["file1"].as_posix() + ".log")
    assert sub_file1.exists(), "This should exists"

def test_run_exclude_extension(file_system):
    """
    Testing exclude extensions is working
    """
    test_workfolder = file_system["main"]["dir"]
    test_instructions = {
        "Directory" : "*",
        "Recursive" : "False",
        "NewExtension" : ".txt",
        "ExcludeExtensions" : ".log"
    }
    var = ConvertFiles(test_workfolder, test_instructions)
    assert var.run(), "This should return True"
    assert file_system["main"]["file2"].exists(), "This should exists"

def test_run_exclude_files(file_system):
    """
    Testing exclude files is working
    """
    test_workfolder = file_system["main"]["dir"]
    test_instructions = {
        "Directory" : "*",
        "Recursive" : "False",
        "NewExtension" : ".txt",
        "ExcludeFiles" : "file2.log"
    }
    var = ConvertFiles(test_workfolder, test_instructions)
    assert var.run(), "This should return True"
    assert file_system["main"]["file2"].exists(), "This should exists"
