from classes.room import Room

class Dwellings:

    def __init__(self, building_number, number_of_room = 10, number_of_beds_per_room = 8):
        self.building_number = building_number
        self.number_of_room = number_of_room
        self.number_of_beds_per_room = number_of_beds_per_room

        self.list_of_rooms = []
        for i in range(number_of_room):
            self.list_of_rooms.append(Room(i+1))


    def assign_room(self, list_of_unassigned_soldier, list_of_assigned_soldiers):
        for room in self.list_of_rooms:
            for i in range(self.number_of_beds_per_room):
                if len(list_of_unassigned_soldier) > 0:
                    soldier = list_of_unassigned_soldier.pop(0)
                    soldier.assignment_status = True
                    soldier.dwellings_assigned = self.building_number
                    room.add_soldier_to_room(soldier)
                    soldier.room_assigned = room.room_num
                    list_of_assigned_soldiers.append(soldier)
                else:
                    return





