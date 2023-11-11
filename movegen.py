from defs import is_empty, COLOR_MASK


def knight_moves(row, col, color, board, moves):
    cords = [(1, 2),
             (1, -2),
             (2, 1),
             (2, -1),
             (-1, 2),
             (-1, -2),
             (-2, -1),
             (-2, 1)]

    for mods in cords:
        _row = row + mods[0]
        _col = col + mods[1]
        space = board.state[_row][_col]
        if is_empty(space) or (space & COLOR_MASK) != color:
            moves.append((_row, _col))
