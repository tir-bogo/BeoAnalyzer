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
        OperationBase.__init__(self)

    def instructions_is_valid(self):
        """
        Checking instructions is valid for this file operation

        Returns:
            bool: True instructions is valid, False instructions is NOT valid
        """
        if self.instructions is None or \
           self._directory_instruction_key not in self.instructions or \
           self._recursive_instruction_key not in self.instructions or \
           self._new_file_extension_instruction_key not in self.instructions:
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
        new_file = Path(path.parents[0], path.name + new_extension)
        new_file.write_text(path.read_text())
        path.unlink()

    @staticmethod
    def __list_item_contains_string(arr, item):
        """
        """
        for val in arr:
            if val.lower() in item.lower():
                return True
        return False

    def run(self):
        """
        Converting files with selected instructions
        """
        new_extension = self._get_new_file_extension_instruction()
        exclude_files = self._get_exclude_files_instruction()
        exclude_ext = self._get_exclude_extensions_instruction()
        recursive = self._get_recursive_instruction()
        relative_file_path = self._get_directory_instruction()

        files = self._get_files(relative_file_path, recursive)

        for filepath in files:
            if not self.__list_item_contains_string(exclude_files, filepath) and \
                not self.__list_item_contains_string(exclude_ext, filepath):
                self.__convert_file(filepath, new_extension)
