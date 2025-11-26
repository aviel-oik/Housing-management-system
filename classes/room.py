class Room:

    def __init__(self, room_num, number_of_beds = 8):
        self.room_num = room_num
        self.number_of_beds = number_of_beds
        self.space = "empty"

    def add_soldier_to_room(self, soldier):
        self.space = "part"
        self.number_of_beds -= 1
        if self.number_of_beds == 0:
            self.space = "full"



