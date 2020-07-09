
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


class TestDelete:

    @pytest.mark.parametrize('orig, start, length, expected', [
        ('abc', 0, 1, 'bc'),
        ('abc', 1, 1, 'ac'),
        ('abc', 2, 1, 'ab'),
        ('abc', 0, 3, ''),
        ('abc', 1, 2, 'a'),
        ('abc', 0, 0, 'abc'),
        ('abc', 1, 10, 'a'),
    ])
    def test_delete(self, orig, start, length, expected):
        t = PieceTable(orig)
        t.delete(start, length)
        assert t.text == expected

    @pytest.mark.parametrize('orig, start', [
        ('abc', -1),
        ('abc', 10),
    ])
    def test_delete_invalid_start(self, orig, start):
        t = PieceTable(orig)
        with pytest.raises(PieceTableError):
            t.delete(start, 1)

    def test_delete_multiple(self):
        t = PieceTable('abcdef')
        t.delete(2, 2)
        t.delete(0, 1)
        t.delete(1, 2)
        assert t.text == 'b'
