

class Base:

    def __init__(self):
        self.list_of_unassigned_soldiers = []
        self.list_of_dwellings = []
        self.list_of_assigned_soldiers = []


    def add_soldier(self, soldier):
        self.list_of_unassigned_soldiers.append(soldier)


    def add_dwelling(self, dwelling):
        self.list_of_dwellings.append(dwelling)


    def assignment_by_distance(self):
        self.list_of_unassigned_soldiers.sort(key = lambda x: x.distance_from_base, reverse = True)
        for dwellings in self.list_of_dwellings:
            dwellings.assign_room(self.list_of_unassigned_soldiers, self.list_of_assigned_soldiers)