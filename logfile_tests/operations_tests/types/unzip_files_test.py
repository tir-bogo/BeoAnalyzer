"""
Module contains tests for ConvertFiles class
"""
import tarfile
import gzip
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
    main_file2 = main_dir / "file2.txt.gz"
    main_gz_corrupted_file = main_dir / "file2.gz"
    main_tgz_corrupted_file = main_dir / "file2.tgz"

    sub_dir = main_dir / "sub"
    sub_file1 = sub_dir / "file1.tgz"

    main_dir.mkdir()
    sub_dir.mkdir()

    main_test_file.write_text("test")
    main_gz_corrupted_file.write_text("I am corrupted")
    main_tgz_corrupted_file.write_text("I am corrupted")

    # Create gz file
    main_test_file_path = main_test_file.as_posix()
    main_file2_path = main_file2.as_posix()
    with open(main_test_file_path, 'rb') as f_in, gzip.open(main_file2_path, 'wb') as f_out:
        f_out.writelines(f_in)

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
            "file2": main_file2,
            "testfile": main_test_file,
            "corrupted_gz": main_gz_corrupted_file,
            "corrupted_tgz": main_tgz_corrupted_file
        },
        "sub": {
            "dir": sub_dir,
            "file1": sub_file1
        },
        "results":{
            "main":{
                "file1" : main_dir / main_file1.stem / temp_file.stem / main_test_file.name,
                "file2": main_dir / main_file2.stem,
                "tmpfile": main_dir / main_file1.stem / temp_file.name
            },
            "sub":{
                "file": sub_dir / sub_file1.stem / main_test_file.name
            }
        }
    }

def test_extract_tar(file_system):
    """
    Testing file can be extracted
    """
    target = file_system["main"]["file1"].as_posix()
    result = UnzipFiles.extract_tar(target)
    expected_dir = (file_system["main"]["dir"] / file_system["main"]["file1"].stem).as_posix()

    assert result == expected_dir, "Not expected return"
    assert file_system["results"]["main"]["tmpfile"].exists()

def test_extract_tar_corrupted_file(file_system):
    """
    Test tar_extract returns None if file is corrupted
    """
    target = file_system["main"]["corrupted_gz"].as_posix()
    result = UnzipFiles.extract_tar(target)
    assert not result, "Not expected return"

def test_extract_tar_arg_none():
    """
    Test tar_extract returns None if arg is none
    """
    target = None
    result = UnzipFiles.extract_tar(target)
    assert not result, "Not expected return"

def test_extract_tar_invalid_path():
    """
    Test tar_extract returns None if filepath is invalid
    """
    target = "invalid/path/test.tar"
    result = UnzipFiles.extract_tar(target)
    assert not result, "Not expected return"

def test_extract_gz(file_system):
    """
    Testing can extract gz file
    """
    target = file_system["main"]["file2"].as_posix()
    result = UnzipFiles.extract_gz(target)

    assert result, "Not expected return"
    assert file_system["results"]["main"]["file2"].exists()

def test_extract_gz_corrupted_file(file_system):
    """
    Testing returns false if gz is corrupted
    """
    target = file_system["main"]["corrupted_gz"].as_posix()
    result = UnzipFiles.extract_gz(target)
    assert not result, "Not expected return"

def test_extract_gz_arg_none():
    """
    Testing returns false if filepath is none
    """
    target = None
    result = UnzipFiles.extract_gz(target)
    assert not result, "Not expected return"

def test_extract_gz_invalid_path():
    """
    Testing returns false if filepath is invalid
    """
    target = "Invalid/path/test.txt.gz"
    result = UnzipFiles.extract_gz(target)
    assert not result, "Not expected return"

def test_extract_arg_none():
    """
    Testing extract dont raise Exception if arg is None
    """
    UnzipFiles.extract(None, True)

def test_extract_invalid_path():
    """
    Testing extract dont raise Exception if arg is invalid
    """
    UnzipFiles.extract("Invalid/path/", True)

def test_extract_recursive(file_system):
    """
    Test extract can walk tree and extract
    """
    target = file_system["main"]["file1"]
    UnzipFiles.extract(target, True)
    assert file_system["results"]["main"]["file1"].exists()

def test_extract_not_recursive(file_system):
    """
    Testing extract can run not recursive
    """
    target = file_system["main"]["file1"]
    UnzipFiles.extract(target, False)
    assert file_system["results"]["main"]["tmpfile"].exists()

def test_run_workfolder_none():
    """
    Testing run returns false if workfolder is none
    """
    instructions = {
        "Directory": "*",
        "Recursive": "False"
    }
    var = UnzipFiles(None, instructions)
    assert not var.run(), "Not expected return"

def test_run_workfolder_invalid():
    """
    Testing run returns false if workfolder is none
    """
    instructions = {
        "Directory": "*",
        "Recursive": "False"
    }
    var = UnzipFiles("invalid/path", instructions)
    assert not var.run(), "Not expected return"

def test_run_instructions_none(file_system):
    """
    Testing use of default values if instructions is none
    """
    workfolder = file_system["main"]["dir"]
    var = UnzipFiles(workfolder, None)
    assert var.run(), "Not expected return"
    