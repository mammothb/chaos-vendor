class GearSet(object):
    def __init__(self):
        gear_slot = ["belt", "boots", "chest", "gloves", "helmet", "neck",
                     "ring1", "ring2", "weapon"]
        self._gear_set = {k: False for k in gear_slot}

    def reset_gear_set(self):
        self.__init__()

    def toggle_gear(self, gear_piece):
        self._gear_set[gear_piece] ^= True

    def get_gear_set(self):
        return self._gear_set

    def set_gear_set(self, gear_set):
        self._gear_set = gear_set.get_gear_set()

    def set_gear(self, gear_piece, value):
        self._gear_set[gear_piece] = value


def main():
    gear_1 = GearSet()
    print(gear_1.get_gear_set())
    gear_1.toggle_gear("belt")
    print(gear_1.get_gear_set())
    # gear_1.toggle_gear("belt")
    # print(gear_1.get_gear_set())
    gear_1.reset_gear_set()
    print(gear_1.get_gear_set())

if __name__ == "__main__":
    main()
