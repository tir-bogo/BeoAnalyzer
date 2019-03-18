"""
Module contains tests for ConvertFiles class
"""
import tarfile
from pathlib import Path
import pytest
from logfile.operations.types.unzip_files import UnzipFiles

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

    main_test_file = main_dir / "text.txt"
    main_file1 = main_dir / "file1.tgz"

    sub_dir = main_dir / "sub"
    sub_file1 = sub_dir / "file1.tgz"

    main_dir.mkdir()
    sub_dir.mkdir()

    main_test_file.write_text("test")

    # Pack single
    temp_file = (main_dir / "tmpfile.tgz")
    tar = tarfile.open(temp_file.as_posix(), "w:gz")
    tar.add(main_test_file.as_posix(), arcname=main_test_file.name)
    tar.close()

    # Pack double
    tar = tarfile.open(main_file1.as_posix(), "w:gz")
    tar.add(temp_file.as_posix(), arcname=temp_file.name)
    tar.close()

    # Sub dir
    tar = tarfile.open(sub_file1.as_posix(), "w:gz")
    tar.add(main_test_file.as_posix(), arcname=main_test_file.name)
    tar.close()

    Path(temp_file).unlink()

    return {
        "main": {
            "dir": main_dir,
            "file1": main_file1,
            "testfile": main_test_file
        },
        "sub": {
            "dir": sub_dir,
            "file1": sub_file1
        },
        "results":{
            "main":{
                "file" : main_dir / main_file1.stem / temp_file.stem / main_test_file.name,
                "tmpfile": main_dir / main_file1.stem / temp_file.name
            },
            "sub":{
                "file": sub_dir / sub_file1.stem / main_test_file.name
            }

        }
    }
def test_none_workfolder():
    """
    Testing run returns false when no valid workfolder is given
    """
    instructions = {
        "Directory":"*",
        "Recursive": "true",
        }
    var = UnzipFiles()
    var.instructions = instructions
    run_is_success = var.run()

    assert not run_is_success, "This should not be able to run"

def test_none_instructions():
    """
    Testing run returns false when no valid workfolder is given
    """
    var = UnzipFiles()
    var.workfolder = "*"
    run_is_success = var.run()

    assert not run_is_success, "This should not be able to run"

def test_run_recursive(file_system):
    """
    Testing run recursive
    """
    instructions = {
        "Directory":"*",
        "Recursive": "true",
        }
    var = UnzipFiles()
    var.instructions = instructions
    var.workfolder = file_system["main"]["dir"].as_posix()
    run_is_success = var.run()

    # Validate run is successful
    assert run_is_success, "This should be able to run"

    # Validate old file exists
    assert file_system["sub"]["file1"].exists(), "Sub file got deleted"

    # Validate unpack success
    assert file_system["results"]["main"]["file"].exists(), "File is not extracted correct"

def test_run_not_recursive(file_system):
    """
    Testing run recursive
    """
    instructions = {
        "Directory":"*",
        "Recursive": "false",
        }
    var = UnzipFiles()
    var.instructions = instructions
    var.workfolder = file_system["main"]["dir"].as_posix()
    run_is_success = var.run()

    # Validate run is successful
    assert run_is_success, "This should be able to run"

    # Validate old file exists
    assert file_system["sub"]["file1"].exists(), "Sub file got deleted"

    # Validate unpack success
    assert file_system["results"]["main"]["tmpfile"].exists(), "File is not extracted correct"

def test_run_sub(file_system):
    """
    Testing run recursive
    """
    instructions = {
        "Directory":"sub",
        "Recursive": "true",
        }
    var = UnzipFiles()
    var.instructions = instructions
    var.workfolder = file_system["main"]["dir"].as_posix()
    run_is_success = var.run()

    # Validate run is successful
    assert run_is_success, "This should be able to run"

    # Validate old file exists
    assert file_system["main"]["file1"].exists(), "Main text file got deleted"

    # Validate unpack success
    assert file_system["results"]["sub"]["file"].exists(), "File is not extracted correct"
    