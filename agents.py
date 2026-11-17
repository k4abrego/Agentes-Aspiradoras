"""
Autores: Ángel Adrik Merino Cedeño A01751507
        Ana Karen Abrego Flores A01753979
Fecha: 16/11/26 
"""

from mesa.discrete_space import CellAgent, FixedAgent

class Cell(FixedAgent):
    """Representa una celda fija que puede estar limpia o sucia"""
    CLEAN = 0
    DIRTY = 1

    # Crea una celda con su estado inicial
    def __init__(self, model, cell, state=CLEAN):
        super().__init__(model)
        self.cell = cell
        self.state = state

    
class CleaningRobot(CellAgent):
    """Robot reactivo, solo observa su celda actual"""

    DIRECTIONS = (
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1),
    )

    # Coloca el robot en su celda inicial
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell
        self.movements = 0

    # Limpia su celda o intenta avanzar en una dirección aleatoria
    def step(self):
        currentCell = self.model.cells[self.cell.coordinate]

        if currentCell.state == Cell.DIRTY:
            currentCell.state = Cell.CLEAN
        else:
            direction = self.random.choice(self.DIRECTIONS)
            newX = self.cell.coordinate[0] + direction[0]
            newY = self.cell.coordinate[1] + direction[1]

            # Un movimiento fuera de la habitación no cambia la posición
            if 0 <= newX < self.model.width and 0 <= newY < self.model.height:
                self.cell = self.model.cells[(newX, newY)].cell
                self.movements += 1






