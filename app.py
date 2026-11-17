"""Visualizacion de limpieza
Autores: Ángel Adrik Merino Cedeño A01751507
        Ana Karen Abrego Flores A01753979
Fecha: 16/11/26 
"""

import solara
from mesa.visualization import SolaraViz, SpaceRenderer
from mesa.visualization.components import AgentPortrayalStyle
from agents import Cell
from model import CleaningModel


# Define el color y la forma de celdas y robots.
def agentPortrayal(agent):
    if isinstance(agent, Cell):
        return AgentPortrayalStyle(
            color="black" if agent.state == Cell.DIRTY else "lightgray",
            marker="s",
            size=100,
        )

    return AgentPortrayalStyle(
        color="red",
        marker="o",
        size=100,
        zorder=3,
    )

def postProcess(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


# Muestra las estadisticas del modelo, sin calcularlas en la interfaz.
# Parametros: model (modelo actual).
# Retorno: ninguno.
def showStatistics(model):
    solara.Markdown(
        f"**Robots activos:** {len(model.robots)}  \n"
        f"**Pasos transcurridos:** {model.time}  \n"
        f"**Celdas limpias:** {model.cleanPercentage:.1f}%  \n"
        f"**Movimientos totales:** {model.totalMovements}  \n"

    )


modelParams = {
    "rng": {
        "type": "InputText", 
        "value": 42, 
        "label": "Semilla"
    },
    "width": {
        "type": "SliderInt", 
        "value": 10, 
        "label": "Ancho", 
        "min": 2, 
        "max": 30
    },
    "height": {
        "type": "SliderInt", 
        "value": 10, 
        "label": "Alto", 
        "min": 2, 
        "max": 30
    },
    "numRobots": {
        "type": "SliderInt", 
        "value": 1, 
        "label": "Robots", 
        "min": 1, 
        "max": 20
    },
    "dirtyFraction": {
        "type": "SliderFloat", 
        "value": 0.3, 
        "label": "Porcentaje sucio",
        "min": 0.0, 
        "max": 1.0, 
        "step": 0.05,
    },
    "maxSteps": {
        "type": "SliderInt", 
        "value": 1000, 
        "label": "Tiempo maximo",
        "min": 10, 
        "max": 3000, 
        "step": 10,
    },
}

# Crea la instancia inicial del modelo
model = CleaningModel(numRobots=1, rng=42)

renderer = SpaceRenderer(model, backend="matplotlib")
renderer.render(agent_portrayal=agentPortrayal)
renderer.post_process = postProcess

page = SolaraViz(
    model,
    renderer,
    components=[(showStatistics, 0)],
    model_params=modelParams,
    name="Robots reactivos",
)

page    #noqa



