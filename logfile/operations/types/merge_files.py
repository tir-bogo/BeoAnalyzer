"""
Module contains file operation to merge files together
"""
import re
import fileinput
import logging
from typing import Pattern
from pathlib import Path
from logfile.operations.operation_base import OperationBase

class MergeFiles(OperationBase):
    """
    """

    @staticmethod
    def match_files_with_regex(files: list, regex: Pattern[str]) -> list:
        """
        """
        result = []
        if files and regex:
            for file_path in files:
                match = regex.search(file_path)
                if match:
                    result.append(file_path)
        return result

    @staticmethod
    def sort_files(files: list, regex: Pattern[str]) -> list:
        """
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
    def merge_files(new_file_path: str, files: list) -> bool:
        """
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
    def delete_files(files: list) -> bool:
        """
        """
        if files:
            for file_path in files:
                try:
                    Path(file_path).unlink()
                except OSError as exc:
                    logging.warning(f"Could not delete file '{file_path}' {exc}")
            return True
        return False
                
            

    def run(self) -> bool:
        """
        """
        directory_path = self.make_directory_path(self.directory_instruction)
        recursive = self.recursive_instruction
        output_name = self.output_name_instruction
        regex = self.regex_expression_instruction
        delete = self.delete_instruction
        sort_type = self.sort_type_instruction

        if regex and \
           output_name and \
           directory_path and \
           Path(directory_path).exists():
            
            regex = re.compile(regex)

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
        
        self._log_run_failed()
        return False
                