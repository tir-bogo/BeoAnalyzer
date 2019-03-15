"""
Module contains file operation to convert files to new extensions
"""
from pathlib import Path
import logging
from logfile.operations.operation_base import OperationBase

# pylint: disable=W1203

class ConvertFiles(OperationBase):
    """
    This class is responseable for converting files to new file extension

    Instructions:
        Directory(str):
            Relative path in work folder or * for current work folder
        Recursive(str):
            False takes current folder, true is recursive through current folder and subs
        NewFileExtension(str):
            The extension files will be converted to
        ExcludeExtensions(str):
            Exclude extensions ".txt|.exe"
        ExcludeFiles(str):
            Exclude files "messages.0|log.txt"
    """

    @staticmethod
    def _convert_file(filepath: str, new_extension: str) -> None:
        """
        Convert file to new extension and deletes the old file

        Args:
            filepath(str): Full filepath to file
            new_extension(str):  New extension to file example: ('.txt')
        """
        try:
            path = Path(filepath)
            new_path = Path(path.parents[0], path.name + new_extension)
            path.rename(new_path)
            logging.debug(f"Converted file '{path}' to '{new_extension}'")
        except OSError as exc:
            logging.warning(f"Could not convert file '{path}' to '{new_extension}' {exc}")

    @staticmethod
    def __list_item_contains_string(arr: list, item: str) -> bool:
        """
        Checks if list items contains part of a string

        Example:
            item = '1h'
            arr = ['ge1h', 'ttt' , 'yyy']
            returns True

        Args:
            arr(list): List of string
            item(str): Item to search for

        Returns:
            bool: Item is found
        """
        for val in arr:
            if val in item:
                return True
        return False

    def run(self) -> bool:
        """
        Converting files with selected instructions

        Returns:
            bool: True run success, False run failed
        """
        try:
            new_extension = self._new_file_extension_instruction
            exclude_files = self._exclude_files_instruction
            exclude_ext = self._exclude_extensions_instruction
            recursive = self._recursive_instruction
            relative_file_path = self._directory_instruction

            files = self._get_files(relative_file_path, recursive)

            for filepath in files:
                if not self.__list_item_contains_string(exclude_files, filepath) and \
                    not self.__list_item_contains_string(exclude_ext, filepath):
                    self._convert_file(filepath, new_extension)
            return True

        except TypeError as exc:
            logging.warning(f"Instructions is '{self.instructions}' {exc}")

        except OSError as exc:
            logging.warning(f"Invalid relative path '{relative_file_path}' {exc}")

        return False
