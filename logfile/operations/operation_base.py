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
        self.__workfolder = None
        self.__instructions = None

        self._directory_instruction_key = "Directory"
        self._recursive_instruction_key = "Recursive"
        self._new_file_extension_instruction_key = "NewFileExtension"
        self._exclude_files_instruction_key = "ExcludeFiles"
        self._exclude_extensions_instruction_key = "ExcludeExtensions"

    @property
    def workfolder(self):
        """
        Get workfolder

        Returns:
            str: workfolder
        """
        return self.__workfolder

    @workfolder.setter
    def workfolder(self, workfolder):
        """
        Set workfolder

        Args:
            workfolder (str): New workfolder path to operate from
        """
        self.__workfolder = workfolder

    @property
    def instructions(self):
        """
        Get instructions

        Returns:
            dict: instructions for file operation
        """
        return self.__instructions

    @instructions.setter
    def instructions(self, instructions):
        """
        Set instructions

        Args:
            instruction(dict): Instructions for file operation
        """
        self.__instructions = instructions

    def _get_exclude_files_instruction(self):
        """
        Get file names to exclude from instructions

        Returns:
            List<string>: Values to exclude
            None
        """
        if self._exclude_files_instruction_key in self.instructions:
            value = self.instructions[self._exclude_files_instruction_key]
            return value.split('|')
        return []

    def _get_exclude_extensions_instruction(self):
        """
        Get file extensions to exclude from instructions

        Returns:
            List<string>: Values to exclude
            None
        """
        if self._exclude_extensions_instruction_key in self.instructions:
            value = self.instructions[self._exclude_extensions_instruction_key]
            return value.split('|')
        return []

    def _get_recursive_instruction(self):
        """
        Get recursive instruction from instructions

        Returns:
            bool: Recursive behavior enabled
        """
        val = self.instructions[self._recursive_instruction_key].lower()
        return val == "true"

    def _get_directory_instruction(self):
        """
        Get directory from instructions

        Returns:
            str: Directory
        """
        return self.instructions[self._directory_instruction_key]

    def _get_new_file_extension_instruction(self):
        """
        Get new extension from instructions

        Returns:
            str: New extension
        """
        return self.instructions[self._new_file_extension_instruction_key]

    def _get_files(self, relative_filepath, recursive):
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
    def instructions_is_valid(self):
        """
        Checking if instructions is valid

        Returns:
            bool: True instructions is valid, False instructions is NOT valid

        Raises:
            NotImplementedError: Must be implemented to use this base class
        """
        raise NotImplementedError("instructions_is_valid must be defined to use OperationBase class")

    @abc.abstractmethod
    def run(self):
        """
        Running the file operation

        Returns:
            bool: True run success, False run failed

        Raises:
            NotImplementedError: Must be implemented to use this base class
        """
        raise NotImplementedError("run must be defined to use OperationBase class")
