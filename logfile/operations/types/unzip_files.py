"""
Module contains file operation to unzip files
"""

import gzip
import tarfile
import logging
from pathlib import Path
from logfile.operations.operation_base import OperationBase

# pylint: disable=W1203


class UnzipFiles(OperationBase):
    """
    This class is responseable for unzipping files

    Instructions:
        Directory(str):
            Relative path in work folder or * for current work folder
        Recursive(str):
            False takes current folder
            true is recursive through current folder and subs
    """
    @staticmethod
    def extract_tar(filepath: str) -> str:
        """
        Extracting tar file

        Args:
            filepath(str): Filepath to tar file

        Returns:
            str: Directory extracted in
            None: Tar extracting failed
        """
        if filepath and Path(filepath).exists():
            filepath = Path(filepath)
            extract_to = filepath.parent / filepath.stem

            filepath = filepath.as_posix()
            extract_to = extract_to.as_posix()

            try:
                logging.debug(f"Create directory '{extract_to}'")
                Path(extract_to).mkdir()

                logging.debug(f"Extracting '{filepath}' to '{extract_to}'")
                tar = tarfile.open(filepath)
                tar.extractall(extract_to)
                tar.close()

                logging.debug("Deleting file '{filepath}'")
                Path(filepath).unlink()

                return extract_to

            except tarfile.ReadError as exc:
                logging.warning(f"File is corrupted '{filepath}' {exc}")

            except OSError as exc:
                logging.warning(f"Could not delete '{filepath}' {exc}")

        return None

    @staticmethod
    def extract_gz(filepath: str) -> bool:
        """
        Extract gz file

        Args:
            filepath(str): Filepath to gz file

        Returns:
            bool: Gz extract success
        """
        if filepath and Path(filepath).exists():
            filepath = Path(filepath)
            extract_to = (filepath.parent / filepath.stem).as_posix()
            filepath = filepath.as_posix()

            try:
                logging.debug(f"Extracting '{filepath}' to '{extract_to}'")
                gzfile = gzip.open(filepath)
                output = open(extract_to, "wb")
                output.write(gzfile.read())
                gzfile.close()
                output.close()

                logging.debug(f"Deleted file '{filepath}'")
                Path(filepath).unlink()
                return True

            except OSError as exc:
                logging.warning(f"Error extracting file '{filepath}' {exc}")

        return False

    @staticmethod
    def extract(filepath: str, recursive: bool) -> None:
        """
        Extract compressed file

        Args:
            filepath(str): Filepath to compressed file
            Recursive(bool): Walk through tree and compress files inside
        """
        new_dir = None
        if filepath:
            ext = Path(filepath).suffix.lower()
            if ext in [".tgz", ".tar"]:
                new_dir = UnzipFiles.extract_tar(filepath)
            elif ext == ".gz":
                UnzipFiles.extract_gz(filepath)

        if recursive and new_dir:
            filepaths = OperationBase.get_files(new_dir, True)
            for filep in filepaths:
                UnzipFiles.extract(filep, recursive)

    def run(self) -> bool:
        """
        Extracting files inside directory with given instructions
        """
        directory = self.directory_instruction
        recursive = self.recursive_instruction

        directory_path = self.make_directory_path(directory)
        files_in_directory = self.get_files(directory_path, False)

        if files_in_directory != []:
            for filepath in files_in_directory:
                UnzipFiles.extract(filepath, recursive)

            self._log_run_success()
            return True

        self._log_run_failed("No files affected")
        return False
