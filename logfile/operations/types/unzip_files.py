"""
Module contains file operation to unzip files
"""

import gzip
import tarfile
import logging
from typing import Optional
from pathlib import Path
from logfile.operations.operation_base import OperationBase

# pylint: disable=W1203
# pylint: disable=no-else-return

class UnzipFiles(OperationBase):
    """
    This class is responseable for unzipping files

    Instructions:
        Directory(str):
            Relative path in work folder or * for current work folder
        Recursive(str):
            False takes current folder, true is recursive through current folder and subs
    """
    @staticmethod
    def extract_tar(filepath: str) -> Optional[str]:
        """
        Extracting tar file

        Args:
            filepath(str): Filepath to tar file

        Returns:
            str: Directory extracted in
        """
        try:
            filepath = Path(filepath)

            extract_to = filepath.parent / filepath.stem
            extract_to.mkdir()

            filepath = filepath.as_posix()
            extract_to = extract_to.as_posix()
            logging.debug(f"Extracting '{filepath}' to '{extract_to}'")

            tar = tarfile.open(filepath)
            tar.extractall(extract_to)
            tar.close()

            logging.debug("Deleting file '{filepath}'")
            Path(filepath).unlink()

            return extract_to

        except OSError as exc:
            logging.warning(f"Error while extracting file '{filepath}' {exc}")

    @staticmethod
    def extract_gz(filepath: str) -> None:
        """
        Extract gz file

        Args:
            filepath(str): Filepath to gz file
        """
        try:
            filepath = Path(filepath)
            extract_to = filepath.parent
            filepath = filepath.as_posix()

            logging.debug(f"Extracting '{filepath}' to '{extract_to}'")
            gzfile = gzip.open(filepath)
            output = open(extract_to, "wb")
            output.write(gzfile.read())
            gzfile.close()
            output.close()

            Path(filepath).unlink()
            logging.debug("Deleted file '{filepath}'")

        except OSError as exc:
            logging.warning(f"Error while extracting file '{filepath}' {exc}")

    @staticmethod
    def extract_file(filepath: str) -> Optional[str]:
        """
        Extracting tar or gz file

        Args:
            filepath(str): Filepath to compressed file
        Returns:
            str: Directory where files are extracted to if there is created a new directory
        """
        ext = Path(filepath).suffix.lower()
        if ext in [".tgz", ".tar"]:
            return UnzipFiles.extract_tar(filepath)
        elif ext == ".gz":
            UnzipFiles.extract_gz(filepath)
        return None

    @staticmethod
    def extract(filepath: str, recursive: bool) -> None:
        """
        Extract compressed file

        Args:
            filepath(str): Filepath to compressed file
            Recursive(bool): Walk through tree and compress files inside
        """
        new_dir = UnzipFiles.extract_file(filepath)

        if recursive and new_dir:
            filepaths = list(x for x in Path(new_dir).glob("**/*.*") if x.is_file())
            for filep in filepaths:
                UnzipFiles.extract(filep, recursive)

    def run(self) -> bool:
        """
        Extracting files inside directory with given instructions
        """
        try:
            directory = self._directory_instruction
            recursive = self._recursive_instruction

            # Dont enable recursive for this, as we want to only get files from current dir
            files_in_directory = self._get_files(directory, False)
            for filepath in files_in_directory:
                UnzipFiles.extract(filepath, recursive)
            return True

        except TypeError as exc:
            logging.warning(f"Instructions is '{self.instructions}' {exc}")

        except OSError as exc:
            logging.warning(f"Invalid relative path '{directory}' {exc}")

        return False
