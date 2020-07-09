# coding: utf-8

ORIG = 'orig'
ADD = 'add'


class PieceTableError(Exception):
    pass


class Piece:

    def __init__(self, type, start, length):
        self.type = type
        self.start = start
        self.length = length


class PieceTable:

    def __init__(self, text=''):
        self._buffer = {
            ORIG: text,
            ADD: ''
        }
        self._pieces = []
        self._pieces.append(Piece(ORIG, 0, len(text)))

    @property
    def text(self):
        s = ''
        for p in self._pieces:
            buf = self._buffer[p.type]
            s += buf[p.start:p.start+p.length]

        return s

    def insert(self, text, start):
        if start < 0:
            raise PieceTableError

        if text == '':
            return

        if start == 0:
            p = Piece(ADD, len(self._buffer[ADD]), len(text))
            self._buffer[ADD] += text
            self._pieces.insert(0, p)
            return

        if start == len(self.text):
            p = Piece(ADD, len(self._buffer[ADD]), len(text))
            self._buffer[ADD] += text
            self._pieces.append(p)
            return

        index, offset = self._get_index_and_offset(start)
        piece = self._pieces[index]
        p0 = Piece(piece.type, piece.start, start - offset)
        p1 = Piece(ADD, len(self._buffer[ADD]), len(text))
        p2 = Piece(piece.type,
                   piece.start + (start - offset),
                   piece.length - (start - offset))

        ps = list(filter(lambda x: x.length != 0, [p0, p1, p2]))

        self._buffer[ADD] += text
        self._pieces[index:index+1] = ps

    def delete(self, start, length):
        if not (0 <= start <= len(self.text) - 1):
            raise PieceTableError

        if length == 0:
            return

        l_index, l_offset = self._get_index_and_offset(start)
        ps = []
        if start - l_offset > 0:
            p = Piece(self._pieces[l_index].type,
                      self._pieces[l_index].start,
                      start - l_offset)
            ps.append(p)

        r_index = len(self._pieces) - 1
        if start + length < len(self.text):
            r_index, r_offset = self._get_index_and_offset(start + length)
            piece = self._pieces[r_index]
            r_start = piece.start + (start + length) - r_offset
            p = Piece(piece.type,
                      r_start,
                      piece.start + piece.length - r_start)
            ps.append(p)

        self._pieces[l_index:r_index+1] = ps

    def _get_index_and_offset(self, start):
        s = ''
        for i, p in enumerate(self._pieces):
            buf = self._buffer[p.type]
            s += buf[p.start:p.start+p.length]
            if start < len(s):
                return i, len(s) - p.length

        raise PieceTableError
