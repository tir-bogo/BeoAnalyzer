"""
Module contains a base class for file readers
"""

import abc
import logging
from typing import Dict
from pathlib import Path
from logfile.readers.reader_result import ReaderResult

# pylint: disable=W1203


class ReaderBase(metaclass=abc.ABCMeta):
    """
    Base for File Readers
    """

    def __init__(self, workfolder: str, relative_path: str,
                 instructions: Dict[str, str]):
        """
        Args:
            workfolder(str): Base where relative paths can be made from
            relative_path(str): Relative path to file
            instructions(Dict[str, str]): Instructions to reader
        """
        logging.info(f"Running FileOperation'{self.__class__.__name__}'")
        self._workfolder = workfolder
        self._relative_path = relative_path
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
    def file_path(self) -> str:
        """
        Get filepath to target file to read

        Returns:
            str: Filepath to target file
        """
        target = ""
        if self._workfolder and self._relative_path:
            val = Path(self._workfolder) / self._relative_path
            if val.exists() and val.is_file():
                target = val.as_posix()
        logging.info(f"Target file to read '{target}'")
        return target

    @property
    def key_name_instruction(self) -> str:
        """
        Get key name instruction

        Returns:
            str: Key name from instructions

        Default value: ""
        """
        key = "KeyName"
        value = ""
        if key in self._instructions:
            value = self._instructions[key]
        self._log_instruction(key, value)
        return value

    @property
    def enable_linenumber_instruction(self) -> bool:
        """
        Get enable linenumber instruction

        Returns:
            bool: enable linenumber from instructions

        Default value: False
        """
        key = "EnableLineNumber"
        value = False
        if key in self._instructions:
            value = self._instructions[key].lower() == "true"
        self._log_instruction(key, str(value))
        return value

    @abc.abstractmethod
    def read(self) -> ReaderResult:
        """
        Reading the document
        """
        raise NotImplementedError("Read must be defined")
