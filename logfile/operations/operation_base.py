"""
Module contains a base class for file operations
"""
import abc
import logging
from pathlib import Path

class OperationBase(metaclass=abc.ABCMeta):
    """
    Base class for sharing methods across file operations
    """
    def __init__(self, workfolder: str, instructions: dict):
        self._workfolder = workfolder
        self._instructions = instructions
        if not self._instructions:
            logging.warning("Instructions is set to None, setting it to empty dict")
            self._instructions = {}

    @property
    def directory_instruction(self) -> str:
        """
        Get directory from instructions

        Returns:
            str: Directory

        Raises:
            TypeError: self._instructions is None
        """
        directory_key = "Directory"
        if directory_key in self._instructions:
            return self._instructions[directory_key]

        logging.info("Directory instruction not set, return current directory")
        return "*"

    @property
    def recursive_instruction(self) -> bool:
        """
        Get recursive instruction from instructions

        Returns:
            bool: Recursive behavior enabled

        Raises:
            TypeError: self.instructions is None
        """
        recursive_key = "Recursive"
        if recursive_key in self._instructions:
            val = self._instructions[recursive_key].lower()
            return val == "true"

        logging.info("Recursive instruction not set, return False")
        return False

    @property
    def exclude_files_instruction(self) -> list:
        """
        Get file names to exclude from instructions

        Returns:
            List<string>: Values to exclude

        Raises:
            TypeError: self.instructions is None
        """
        exclude_files_key = "ExcludeFiles"
        if exclude_files_key in self._instructions:
            value = self._instructions[exclude_files_key]
            return value.split('|')

        logging.info("ExcludeFiles instruction not set, return empty list")
        return []

    @property
    def exclude_extensions_instruction(self) -> list:
        """
        Get file extensions to exclude from instructions

        Returns:
            List<string>: Values to exclude

        Raises:
            TypeError: self.instructions is None
        """
        exclude_extensions_key = "ExcludeExtensions"
        if exclude_extensions_key in self._instructions:
            value = self._instructions[exclude_extensions_key]
            return value.split('|')

        logging.info("ExcludeFiles instruction not set, return empty list")
        return []

    @property
    def new_file_extension_instruction(self) -> str:
        """
        Get new extension from instructions

        Returns:
            str: New extension

        Raises:
            TypeError: self.instructions is None
        """
        new_file_extension_key = "NewFileExtension"
        if new_file_extension_key in self._instructions:
            return self._instructions[new_file_extension_key]

        logging.info("NewFileExtension instruction not set, return '.log' extension")
        return ".log"

    def make_directory_path(self, relative_path: str) -> str:
        """
        """
        if self._workfolder:
            result = Path(self._workfolder)
            if relative_path and relative_path != "*":
                return (result / relative_path).as_posix()
            return result.as_posix()
        return ""

    @staticmethod
    def get_files(directory: str, recursive: bool) -> list:
        """
        """
        if not directory:
            return []

        path = Path(directory)
        if recursive:
            return list(str(x) for x in path.glob("**/*.*") if x.is_file())

        return list(str(x) for x in path.iterdir() if x.is_file())


    @staticmethod
    def get_directories(directory: str, recursive: bool) -> bool:
        """
        """
        if not directory:
            return []

        path = Path(directory)
        if recursive:
            return [str(x) for x in path.glob("*/**") if x.is_dir()]
        
        if path.exists():
            return [str(x) for x in path.iterdir() if x.is_dir()]
        return []

    @abc.abstractmethod
    def run(self) -> bool:
        """
        Running the file operation

        Returns:
            bool: True run success, False run failed

        Raises:
            NotImplementedError: Must be implemented to use this base class
        """
        raise NotImplementedError("run must be defined")
