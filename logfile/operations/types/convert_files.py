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
    def convert_file(filepath: str, new_extension: str) -> bool:
        """
        Convert file to new extension and deletes the old file

        Args:
            filepath(str): Full filepath to file
            new_extension(str):  New extension to file example: ('.txt')

        Returns:
            bool: Convert is a success
        """
        if filepath and new_extension:
            path = Path(filepath)

            if path.exists():
                try:
                    new_path = Path(path.parents[0], path.name + new_extension)
                    path.rename(new_path)
                    logging.debug(f"Converted file '{path}' to '{new_extension}'")
                    return True
                except OSError as exc:
                    logging.warning(f"Could not convert file '{path}' to '{new_extension}' {exc}")
        return False

    @staticmethod
    def list_item_in_string(arr: list, item: str) -> bool:
        """
        Checks if any part in a list match a string
        Example:
            item = 'c:/windows/llll/file.1h'
            arr = ['file.1h', 'ttt' , 'yyy']
            returns True

        Args:
            arr(list): List of string
            item(str): Item to search for

        Returns:
            bool: Item is found
        """
        if arr and item:
            for val in arr:
                if val in item:
                    return True
        return False

    @staticmethod
    def sort_files(files: list, filters: list):
        """
        Discard files where filters match file

        Args:
            files(list): Filepaths
            filters(list): Filters for files to discard

        Returns:
            list: Remainding files
        """
        result = []
        if files:
            for filepath in files:
                if ConvertFiles.list_item_in_string(filters, filepath):
                    logging.debug(f"Skipping file to convert {filepath}")
                else:
                    result.append(filepath)
        return result

    def run(self) -> bool:
        """
        Converting files with selected instructions

        Returns:
            bool: True run success, False run failed
        """
        new_extension = self.new_file_extension_instruction
        exclude_files = self.exclude_files_instruction
        exclude_ext = self.exclude_extensions_instruction
        recursive = self.recursive_instruction
        relative_file_path = self.directory_instruction

        directory_path = self.make_directory_path(relative_file_path)

        files = self.get_files(directory_path, recursive)
        files = self.sort_files(files, exclude_files)
        files = self.sort_files(files, exclude_ext)

        if files != []:
            for filepath in files:
                self.convert_file(filepath, new_extension)

            self._log_run_success()
            return True

        self._log_run_failed("No files affected")
        return False
