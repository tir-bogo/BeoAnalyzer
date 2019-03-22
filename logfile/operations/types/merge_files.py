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
                match = regex.match(file_path)
                if match:
                    result.append(file_path)
        return result

    @staticmethod
    def sort_files(files: list, regex: Pattern[str]) -> list:
        """
        """
        if files and regex:
            def regex_sort(line):
                match = regex.match(line)
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
           Path(directory_path).exists():
            
            regex = re.compile(regex)
            directories = self.get_directories(directory_path, recursive)
            for path in directories:
                files = self.get_files(path, False)

                # kan blive til metode
                files_to_merge = []
                for file_path in files:
                    match = regex.match(file_path)
                    if match:
                        files_to_merge.append(file_path)
                
                # Kan blive til metode
                if len(files_to_merge) < 1 and sort_type != "None":

                    if sort_type == "LowHigh":
                        files_to_merge.sort(key=lambda x: int(regex.match(x).groups()[0]))
                    elif sort_type == "HighLow":
                        files_to_merge.sort(key=lambda x: int(regex.match(x).groups()[0]))
                        files_to_merge.reverse()
                
                # Merge file ny metode ?
                new_file_path = Path(path) / output_name
                with open(new_file_path, 'w') as outfile:
                    input_lines = fileinput.input(files_to_merge)
                    outfile.writelines(input_lines)
                
                if delete:
                    # metode
                    for fpath in files_to_merge:
                        Path.unlink(fpath)
                
                