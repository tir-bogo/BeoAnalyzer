"""
Module contains a base class for file operations
"""
import abc
from pathlib import Path

class OperationBase(metaclass=abc.ABCMeta):
    """
    Base class for sharing methods across file operations
    """
    def __init__(self):
        self.__workfolder = None
        self.__config = None

    @property
    def workfolder(self):
        """
        Get workfolder

        Returns:
            str: workfolder
        """
        return self.__workfolder

    @workfolder.setter
    def workfolder(self, workfolder):
        """
        Set workfolder

        Args:
            workfolder (str): New workfolder path to operate from
        """
        self.__workfolder = workfolder

    @property
    def config(self):
        """
        Get config

        Returns:
            dict: Configuration for file operation
        """
        return self.__config

    @config.setter
    def config(self, config):
        """
        Set config

        Args:
            config(dict): Configuration for file operation
        """
        self.__config = config

    def _get_files(self, relative_filepath, recursive):
        """
        Get files from directory

        Args:
            relative_filepath(str): Relative file path to workfolder or * for current
            recursive(bool): Enable recursive behavior

        Returns:
            List<string>: Filepaths for files found
        """
        path = None
        if relative_filepath == "*":
            path = Path(self.workfolder)
        else:
            path = Path(self.workfolder, relative_filepath)

        result = []
        if recursive:
            result = list(x for x in path.glob("**/*.*") if x.is_file())

        else:
            result = list(x for x in path.iterdir() if x.is_file())

        return [str(x) for x in result]

    @abc.abstractmethod
    def config_is_valid(self):
        """
        Checking if configuration is valid

        Returns:
            bool: True configuration is valid, False configuration is NOT valid

        Raises:
            NotImplementedError: Must be implemented to use this base class
        """
        raise NotImplementedError("config_is_valid must be defined to use OperationBase class")

    @abc.abstractmethod
    def run(self):
        """
        Running the file operation

        Returns:
            bool: True run success, False run failed

        Raises:
            NotImplementedError: Must be implemented to use this base class
        """
        raise NotImplementedError("run must be defined to use OperationBase class")
