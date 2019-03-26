"""
Module contains tests for ReaderResult
"""

from logfile.readers.reader_result import ReaderResult


def test_add():
    """
    Test can add key value to result
    """
    var = ReaderResult()
    var.add("my key", "my", "values")
    assert len(var.container) == 1

    obj = var.container[0]
    assert obj.key == "my key"
    assert obj.values == ("my", "values")


def test_add_key_none():
    """
    Test can add key value to result
    """
    var = ReaderResult()
    var.add(None, "my", "values")
    assert len(var.container) == 1

    obj = var.container[0]
    assert not obj.key
    assert obj.values == ("my", "values")


def test_add_values_none():
    """
    Test can add key value to result
    """
    var = ReaderResult()
    var.add("my key", None)
    assert len(var.container) == 1

    obj = var.container[0]
    assert obj.key == "my key"
    assert not obj.values[0]


def test_add_list():
    """
    Test add list to result
    """
    var = ReaderResult()
    var.add_list("my key", ["item"])
    assert len(var.container) == 1
    obj = var.container[0]
    assert obj.key == "my key"
    assert obj.values == ('item',)


def test_add_list_key_none():
    """
    Test add list to result when key is none
    """
    var = ReaderResult()
    var.add_list(None, ["item"])
    assert len(var.container) == 1
    obj = var.container[0]
    assert not obj.key
    assert obj.values == ('item',)


def test_add_list_values_none():
    """
    Test add list to result when values is none
    """
    var = ReaderResult()
    var.add_list("my key", None)
    assert len(var.container) == 1
    obj = var.container[0]
    assert obj.key == "my key"
    assert not obj.values
