class GearSet(object):
    def __init__(self):
        self._gear_set = {
            "belt": False,
            "boots": False,
            "chest": False,
            "gloves": False,
            "helmet": False,
            "neck": False,
            "ring1": False,
            "ring2": False,
            "weapon": False
        }

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
