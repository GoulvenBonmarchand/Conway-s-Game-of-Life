class Cell:
    def __init__(self, i, j):
        self._i = i
        self._j = j
    
    @property
    def loc(self):
        return (self._i, self._j)

class World:
    def __init__(self):
        self._cells = set()

    @classmethod
    def from_file(cls, file_path):
        w = cls()
        with open(file_path, "r", encoding="utf-8") as f:
            for i, ligne in enumerate(f):
                for j, char in enumerate(ligne):
                    if char == "1":
                        w.add_cell(i, j)
        return w
    
    def to_file(self, file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            (min_i, min_j), (max_i, max_j) = self.dimension
            for i in range(min_i, max_i + 1):
                ligne = ""
                for j in range(min_j, max_j + 1):
                    if self.is_alive(i, j):
                        ligne += "1"
                    else:
                        ligne += "0"
                f.write(ligne + "\n")
    
    def add_cell(self, i, j):
        self._cells.add(Cell(i, j))

    def remove_cell(self, i, j):
        self._cells.discard(Cell(i, j))
    
    def is_alive(self, i, j):
        return Cell(i, j) in self._cells

    def nb_voisin(self, i, j):
        voisins = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),          (0, 1),
                   (1, -1), (1, 0), (1, 1)]
        count = 0
        for di, dj in voisins:
            if self.is_alive(i + di, j + dj):
                count += 1
        return count
    
    @property
    def dimension(self):
        if not self._cells:
            return (0, 0)
        max_i = max(cell.loc[0] for cell in self._cells)
        max_j = max(cell.loc[1] for cell in self._cells)
        min_i = min(cell.loc[0] for cell in self._cells)
        min_j = min(cell.loc[1] for cell in self._cells)
        return ((min_i-1, min_j-1), (max_i + 1, max_j + 1))
    
    def step(self):
        new_world = World()
        (min_i, min_j), (max_i, max_j) = self.dimension
        for i in range(min_i, max_i + 1):
            for j in range(min_j, max_j + 1):
                alive = self.is_alive(i, j)
                voisins = self.nb_voisin(i, j)
                if alive and (voisins == 2 or voisins == 3):
                    new_world.add_cell(i, j)
                elif not alive and voisins == 3:
                    new_world.add_cell(i, j)
        self._cells = new_world._cells
    
w = World.from_file("../data/glider.txt")
w.step()
w.to_file("../data/glider_step1.txt")