"""
Module contains a base class for file operations
"""
import abc
import logging
from pathlib import Path
from typing import List, Dict

# pylint: disable=W1203


class OperationBase(metaclass=abc.ABCMeta):
    """
    Base class for sharing methods across file operations
    """
    def __init__(self, workfolder: str, instructions: Dict[str, str]):
        logging.info(f"Running FileOperation'{self.__class__.__name__}'")
        self._workfolder = workfolder
        self._instructions = instructions

        if not self._instructions:
            logging.warning(r"Instructions is set to None, set it to {}")
            self._instructions = {}

    @staticmethod
    def _log_instruction(instrution_key: str, instruction_value: str) -> None:
        """
        Logs instrution
        """
        logging.info(f"Instruction '{instrution_key}' = '{instruction_value}'")

    def _log_run_success(self) -> None:
        """
        Logs run is a success
        """
        logging.info(f"'{self.__class__.__name__}'Execution done successfully")

    def _log_run_failed(self, message: str) -> None:
        """
        """
        class_name = self.__class__.__name__
        logging.warning(f"'{class_name}'Execution Failed. {message}")

    @property
    def directory_instruction(self) -> str:
        """
        Get directory from instructions

        Returns:
            str: Directory

        Default value: '*'
        """
        directory_key = "Directory"
        val = "*"
        if directory_key in self._instructions:
            val = self._instructions[directory_key]

        self._log_instruction(directory_key, val)
        return val

    @property
    def recursive_instruction(self) -> bool:
        """
        Get recursive instruction from instructions

        Returns:
            bool: Recursive behavior enabled

        Default value: False
        """
        recursive_key = "Recursive"
        val = False
        if recursive_key in self._instructions:
            value_found = self._instructions[recursive_key].lower()
            val = (value_found == "true")
        self._log_instruction(recursive_key, str(val))
        return val

    @property
    def exclude_files_instruction(self) -> List[str]:
        """
        Get file names to exclude from instructions

        Returns:
            List<string>: Values to exclude

        Default value: []
        """
        exclude_files_key = "ExcludeFiles"
        val: List[str] = []
        if exclude_files_key in self._instructions:
            value = self._instructions[exclude_files_key]
            val = value.split('|')

        self._log_instruction(exclude_files_key, str(val))
        return val

    @property
    def exclude_extensions_instruction(self) -> list:
        """
        Get file extensions to exclude from instructions

        Returns:
            List<string>: Values to exclude

        Default value: []
        """
        exclude_extensions_key = "ExcludeExtensions"
        val: List[str] = []
        if exclude_extensions_key in self._instructions:
            value = self._instructions[exclude_extensions_key]
            val = value.split('|')
        self._log_instruction(exclude_extensions_key, str(val))
        return val

    @property
    def new_file_extension_instruction(self) -> str:
        """
        Get new extension from instructions

        Returns:
            str: New extension

        Default value: '.log'
        """
        new_file_extension_key = "NewFileExtension"
        val = ".log"
        if new_file_extension_key in self._instructions:
            val = self._instructions[new_file_extension_key]
        self._log_instruction(new_file_extension_key, val)
        return val

    @property
    def output_name_instruction(self) -> str:
        """
        Get output name from instructions

        Returns:
            str: Output name

        Default value: ''
        """
        output_name_key = "OutputName"
        val = ""
        if output_name_key in self._instructions:
            val = self._instructions[output_name_key]
        self._log_instruction(output_name_key, val)
        return val

    @property
    def regex_expression_instruction(self) -> str:
        """
        Get regex expression from instructions

        Returns:
            str: Regex expression

        Default value: ''
        """
        regex_key = "RegexExpression"
        val = ""
        if regex_key in self._instructions:
            val = self._instructions[regex_key]
        self._log_instruction(regex_key, val)
        return val

    @property
    def delete_instruction(self) -> bool:
        """
        Get delete instruction from instructions

        Returns:
            bool: Delete instruction

        Default value: False
        """
        delete_key = "Delete"
        val = False
        if delete_key in self._instructions:
            val = self._instructions[delete_key].lower() == "true"
        self._log_instruction(delete_key, str(val))
        return val

    @property
    def sort_type_instruction(self) -> str:
        """
        Get SortType instruction from instructions

        Returns:
            str: SortType

        Default value: 'None'
        """
        key = "SortType"
        val = "None"
        if key in self._instructions:
            val = self._instructions[key]
        self._log_instruction(key, val)
        return val

    def make_directory_path(self, relative_path: str) -> str:
        """
        Combines workfolder with relative path

        Args:
            relative_path(str): Relative path to add

        Returns:
            str: Full directory path
        """
        val = ""
        if self._workfolder:
            result = Path(self._workfolder)
            if relative_path and relative_path != "*":
                val = (result / relative_path).as_posix()
            else:
                val = result.as_posix()
        else:
            logging.error(f"Workfolder is set to '{self._workfolder}'")
        return val

    @staticmethod
    def get_files(directory: str, recursive: bool) -> List[str]:
        """
        Getting files from directory

        Args:
            directory(str): Directory path
            recursive(bool): Run recursive through sub directories

        Returns:
            list: Filepaths
        """
        files: List[str] = []
        if directory:
            path = Path(directory)
            if path.exists():
                if recursive:
                    files = list(str(x) for x in path.glob("**/*.*")
                                 if x.is_file())
                else:
                    files = list(str(x) for x in path.iterdir() if x.is_file())
        return files

    @staticmethod
    def get_directories(directory: str, recursive: bool) -> List[str]:
        """
         Getting sub directories from directory

        Args:
            directory(str): Directory path
            recursive(bool): Run recursive through sub directories

        Returns:
            list: Direcory paths
        """
        if directory:
            path = Path(directory)
            if path.exists():
                if recursive:
                    return [str(x) for x in path.glob("*/**") if x.is_dir()]
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
