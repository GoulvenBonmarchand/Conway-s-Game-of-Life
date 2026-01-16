import pytest
from conway_s_game_of_life.world import World
from pathlib import Path
import filecmp

@pytest.fixture
def glider_file_path():
    res_dir = Path(__file__).parent / "res"
    return res_dir / "glider.txt"

def test_glider(glider_file_path):
    world = World.from_file(glider_file_path)
    expected_cells = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    assert sorted(world.cells) == sorted(expected_cells)
    assert world.taille == (-1, -1, 3, 3)
    
    world.step()
    work_dir = Path(__file__).parent / "work"
    work_dir.mkdir(exist_ok=True)
    output_file = work_dir / "glider_step1.txt"
    world.to_file(output_file)
    assert output_file.exists()
    assert filecmp.cmp(output_file, glider_file_path.parent / "glider_step1_expected.txt")