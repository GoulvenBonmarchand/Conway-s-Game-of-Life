import argparse

import pygame

p = argparse.ArgumentParser(
    description="Jeu de la vie (Conway) - simulation."
)
p.add_argument("--input", help="Chemin du fichier d'entrée (txt).")
p.add_argument("--output", help="Chemin du fichier de sortie (txt). si omis, pas de sauvegarde.")
p.add_argument(
    "-n",
    "--steps",
    type=int,
    default=6000,
    help="Nombre d'itérations à simuler (défaut: 1000).",
)
p.add_argument("--taille", help="Taille de la fenêtre graphique (largeur,hauteur). Par défaut 30,30."
               , default="50,50")

class Cell:
    def __init__(self, i, j):
        self._i = i
        self._j = j
    
    def __eq__(self, other):
        if not isinstance(other, Cell):
            return NotImplemented
        return self._i == other._i and self._j == other._j

    def __hash__(self):
        return hash((self._i, self._j))

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
            min_i, min_j, max_i, max_j = self.taille
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
    def cells(self):
        return [(cell.loc[1], cell.loc[0]) for cell in self._cells]
    
    @property
    def taille(self):
        if not self._cells:
            return (0, 0, 0, 0)
        max_i = max(cell.loc[0] for cell in self._cells)
        max_j = max(cell.loc[1] for cell in self._cells)
        min_i = min(cell.loc[0] for cell in self._cells)
        min_j = min(cell.loc[1] for cell in self._cells)
        return (min_i-1, min_j-1, max_i + 1, max_j + 1)
    
    def step(self):
        new_world = World()
        min_i, min_j, max_i, max_j = self.taille
        for i in range(min_i, max_i + 1):
            for j in range(min_j, max_j + 1):
                alive = self.is_alive(i, j)
                voisins = self.nb_voisin(i, j)
                if alive and (voisins == 2 or voisins == 3):
                    new_world.add_cell(i, j)
                elif not alive and voisins == 3:
                    new_world.add_cell(i, j)
        self._cells = new_world._cells
    
class Simulation:
    def __init__(self, world, steps):
        self._world = world
        self._steps = steps

    def run(self, taille):
        cell_size = 20
        GRID_W, GRID_H = taille[0], taille[1] 
        WIN_W, WIN_H = GRID_W * cell_size, GRID_H * cell_size
        def draw(screen, alive_cells):
            screen.fill((255, 255, 255))  
            for (x, y) in alive_cells:
                if 0 <= x < GRID_W and 0 <= y < GRID_H:
                    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, (0, 0, 0), rect)
            pygame.display.flip()

        FPS = 20
        step = 0
        pygame.init()
        screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Jeu de la vie (Conway) - simulation")
        clock = pygame.time.Clock()
        running = True
        paused = False
        
        while running:
            clock.tick(FPS)

            # --- Events ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if step >= self._steps:
                    running = False

                # Pause avec espace
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    paused = not paused

                # --- Update simulation ---
                if not paused:
                    cells = self._world.cells
                    self._world.step()

                # --- Draw ---
                step += 1
                draw(screen, cells)

        pygame.quit()

w = World.from_file(p.parse_args().input)
sim = Simulation(w, p.parse_args().steps)
sim.run(tuple(int(x) for x in p.parse_args().taille.split(",")))
if p.parse_args().output:
    w.to_file(p.parse_args().output)