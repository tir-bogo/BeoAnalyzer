"""
Module contains a base class for file operations
"""
import abc
from pathlib import Path

class OperationBase(metaclass=abc.ABCMeta):
    """
    Base class for sharing methods across file operations
    """

    def __init__(self):
        self._workfolder = None
        self._instructions = None

    @property
    def workfolder(self) -> str:
        """
        Get workfolder

        Returns:
            str: workfolder
        """
        return self._workfolder

    @workfolder.setter
    def workfolder(self, workfolder: str) -> None:
        """
        Set workfolder

        Args:
            workfolder (str): New workfolder path to operate from
        """
        self._workfolder = workfolder

    @property
    def instructions(self) -> dict:
        """
        Get instructions

        Returns:
            dict: instructions for file operation
        """
        return self._instructions

    @instructions.setter
    def instructions(self, instructions: dict) -> None:
        """
        Set instructions

        Args:
            instruction(dict): Instructions for file operation
        """
        self._instructions = instructions

    @property
    def _exclude_files_instruction(self) -> list:
        """
        Get file names to exclude from instructions

        Returns:
            List<string>: Values to exclude

        Raises:
            TypeError: self.instructions is None
        """
        exclude_files_key = "ExcludeFiles"
        if exclude_files_key in self.instructions:
            value = self.instructions[exclude_files_key]
            return value.split('|')
        return []

    @property
    def _exclude_extensions_instruction(self) -> list:
        """
        Get file extensions to exclude from instructions

        Returns:
            List<string>: Values to exclude

        Raises:
            TypeError: self.instructions is None
        """
        exclude_extensions_key = "ExcludeExtensions"
        if exclude_extensions_key in self.instructions:
            value = self.instructions[exclude_extensions_key]
            return value.split('|')
        return []

    @property
    def _recursive_instruction(self) -> bool:
        """
        Get recursive instruction from instructions

        Returns:
            bool: Recursive behavior enabled

        Raises:
            TypeError: self.instructions is None
        """
        recursive_key = "Recursive"
        if recursive_key in self.instructions:
            val = self.instructions[recursive_key].lower()
            return val == "true"
        return False

    @property
    def _directory_instruction(self) -> str:
        """
        Get directory from instructions

        Returns:
            str: Directory

        Raises:
            TypeError: self.instructions is None
        """
        directory_key = "Directory"
        if directory_key in self.instructions:
            return self.instructions[directory_key]
        return "*"

    @property
    def _new_file_extension_instruction(self) -> str:
        """
        Get new extension from instructions

        Returns:
            str: New extension

        Raises:
            TypeError: self.instructions is None
        """
        new_file_extension_key = "NewFileExtension"
        if new_file_extension_key in self.instructions:
            return self.instructions[new_file_extension_key]
        return ""

    def _get_files(self, relative_filepath: str, recursive: bool) -> list:
        """
        Get files from directory

        Args:
            relative_filepath(str): Relative file path to workfolder or * for current
            recursive(bool): Enable recursive behavior

        Returns:
            List<string>: Filepaths for files found
        """
        path = None
        if relative_filepath == "*":
            path = Path(self.workfolder)
        else:
            path = Path(self.workfolder, relative_filepath)

        result = []
        if recursive:
            result = list(x for x in path.glob("**/*.*") if x.is_file())

        else:
            result = list(x for x in path.iterdir() if x.is_file())

        return [str(x) for x in result]

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
