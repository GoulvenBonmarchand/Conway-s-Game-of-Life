from conway_s_game_of_life.world import Cell

def test_init():
    cell = Cell(2, 3)
    assert cell.loc == (2, 3)

def test_eq():
    cell1 = Cell(1, 1)
    cell2 = Cell(1, 1)
    cell3 = Cell(2, 2)
    assert cell1 == cell2
    assert cell1 != cell3

def test_hash():
    cell1 = Cell(1, 1)
    cell2 = Cell(1, 1)
    cell3 = Cell(1, 2)
    assert hash(cell1) == hash(cell2)
    assert hash(cell1) != hash(cell3)