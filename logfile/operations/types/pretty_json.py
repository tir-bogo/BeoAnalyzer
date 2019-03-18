"""
Module contains file operation to pretty print files in json
"""
import json
from logfile.operations.operation_base import OperationBase

class PrettyJson(OperationBase):
    """
    """

    @staticmethod
    def _format(filepath):
        """
        """


    def run(self):
        """
        """
        with open('/home/autotest/Desktop/test.txt', 'r') as handle:
            print(json.dumps(json.load(handle.read()), sort_keys=True, indent=4))
