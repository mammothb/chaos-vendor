class GearSet(object):
    def __init__(self):
        gear_slot = ["belt", "boot", "chest", "glove", "helm", "neck",
                     "ring1", "ring2", "weap"]
        self._gear_set = {k: False for k in gear_slot}

    def reset_gear_set(self):
        self.__init__()

    def get_gear_set(self):
        return self._gear_set

    def set_gear_set(self, gear_set):
        self._gear_set = gear_set.get_gear_set()

    def set_gear(self, gear_piece, value):
        self._gear_set[gear_piece] = value
