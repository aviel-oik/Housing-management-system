

class Room:
    def __init__(self, room_num, number_of_beds = 8):
        self.room_num = room_num
        self.number_of_beds = number_of_beds


    def add_soldier_to_room(self, soldier):
        self.number_of_beds -= 1
