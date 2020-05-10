from typing import List


class Matrix:

    def __init__(self, matrix: List[List[float]]):
        assert matrix
        assert len(matrix) >= 1 and len(matrix[0]) >= 1
        for i in range(len(matrix) - 1):
            assert len(matrix[i + 1]) is len(matrix[i])

        self._matrix = matrix
        self._rows = len(matrix)
        self._cols = len(matrix[0])

    def get(self):
        return self._matrix

    def get_rows(self):
        return self._rows

    def get_cols(self):
        return self._cols

    def sum(self, matrix: 'Matrix' = None) -> 'Matrix':
        if matrix is None:
            var = 0.0
            for e in self._matrix:
                var += sum(e)
            return Matrix([[var]])
        assert self._rows is matrix._rows and self._cols is matrix._cols
        _M = [
            [self._matrix[i][j] + matrix.get()[i][j] for j in range(self._cols)] for i in range(self._rows)
        ]
        return Matrix(_M)

    def sub(self, matrix: 'Matrix') -> 'Matrix':
        assert self._rows is matrix._rows and self._cols is matrix._cols
        _M = [
            [self._matrix[i][j] - matrix.get()[i][j] for j in range(self._cols)] for i in range(self._rows)
        ]
        return Matrix(_M)

    def mult(self, matrix: 'Matrix' = None, value=None) -> 'Matrix':
        if matrix:
            assert self._cols is matrix._rows
            rows: int = self._rows
            cols: int = matrix._cols

            _M = Matrix.empty(rows, cols)

            for i in range(rows):
                for j in range(cols):
                    for k in range(matrix._rows):
                        _M.get()[i][j] += self.get()[i][k] * matrix.get()[k][j]
            return _M
        else:
            assert value
            rows: int = self._rows
            cols: int = self._cols

            _M = Matrix.empty(rows, cols)

            for i in range(rows):
                for j in range(cols):
                    _M.get()[i][j] = self.get()[i][j] * value
            return _M

    @staticmethod
    def empty(rows=2, cols=2) -> 'Matrix':
        return Matrix([[0 for c in range(cols)] for r in range(rows)])
