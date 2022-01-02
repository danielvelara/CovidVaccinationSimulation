from mesa import Agent
from infected_person.random_walk import RandomWalker
import numpy as np


class Person(RandomWalker):
    """
    A person that walks around, gets infected
    The init is the same as the RandomWalker.
    """

    #Immunity will be a percentage that will be compared against a probability
    #If the prob is higher the person gets eliminated and replaced with an ifected
    immunity = None 
    hasTakenVaccine = False

    def __init__(self, unique_id, pos, model, moore, immunity=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.immunity = immunity

    def step(self):
        """
        A model step. Move, if vaccine avalaible take it
        """
        self.random_move()
        living = True

        if self.model.vaccine:
            #can decrease immunity over time, min would be 0
            if self.immunity > 0:
                self.immunity -= 0.05 
            if self.immunity < self.model.infection_rate:
                self.hasTakenVaccine = False

            # If there is vaccine available, take it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            vaccine_dose = [obj for obj in this_cell if isinstance(obj, Vaccine)][0]
            if vaccine_dose.grown and not self.hasTakenVaccine:
                self.immunity = self.model.immunity_from_vaccine
                self.hasTakenVaccine = True
                vaccine_dose.grown = False




class Infected(RandomWalker):
    """
    An Infected that walks around, reproduces and infects people.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()

        # If there are people present check possibility of infecting
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        people = [obj for obj in this_cell if isinstance(obj, Person)]
        if len(people) > 0:
            # people_to_infect = self.random.choice(people)
            for person in people:
                    print(f"immunity: {person.immunity}")
                    if self.random.random() > person.immunity: # Infect the person
                        print(f"infected")
                        # Delete people agent
                        self.model.grid._remove_agent(self.pos, person)
                        self.model.schedule.remove(person)
                        # add infected agent in same pos
                        newInfected = Infected(
                            self.model.next_id(), self.pos, self.model, self.moore, self.energy
                        )
                        self.model.grid.place_agent(newInfected, newInfected.pos)
                        self.model.schedule.add(newInfected)
                    else:
                        print("not infect")
        
        # Changing state to recovered, dead or stay the same
        state = np.random.choice(3, 1, p = [self.model.recovery_rate, self.model.death_rate, 1 - self.model.recovery_rate - self.model.death_rate])
        #recover
        if state[0] == 0:
            # Delete infected agent
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            #replace with a new person
            person = Person(
                self.model.next_id(), self.pos, self.model, self.moore, self.energy
            )
            self.model.grid.place_agent(person, person.pos)
            self.model.schedule.add(person)
        elif state[0] == 1:
            # Delete infected agent
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)


# Could implement Diferent Vaccines types the inherit from Vaccine Class
class Vaccine(Agent):
    """
    A Vaccines that spawns at a fixed rate and it is taken by persons
    """

    def __init__(self, unique_id, pos, model, grown, countdown):
        """
        Creates a new Vaccine

        Args:
            Spawned: (boolean) Whether the vaccines is spawned or not
            countdown: Time for the vaccine to be produced again
        """
        super().__init__(unique_id, model)
        self.grown = grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.grown:
            if self.countdown <= 0:
                # Set as grown
                self.grown = True
                self.countdown = self.model.vaccine_spawned_time
            else:
                self.countdown -= 1
