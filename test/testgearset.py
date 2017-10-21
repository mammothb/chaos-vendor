import inspect
import os
import sys
import unittest

# To allow import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gearset # pylint: disable=E0401,C0413

class TestGearSet(unittest.TestCase):
    """Runs all tests when run as part of a suite"""
    def runTest(self):  # pylint: disable=C0103
        print("\nRunning %s" % self.__class__.__name__)
        self.test_constructor()
        self.test_reset_gear_set()
        self.test_toggle_gear()
        self.test_set_gear_set()

    def test_constructor(self):
        """Test class constructor"""
        print("  - %s" % inspect.stack()[0][3])
        gear_set = gearset.GearSet()
        gears = gear_set.get_gear_set()
        # Check variables
        self.assertEqual(False, gears["belt"])
        self.assertEqual(False, gears["boots"])
        self.assertEqual(False, gears["chest"])
        self.assertEqual(False, gears["gloves"])
        self.assertEqual(False, gears["helmet"])
        self.assertEqual(False, gears["neck"])
        self.assertEqual(False, gears["ring1"])
        self.assertEqual(False, gears["ring2"])
        self.assertEqual(False, gears["weapon"])

    def test_reset_gear_set(self):
        """Test reset_gear_set() method"""
        print("  - %s" % inspect.stack()[0][3])
        gear_set = gearset.GearSet()
        gear_set.toggle_gear("belt")
        gear_set.toggle_gear("boots")
        gear_set.toggle_gear("chest")
        gear_set.toggle_gear("gloves")
        gear_set.toggle_gear("helmet")
        gear_set.toggle_gear("neck")
        gear_set.toggle_gear("ring1")
        gear_set.toggle_gear("ring2")
        gear_set.toggle_gear("weapon")
        gear_set.reset_gear_set()
        gears = gear_set.get_gear_set()
        # Check variables
        self.assertEqual(False, gears["belt"])
        self.assertEqual(False, gears["boots"])
        self.assertEqual(False, gears["chest"])
        self.assertEqual(False, gears["gloves"])
        self.assertEqual(False, gears["helmet"])
        self.assertEqual(False, gears["neck"])
        self.assertEqual(False, gears["ring1"])
        self.assertEqual(False, gears["ring2"])
        self.assertEqual(False, gears["weapon"])

    def test_toggle_gear(self):
        """Test reset_gear_set() method"""
        print("  - %s" % inspect.stack()[0][3])
        gear_set = gearset.GearSet()
        gear_set.toggle_gear("belt")
        gear_set.toggle_gear("boots")
        gear_set.toggle_gear("chest")
        gear_set.toggle_gear("gloves")
        gear_set.toggle_gear("helmet")
        gear_set.toggle_gear("neck")
        gear_set.toggle_gear("ring1")
        gear_set.toggle_gear("ring2")
        gear_set.toggle_gear("weapon")
        gears = gear_set.get_gear_set()
        # Check variables
        self.assertEqual(True, gears["belt"])
        self.assertEqual(True, gears["boots"])
        self.assertEqual(True, gears["chest"])
        self.assertEqual(True, gears["gloves"])
        self.assertEqual(True, gears["helmet"])
        self.assertEqual(True, gears["neck"])
        self.assertEqual(True, gears["ring1"])
        self.assertEqual(True, gears["ring2"])
        self.assertEqual(True, gears["weapon"])

    def test_set_gear_set(self):
        """Test set_gear_set() method"""
        print("  - %s" % inspect.stack()[0][3])
        gear_set_1 = gearset.GearSet()
        gear_set_2 = gearset.GearSet()
        gear_set_1.toggle_gear("belt")
        gear_set_1.toggle_gear("boots")
        gear_set_1.toggle_gear("chest")
        gear_set_1.toggle_gear("gloves")
        gear_set_1.toggle_gear("helmet")
        gear_set_1.toggle_gear("neck")
        gear_set_1.toggle_gear("ring1")
        gear_set_1.toggle_gear("ring2")
        gear_set_1.toggle_gear("weapon")
        gear_set_2.set_gear_set(gear_set_1)
        gears = gear_set_2.get_gear_set()
        # Check variables
        self.assertEqual(True, gears["belt"])
        self.assertEqual(True, gears["boots"])
        self.assertEqual(True, gears["chest"])
        self.assertEqual(True, gears["gloves"])
        self.assertEqual(True, gears["helmet"])
        self.assertEqual(True, gears["neck"])
        self.assertEqual(True, gears["ring1"])
        self.assertEqual(True, gears["ring2"])
        self.assertEqual(True, gears["weapon"])
