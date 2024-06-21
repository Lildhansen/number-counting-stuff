import pytest
from randomNumberStuff import parenthesisCleanup

def test_parenthesisCleanup():
    assert parenthesisCleanup("(((4)+5)-3)") == "(4+5-3)"
    assert parenthesisCleanup("((4+5)+3+(-3))") == "(4+5+3-3)"
    assert parenthesisCleanup("((4-3)*5)") == "(4-3)*5"
    ## add these:
    """
    4-3 = 1
5-3 = 2
3 = 3
4 = 4
((4-3)*5) = 5
5-3+4 = 6
3+4 = 7
5+3 = 8
5+4 = 9
    """

