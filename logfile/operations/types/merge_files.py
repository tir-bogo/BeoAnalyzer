"""
Module contains file operation to merge files together
"""
import re
import fileinput
import logging
from typing import Pattern, List
from pathlib import Path
from logfile.operations.operation_base import OperationBase

# pylint: disable=W1203


class MergeFiles(OperationBase):
    """
    This class is responseable for merging files together with regex

    Instructions:
        Directory(str):
            Relative path in work folder or * for current work folder
        Recursive(str):
            False takes current folder
            True is recursive through current folder and subs
        OutputName(str):
            File name for merged file example: 'out.txt'
        Regex(str):
            Regex expression to match filepaths with
            For sorting first group must be int
        Delete:
            Delete old files after merge
        SortType:
            HighLow:
                Sorts file with regex group 1 to combined result high to low
            LowHigh:
                Sorts file with regex group 1 to combined result low to high
            None:
                Do not sort files
    """

    @staticmethod
    def match_files_with_regex(files: List[str],
                               regex: Pattern[str]) -> List[str]:
        """
        Matching files with regex expression

        Args:
            files(list): Files to match regex with
            regex(Pattern[str]): Precompiled regex

        Returns:
            list: Matched files
        """
        result = []
        if files and regex:
            for file_path in files:
                match = regex.search(file_path)
                if match:
                    result.append(file_path)
        return result

    @staticmethod
    def sort_files(files: List[str], regex: Pattern[str]) -> List[str]:
        """
        Sorting files using first group item in regex match

        Args:
            files(list): Files to order
            regex(Pattern[str]): Precompiled regex

        Returns:
            list: Sorted list
        """
        if files and regex:
            def regex_sort(line):
                match = regex.search(line)
                if match:
                    return match.groups()[0]
                return 0
            files.sort(key=regex_sort)
        return files

    @staticmethod
    def merge_files(new_file_path: str, files: List[str]) -> bool:
        """
        Merging files together with that order arg files is in

        Args:
            new_file_path(str): Output file path for new file
            files(list): Files to merge

        Returns:
            bool: Files is merged
        """
        if new_file_path and files:
            try:
                with open(new_file_path, 'w') as outfile:
                    for line in fileinput.input(files):
                        outfile.write(line + "\n")
                return True
            except OSError as exc:
                logging.error(f"Could not merge files '{exc}'")
        return False

    @staticmethod
    def delete_files(files: List[str]) -> bool:
        """
        Delete files

        Args:
            files(list): Files to delete

        Returns:
            bool: Files is deleted
        """
        if files:
            for file_path in files:
                try:
                    Path(file_path).unlink()
                except OSError as exc:
                    logging.warning(f"""Could not delete file '{file_path}'
                                    {exc}""")
            return True
        return False

    def run(self) -> bool:
        """
        Running mergefiles operation with given instructions
        """
        directory_path = self.make_directory_path(self.directory_instruction)
        recursive = self.recursive_instruction
        output_name = self.output_name_instruction
        regex_string = self.regex_expression_instruction
        delete = self.delete_instruction
        sort_type = self.sort_type_instruction

        if regex_string and \
           output_name and \
           directory_path and \
           Path(directory_path).exists():

            regex = re.compile(regex_string)

            directories = None
            if recursive:
                directories = self.get_directories(directory_path, recursive)
                directories.append(directory_path)
            else:
                directories = [directory_path]
            for path in directories:
                files = self.get_files(path, False)

                files_to_merge = self.match_files_with_regex(files, regex)

                if files_to_merge:
                    if sort_type == "LowHigh":
                        files_to_merge = self.sort_files(files_to_merge, regex)

                    elif sort_type == "HighLow":
                        files_to_merge = self.sort_files(files_to_merge, regex)
                        files_to_merge.reverse()

                    new_file_path = (Path(path) / output_name).as_posix()
                    self.merge_files(new_file_path, files_to_merge)

                    if delete:
                        self.delete_files(files_to_merge)

            self._log_run_success()
            return True

        self._log_run_failed("No files affected")
        return False
