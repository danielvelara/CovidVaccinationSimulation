from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from infected_person.agents import Person, Infected, Vaccine
from infected_person.schedule import RandomActivationByType


class InfectedPerson(Model):
    """
    Infected-Person Model
    """

    description = (
        "Agent-based modeling simulation using Python3 and Mesa Framework for simulating how the Covid-19 virus would spread depending on multiple variables such as vaccination, population density, age, mobility, and social distancing.\n Build by Andŕes Días de León and Daniel Velázquez"
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_people=100,
        infection_rate=0.33,
        death_rate = 0.12,
        recovery_rate = 0.30,
        initial_infected = 50,
        vaccine=False, 
        vaccine_spawned_time=500,
        immunity_from_vaccine=0.70, 
    ):
        
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_people = initial_people
        self.infection_rate = infection_rate
        self.death_rate = death_rate
        self.recovery_rate = recovery_rate
        self.initial_infected = initial_infected
        self.vaccine = vaccine
        self.vaccine_spawned_time = vaccine_spawned_time
        self.immunity_from_vaccine = immunity_from_vaccine

        self.schedule = RandomActivationByType(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Infected": lambda m: m.schedule.get_type_count(Infected),
                "Person": lambda m: m.schedule.get_type_count(Person),
            }
        )

        # Create Persons
        for i in range(self.initial_people):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            immunity = infection_rate
            person = Person(self.next_id(), (x, y), self, True, immunity)
            self.grid.place_agent(person, (x, y))
            self.schedule.add(person)

        # Create Infected
        for i in range(self.initial_infected):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            infected = Infected(self.next_id(), (x, y), self, True, immunity)
            self.grid.place_agent(infected, (x, y))
            self.schedule.add(infected)

        # Create vaccines
        if self.vaccine:
            for agent, x, y in self.grid.coord_iter():
                grown = self.random.choice([True, False, False, False, False, False, False, False, False, False])


                if grown:
                    countdown = self.vaccine_spawned_time
                else:
                    countdown = self.random.randrange(self.vaccine_spawned_time)

                patch = Vaccine(self.next_id(), (x, y), self, grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self, step_count=200):
        for i in range(step_count):
            self.step()