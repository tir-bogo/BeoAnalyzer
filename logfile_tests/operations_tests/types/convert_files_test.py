"""
Module contains tests for ConvertFiles class
"""
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

def test_config_is_valid_true():
    """
    Testing configuration is valid returns true when a correct configuration is used
    """
    config = {
        "Directory":"*",
        "Recursive": "true",
        "NewFileExtension": ".log"
        }
    var = ConvertFiles()
    var.config = config
    assert var.config_is_valid(), "This is a valid configuration"

def test_config_is_valid_false():
    """
    Testing configuration is valid returns false when a incorrect configuration is used
    """
    config = {
        "Directory":"*",
        "Recursive": "true"
        }
    var = ConvertFiles()
    var.config = config
    assert not var.config_is_valid(), "This is NOT a valid configuration"
def test_run_recursive(file_system):
    """
    Testing Operation can run recursive
    """
    config = {
        "Directory":"*",
        "Recursive": "true",
        "NewFileExtension": ".log"
        }
    var = ConvertFiles()
    var.config = config
    var.workfolder = str(file_system["main"]["dir"])
    var.run()

    # Validate old files are deleted
    assert not file_system["main"]["file1"].exists(), "Main file 1 did not get deleted"
    assert not file_system["main"]["file2"].exists(), "Main file 2 did not get deleted"
    assert not file_system["main"]["file3"].exists(), "Main file 3 did not get deleted"

    assert not file_system["sub"]["file1"].exists(), "Sub file 1 did not get deleted"
    assert not file_system["sub"]["file2"].exists(), "Sub file 2 did not get deleted"
    assert not file_system["sub"]["file3"].exists(), "Sub file 3 did not get deleted"

    # Validate new files are created
    main_file1 = file_system["main"]["file1"].parent / (file_system["main"]["file1"].name + ".log")
    assert main_file1.exists(), "Main file 1 did not get converted"

    main_file2 = file_system["main"]["file2"].parent / (file_system["main"]["file2"].name + ".log")
    assert main_file2.exists(), "Main file 2 did not get converted"

    main_file3 = file_system["main"]["file3"].parent / (file_system["main"]["file3"].name + ".log")
    assert main_file3.exists(), "Main file 3 did not get converted"

    sub_file1 = file_system["sub"]["file1"].parent / (file_system["sub"]["file1"].name + ".log")
    assert sub_file1.exists(), "Sub file 1 did not get converted"

    sub_file2 = file_system["sub"]["file2"].parent / (file_system["sub"]["file2"].name + ".log")
    assert sub_file2.exists(), "Sub file 2 did not get converted"

    sub_file3 = file_system["sub"]["file3"].parent / (file_system["sub"]["file3"].name + ".log")
    assert sub_file3.exists(), "Sub file 3 did not get converted"

def test_run_not_recursive(file_system):
    """
    Testing without recursive
    """
    config = {
        "Directory":"*",
        "Recursive": "false",
        "NewFileExtension": ".log"
        }
    var = ConvertFiles()
    var.config = config
    var.workfolder = str(file_system["main"]["dir"])
    var.run()

    # Validate old files are deleted
    assert not file_system["main"]["file1"].exists(), "Main file 1 did not get deleted"
    assert not file_system["main"]["file2"].exists(), "Main file 2 did not get deleted"
    assert not file_system["main"]["file3"].exists(), "Main file 3 did not get deleted"

    # Validate sub files are not deleted
    assert file_system["sub"]["file1"].exists(), "Sub file 1 did get deleted"
    assert file_system["sub"]["file2"].exists(), "Sub file 2 did get deleted"
    assert file_system["sub"]["file3"].exists(), "Sub file 3 did get deleted"

    # Validate new files
    main_file1 = file_system["main"]["file1"].parent / (file_system["main"]["file1"].name + ".log")
    assert main_file1.exists(), "Main file 1 did not get converted"

    main_file2 = file_system["main"]["file2"].parent / (file_system["main"]["file2"].name + ".log")
    assert main_file2.exists(), "Main file 2 did not get converted"

    main_file3 = file_system["main"]["file3"].parent / (file_system["main"]["file3"].name + ".log")
    assert main_file3.exists(), "Main file 3 did not get converted"

def test_run_exclude_file(file_system):
    """
    Testing exclude files are working
    """
    config = {
        "Directory":"*",
        "Recursive": "false",
        "NewFileExtension": ".log",
        "ExcludeFiles":"file1.txt|file2.log"
        }
    var = ConvertFiles()
    var.config = config
    var.workfolder = str(file_system["main"]["dir"])
    var.run()

    # Validate old file is deleted
    assert not file_system["main"]["file3"].exists(), "Main file 3 did not get deleted"

    # Validate files is not deleted
    assert file_system["main"]["file1"].exists(), "Main file 1 did get deleted"
    assert file_system["main"]["file2"].exists(), "Main file 2 did get deleted"

    # Validate new file exists
    main_file3 = file_system["main"]["file3"].parent / (file_system["main"]["file3"].name + ".log")
    assert main_file3.exists(), "Main file 3 did not get converted"

def test_run_exclude_extension(file_system):
    """
    Testing exclude extension are working
    """
    config = {
        "Directory":"*",
        "Recursive": "false",
        "NewFileExtension": ".log",
        "ExcludeExtensions":".log"
        }
    var = ConvertFiles()
    var.config = config
    var.workfolder = str(file_system["main"]["dir"])
    var.run()

    # Validate old file is deleted
    assert not file_system["main"]["file1"].exists(), "Main file 1 did not get deleted"
    assert not file_system["main"]["file3"].exists(), "Main file 3 did not get deleted"

    # Validate file is not deleted
    assert file_system["main"]["file2"].exists(), "Main file 2 did get deleted"

    # Validate new file exists
    main_file3 = file_system["main"]["file3"].parent / (file_system["main"]["file3"].name + ".log")
    assert main_file3.exists(), "Main file 3 did not get converted"

    main_file1 = file_system["main"]["file1"].parent / (file_system["main"]["file1"].name + ".log")
    assert main_file1.exists(), "Main file 1 did not get converted"

def test_run_relative_dir(file_system):
    """
    Testing relative path is working
    """
    config = {
        "Directory":"sub",
        "Recursive": "false",
        "NewFileExtension": ".log"
        }
    var = ConvertFiles()
    var.config = config
    var.workfolder = str(file_system["main"]["dir"])
    var.run()

    # Validate main files is not deleted
    assert file_system["main"]["file1"].exists(), "Main file 1 did get deleted"
    assert file_system["main"]["file2"].exists(), "Main file 2 did get deleted"
    assert file_system["main"]["file3"].exists(), "Main file 3 did get deleted"

    # Validate sub files are deleted
    assert not file_system["sub"]["file1"].exists(), "Sub file 1 did not get deleted"
    assert not file_system["sub"]["file2"].exists(), "Sub file 2 did not get deleted"
    assert not file_system["sub"]["file3"].exists(), "Sub file 3 did not get deleted"

    # Validate sub files are converted
    sub_file1 = file_system["sub"]["file1"].parent / (file_system["sub"]["file1"].name + ".log")
    assert sub_file1.exists(), "Sub file 1 did not get converted"

    sub_file2 = file_system["sub"]["file2"].parent / (file_system["sub"]["file2"].name + ".log")
    assert sub_file2.exists(), "Sub file 2 did not get converted"

    sub_file3 = file_system["sub"]["file3"].parent / (file_system["sub"]["file3"].name + ".log")
    assert sub_file3.exists(), "Sub file 3 did not get converted"
