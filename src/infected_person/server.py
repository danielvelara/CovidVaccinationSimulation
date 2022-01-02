from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from infected_person.agents import Infected, Person, Vaccine
from infected_person.model import InfectedPerson


def infected_person_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Person:
        portrayal["Shape"] = "infected_person/resources/person.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Infected:
        portrayal["Shape"] = "infected_person/resources/infected.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is Vaccine:
        if agent.grown:
            # portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
            portrayal["Color"] = ["#82fffb", "#82fffb", "#82fffb"]
        else:
            # portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
            portrayal["Color"] = ["#FFF", "#FFF", "#FFF"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(infected_person_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Infected", "Color": "#AA0000"}, {"Label": "Person", "Color": "#666666"}]
)

model_params = {
    "vaccine": UserSettableParameter("checkbox", "Vaccine Enabled", True),
    "vaccine_spawned_time": UserSettableParameter(
        "slider", "Vaccine Regrowth Time", 75, 50, 100
    ),
    "initial_people": UserSettableParameter(
        "slider", "Initial People Population", 100, 10, 300
    ),
    "infection_rate": UserSettableParameter(
        "slider", "Infection rate without vaccine", 0.33, 0.10, 1.0, 0.01
    ),
    "death_rate": UserSettableParameter(
        "slider", "Death Rate", 0.12, 0.01, 0.30, 0.01
    ),
    "recovery_rate": UserSettableParameter(
        "slider", "Recovery Rate", 0.30, 0.01, 0.50, 0.01
    ),
    "initial_infected": UserSettableParameter(
        "slider", "Initial Infected Population", 50, 1, 300
    ),
    "immunity_from_vaccine": UserSettableParameter(
        "slider", "Vaccine immunity", 0.70, 0.10, 1.0, 0.01
    ),
}

server = ModularServer(
    InfectedPerson, [canvas_element, chart_element], "Covid-19 Vaccination Simulation", model_params
)
server.port = 8521
