"""Modelo y mediciones de robots de limpieza
Autores: Ángel Adrik Merino Cedeño A01751507
        Ana Karen Abrego Flores A01753979
Fecha: 16/11/26 
"""
from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid
from agents import Cell, CleaningRobot


class CleaningModel(Model):
    """Habitación con suciedad aleatoria y robots sin memoria"""

    def __init__(self, width=10, height=10, numRobots=1,
                 dirtyFraction=0.3, maxSteps=1000, rng=None):
        super().__init__(rng=rng)

        if width < 2 or height < 2 or numRobots < 1 or maxSteps < 0:
            raise ValueError("Dimensiones >= 2, robots >= 1 y pasos >= 0.")
        if not 0.0 <= dirtyFraction <= 1.0:
            raise ValueError("dirtyFraction debe estar entre 0 y 1.")

        self.width = width
        self.height = height
        self.maxSteps = maxSteps
        self.time = 0
        self.grid = OrthogonalMooreGrid(
            (width, height), capacity=None, random=self.random, torus=False
        )

        # Se seleccionan las celdas sucias antes de crear los robots
        gridCells = list(self.grid.all_cells)
        dirtyCount = round(len(gridCells) * dirtyFraction)
        dirtyCoordinates = {
            cell.coordinate for cell in self.random.sample(gridCells, dirtyCount)
        }

        self.cells = {}
        for cell in gridCells:
            state = Cell.DIRTY if cell.coordinate in dirtyCoordinates else Cell.CLEAN
            self.cells[cell.coordinate] = Cell(self, cell, state)

        startCell = self.cells[(1, 1)].cell
        self.robots = [CleaningRobot(self, startCell) for _ in range(numRobots)]
        self.running = self.dirtyCount > 0 and maxSteps > 0

    # Cuenta las celdas que todavía están sucias
    @property
    def dirtyCount(self):
        return sum(cell.state == Cell.DIRTY for cell in self.cells.values())

    # Obtiene el porcentaje de celdas limpias
    @property
    def cleanPercentage(self):
        return 100.0 * (1.0 - self.dirtyCount / (self.width * self.height))


    # Cuenta solo los movimientos efectivos de los robots
    @property
    def totalMovements(self):
        return sum(robot.movements for robot in self.robots)

    # Ejecuta una acción por robot en orden aleatorio
    def step(self):
        if self.running:
            for robot in self.random.sample(self.robots, len(self.robots)):
                robot.step()

            self.time += 1
            if self.dirtyCount == 0 or self.time >= self.maxSteps:
                self.running = False


# Para que se muestren los resultadors para el reporte
if __name__ == "__main__":
        print(
            f"Robots: {numRobots} | "
            f"Pasos promedio: {totalTime / 30:.1f} | "
            f"Limpieza promedio: {totalClean / 30:.1f}% | "
            f"Movimientos promedio: {totalMoves / 30:.1f}"
        )








