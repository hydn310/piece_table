
import pytest
from piece_table import PieceTable, PieceTableError


class TestInsert:

    @pytest.mark.parametrize('orig, add, start, expected', [
        ('abc', 'def', 0, 'defabc'),
        ('abc', 'def', 1, 'adefbc'),
        ('abc', 'def', 2, 'abdefc'),
        ('abc', 'def', 3, 'abcdef'),
        ('', 'abc', 0, 'abc'),
    ])
    def test_insert(self, orig, add, start, expected):
        t = PieceTable(orig)
        t.insert(add, start)
        assert t.text == expected

    @pytest.mark.parametrize('orig, add, start', [
        ('abc', 'def', -1),
        ('abc', 'def', 10),
        ('', 'abc', -1),
        ('', 'abc', 10),
    ])
    def test_insert_invalid_start(self, orig, add, start):
        t = PieceTable(orig)
        with pytest.raises(PieceTableError):
            t.insert(add, start)

    def test_insert_multiple(self):
        t = PieceTable('abc')
        t.insert('d', 3)
        t.insert('ef', 4)
        t.insert('ghi', 6)
        assert t.text == 'abcdefghi'
