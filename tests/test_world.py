from conway_s_game_of_life.world import World

def test_empty_world():
    world = World()
    assert world.cells == []
    assert world.nb_voisin(0, 0) == 0
    assert world.nb_voisin(100, -100) == 0
    assert world.taille == (0, 0, 0, 0)
    world.step()
    assert world.cells == []
    assert world.taille == (0, 0, 0, 0)

def test_one_cell():
    world = World()
    world.add_cell(1, 1)
    assert world.cells == [(1, 1)]
    assert world.taille == (0, 0, 2, 2)
    assert world.nb_voisin(1, 1) == 0
    assert world.nb_voisin(0, 0) == 1
    assert world.nb_voisin(3,3) == 0
    world.step()
    assert world.cells == []
    assert world.taille == (0, 0, 0, 0)

def test_block_stability():
    world = World()
    block_cells = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for i, j in block_cells:
        world.add_cell(i, j)
    assert world.nb_voisin(1, 1) == 3
    assert world.nb_voisin(1, 2) == 3
    assert sorted(world.cells) == sorted(block_cells)
    assert world.taille == (0, 0, 3, 3)
    world.step()
    assert sorted(world.cells) == sorted(block_cells)
    assert world.taille == (0, 0, 3, 3)

def test_blinker_oscillation():
    world = World()
    blinker_cells = [(1, 0), (1, 1), (1, 2)]
    for i, j in blinker_cells:
        world.add_cell(i, j)
    assert sorted(world.cells) == sorted(blinker_cells)
    assert world.taille == (0, -1, 2, 3)
    world.step()
    expected_after_step = [(0, 1), (1, 1), (2, 1)]
    assert sorted(world.cells) == sorted(expected_after_step)
    assert world.taille == (-1, 0, 3, 2)
    world.step()
    assert sorted(world.cells) == sorted(blinker_cells)
    assert world.taille == (0, -1, 2, 3)