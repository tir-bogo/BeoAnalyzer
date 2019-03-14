"""
Module contains file operation to convert files to new extensions
"""
from pathlib import Path
from logfile.operations.operation_base import OperationBase

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

    def __init__(self):
        super().__init__()
        self.__directory_instruction_key = "Directory"
        self.__recursive_instruction_key = "Recursive"
        self.__new_file_extension_instruction_key = "NewFileExtension"
        self.__exclude_files_instruction_key = "ExcludeFiles"
        self.__exclude_extensions_instruction_key = "ExcludeExtensions"

    def config_is_valid(self):
        """
        Checking config is valid for this file operation

        Returns:
            bool: True configuration is valid, False configuration is NOT valid
        """
        if self.config is None or \
           self.__directory_instruction_key not in self.config or \
           self.__recursive_instruction_key not in self.config or \
           self.__new_file_extension_instruction_key not in self.config:
            return False
        return True

    @staticmethod
    def __convert_file(filepath, new_extension):
        """
        Convert file to new extension and deletes the old file

        Args:
            filepath(str): Full filepath to file
            new_extension(str):  New extension to file example: ('.txt')
        """
        path = Path(filepath)
        path.rename(Path(path.parents[0], path.name + new_extension))

    def __get_exclude_files_instruction(self):
        """
        Get file names to exclude from configuration instructions

        Returns:
            List<string>: Values to exclude
            None
        """
        if self.__exclude_files_instruction_key in self.config:
            value = self.config[self.__exclude_files_instruction_key]
            return value.split('|')
        return []

    def __get_exclude_extensions_instruction(self):
        """
        Get file extensions to exclude from configuration instructions

        Returns:
            List<string>: Values to exclude
            None
        """
        if self.__exclude_extensions_instruction_key in self.config:
            value = self.config[self.__exclude_extensions_instruction_key]
            return value.split('|')
        return []

    def __get_recursive_instruction(self):
        """
        Get recursive instruction from configuration instructions

        Returns:
            bool: Recursive behavior enabled
        """
        val = self.config[self.__recursive_instruction_key].lower()
        return val == "true"

    def __get_directory_instruction(self):
        """
        Get directory from configuration instructions

        Returns:
            str: Directory
        """
        return self.config[self.__directory_instruction_key]

    def __get_new_file_extension_instruction(self):
        """
        Get new extension from configuration instructions

        Returns:
            str: New extension
        """
        return self.config[self.__new_file_extension_instruction_key]

    @staticmethod
    def __list_item_contains_string(arr, item):
        """
        """
        for val in arr:
            if val in item:
                return True
        return False

    def run(self):
        """
        Converting files with selected instructions
        """
        new_extension = self.__get_new_file_extension_instruction()
        exclude_files = self.__get_exclude_files_instruction()
        exclude_ext = self.__get_exclude_extensions_instruction()
        recursive = self.__get_recursive_instruction()
        relative_file_path = self.__get_directory_instruction()

        files = self._get_files(relative_file_path, recursive)

        for filepath in files:
            if not self.__list_item_contains_string(exclude_files, filepath) and \
                not self.__list_item_contains_string(exclude_ext, filepath):
                self.__convert_file(filepath, new_extension)
