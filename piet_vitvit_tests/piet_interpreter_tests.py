import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from piet_vitvit import piet_interpreter as pinter

class PietInterpreterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.inter = pinter.PietInterpreter("placeholder")
    
    def tearDown(self) -> None:
        self.inter._dispose
        
    # TO-DO


if __name__ == "__main__":
    unittest.main()
