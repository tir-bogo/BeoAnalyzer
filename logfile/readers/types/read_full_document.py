"""
Module contains file reader to read an entire document
"""
from logfile.readers.reader_base import ReaderBase
from logfile.readers.reader_result import ReaderResult


class ReadFullDocument(ReaderBase):
    """
    Read entire document file reader

    Instructions:
        KeyName: Key to add to result
        EnableLineNumber: Setting line number as first value in result
    """

    def read(self) -> ReaderResult:
        """
        Reading an entire document
        """
        file_to_read = self.file_path
        key_name = self.key_name_instruction
        enable_linenumber = self.enable_linenumber_instruction

        result = ReaderResult()
        if file_to_read and key_name:
            with open(file_to_read, 'r') as content_file:
                content = content_file.read()

            if enable_linenumber:
                result.add(key_name, "1", content)
            else:
                result.add(key_name, content)
            self._log_run_success()
        else:
            self._log_run_failed("Invalid file path or instructions")
        return result
