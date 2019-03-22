"""
Module contains tests for MergeFiles
"""

import re
import pytest
from logfile.operations.types.merge_files import MergeFiles


@pytest.fixture
def file_system(tmp_path):
    """
    """
    main_dir = tmp_path / "main"
    main_file1 = main_dir / "file1.txt"
    main_file2 = main_dir / "file2.txt"
    main_file3 = main_dir / "file3.txt"

    sub_dir = main_dir / "main"
    sub_file1 = sub_dir / "file1.txt"
    sub_file2 = sub_dir / "file2.txt"
    sub_file3 = sub_dir / "file3.txt"

    main_dir.mkdir()
    sub_dir.mkdir()

    main_file1.write_text("1")
    main_file2.write_text("2")
    main_file3.write_text("3")

    sub_file1.write_text("1")
    sub_file2.write_text("2")
    sub_file3.write_text("3")

    return {
        "main": {
            "dir": main_dir,
            "file1": main_file1,
            "file2": main_file2,
            "file3": main_file3
        },
        "sub":{
            "dir": sub_dir,
            "file1": sub_file1,
            "file2": sub_file2,
            "file3": sub_file3
        }
    }

def test_match_files_with_regex():
    """
    Test return is only matched files
    """
    regex = re.compile(r".*(\d)")
    test_files = ["c:/test/path/test1.txt", "c:/test/path/test2.txt", "c:/test/path/message.txt"]
    files = MergeFiles.match_files_with_regex(test_files, regex)

    assert len(files) == 2
    assert files[0] == "c:/test/path/test1.txt"
    assert files[1] == "c:/test/path/test2.txt"

def test_match_files_with_regex_no_match():
    """
    """
    regex = re.compile(r"no match.*(\d)")
    test_files = ["c:/test/path/test1.txt", "c:/test/path/test2.txt", "c:/test/path/message.txt"]
    files = MergeFiles.match_files_with_regex(test_files, regex)
    assert not files

def test_match_files_with_regex_arg_files_none():
    """
    """
    regex = re.compile(r".*(\d)")
    files = MergeFiles.match_files_with_regex(None, regex)
    assert not files

def test_match_files_with_regex_arg_regex_none():
    """
    """
    test_files = ["c:/test/path/test1.txt", "c:/test/path/test2.txt", "c:/test/path/message.txt"]
    files = MergeFiles.match_files_with_regex(test_files, None)
    assert not files

def test_sort_files():
    """
    """
    regex = re.compile(r".*(\d)")
    test_files = ["c:/test/path/test2.txt", "c:/test/path/test3.txt", "c:/test/path/test1.txt"]
    sorted_files = MergeFiles.sort_files(test_files, regex)

    assert len(sorted_files) == 3
    assert sorted_files[0] == "c:/test/path/test1.txt"
    assert sorted_files[1] == "c:/test/path/test2.txt"
    assert sorted_files[2] == "c:/test/path/test3.txt"

def test_sort_files_no_regex_match():
    """
    """
    regex = re.compile(r"no match(\d)")
    test_files = ["c:/test/path/test2.txt", "c:/test/path/test3.txt", "c:/test/path/test1.txt"]
    sorted_files = MergeFiles.sort_files(test_files, regex)

    assert len(sorted_files) == 3
    assert sorted_files[0] == "c:/test/path/test2.txt"
    assert sorted_files[1] == "c:/test/path/test3.txt"
    assert sorted_files[2] == "c:/test/path/test1.txt"

def test_sort_files_arg_files_none():
    """
    """
    regex = re.compile(r"no match(\d)")
    sorted_files = MergeFiles.sort_files(None, regex)
    assert not sorted_files

def test_sort_files_arg_regex_none():
    """
    """
    test_files = ["c:/test/path/test2.txt", "c:/test/path/test3.txt", "c:/test/path/test1.txt"]
    sorted_files = MergeFiles.sort_files(test_files, None)

    assert len(sorted_files) == 3
    assert sorted_files[0] == "c:/test/path/test2.txt"
    assert sorted_files[1] == "c:/test/path/test3.txt"
    assert sorted_files[2] == "c:/test/path/test1.txt"

def test_merge_files(file_system):
    """
    """
    test_files = []
    test_files.append(file_system["main"]["file1"].as_posix())
    test_files.append(file_system["main"]["file2"].as_posix())
    test_files.append(file_system["main"]["file3"].as_posix())

    output_file = (file_system["main"]["dir"] / "output.txt").as_posix()

    ran_success = MergeFiles.merge_files(output_file, test_files)
    assert ran_success, "Expected to return True"

    result = []
    with open(output_file, 'r') as file_read:
        for line in file_read:
            result.append(line)

    expected_result = ["1\n", "2\n", "3\n"]
    assert result == expected_result

def test_merge_files_arg_new_filepath_none(file_system):
    """
    """
    test_files = []
    test_files.append(file_system["main"]["file1"].as_posix())
    test_files.append(file_system["main"]["file2"].as_posix())
    test_files.append(file_system["main"]["file3"].as_posix())

    ran_success = MergeFiles.merge_files(None, test_files)
    assert not ran_success, "Expected to return False"

def test_merge_files_arg_files_none(file_system):
    """
    """
    output_file = (file_system["main"]["dir"] / "output.txt").as_posix()
    ran_success = MergeFiles.merge_files(output_file, None)
    assert not ran_success, "Expected to return False"

def test_merge_files_invalid_files(file_system):
    """
    """
    test_files = ["invalid/test1.txt", "invalid/test2.txt"]
    output_file = (file_system["main"]["dir"] / "output.txt").as_posix()
    ran_success = MergeFiles.merge_files(output_file, test_files)
    assert not ran_success, "Expected to return False"

def test_merge_files_invalid_new_path(file_system):
    """
    """
    test_files = []
    test_files.append(file_system["main"]["file1"].as_posix())
    test_files.append(file_system["main"]["file2"].as_posix())
    test_files.append(file_system["main"]["file3"].as_posix())
    output_file = "Invalid/path.txt"
    ran_success = MergeFiles.merge_files(output_file, test_files)
    assert not ran_success, "Expected to return False"

def test_delete_files(file_system):
    """
    """
    test_files = []
    test_files.append(file_system["main"]["file1"].as_posix())
    test_files.append(file_system["main"]["file2"].as_posix())
    test_files.append(file_system["main"]["file3"].as_posix())

    ran_success = MergeFiles.delete_files(test_files)

    assert ran_success, "Expected to run successfully"
    assert not file_system["main"]["file1"].exists(), "Expected to be deleted"
    assert not file_system["main"]["file2"].exists(), "Expected to be deleted"
    assert not file_system["main"]["file3"].exists(), "Expected to be deleted"

def test_delete_files_arg_none():
    """
    """
    ran_success = MergeFiles.delete_files(None)
    assert not ran_success, "Expected False"

def test_delete_files_invalid_path():
    """
    """
    test_files = ["invalid/path/test.txt", "invalid/path/test2.txt"]
    ran_success = MergeFiles.delete_files(None)
    assert not ran_success, "Expected False"

def test_run_not_recursive():
    """
    """
    assert False, "Not implemented"
