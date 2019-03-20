"""
Module contains file operation to pretty print files in json
"""
import logging
import json
from json.decoder import JSONDecodeError
from logfile.operations.operation_base import OperationBase

# pylint: disable=W1203

class PrettyJson(OperationBase):
    """
    This class is responseable for pretty printing json files
    """

    @staticmethod
    def pretty_print_file(filepath: str) -> bool:
        """
        Pretty print file content of a json file

        Args:
            filepath(str): File to convert file content
        Returns:
            bool: True file is pretty printed, False file NOT pretty printed
        """
        if filepath:
            logging.debug(f"Pretty printing file content for '{filepath}'")
            try:
                with open(filepath, 'r') as handle:
                    json_data = json.load(handle)
                    handle.close()

                with open(filepath, 'w') as handle:
                    pretty_json = json.dumps(json_data, sort_keys=True, indent=4)
                    handle.write(pretty_json)
                    handle.close()
                return True

            except JSONDecodeError:
                logging.warning(f"Invalid json in file '{filepath}'")
            except OSError as exc:
                logging.warning(f"{exc}")
        return False

    def run(self) -> bool:
        """
        Runs recursively and pretty print all possible files
        Returns:
            bool: Operation run successfull
        """
        dir_path = self.make_directory_path("*")
        files = self.get_files(dir_path, True)
        if files != []:
            for filepath in files:
                PrettyJson.pretty_print_file(filepath)
            return True
        return False
