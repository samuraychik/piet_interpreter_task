import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from piet_vitvit import piet_interpreter as pinter

class PietInterpreterTestCase(unittest.TestCase):
    def tearDown(self) -> None:
        return self.inter._dispose()
    
    def test_init_correct(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\init_correct_64.png", 64)
        self.assertEqual(self.inter.codel_size, 64)
        self.assertEqual(self.inter.codel_x, 0)
        self.assertEqual(self.inter.codel_y, 0)
        self.assertEqual(self.inter.step, 0)
        self.assertEqual(self.inter.rows, 1)
        self.assertEqual(self.inter.rows, 1)
        
    def test_init_correct_matrix_1(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\correct_matrix_1_64.png", 64)
        self.assertEqual(self.inter.matrix, [["#000000"]])
    
    def test_init_correct_matrix_2(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\correct_matrix_2_64.png", 64)
        self.assertEqual(self.inter.matrix, [
            ["#ffffff", "#ffffff", "#ffffff"],
            ["#0000ff", "#0000ff", "#0000ff"],
            ["#ff0000", "#ff0000", "#ff0000"]])
        
    def test_find_adjacent_1(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\find_adjacent_1_64.png", 64)
        self.inter._add_adjacent_to_block(0, 0)
        self.assertCountEqual(self.inter.block, [
            (0, 0), (1, 0), (2, 0), (1, 1), (2, 1), (2, 2)])
        
    def test_find_adjacent_2(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\find_adjacent_2_64.png", 64)
        self.inter._add_adjacent_to_block(0, 0)
        self.assertCountEqual(self.inter.block, [
            (0, 0), (1, 0), (0, 1)])
        
    def test_find_edge_1(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\find_edge_1_64.png", 64)
        self.inter._add_adjacent_to_block(0, 0)
        edge = self.inter._get_block_edge()
        self.assertEqual(edge, (1, 0))
        
    def test_find_edge_2(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\find_edge_2_64.png", 64)
        self.inter._add_adjacent_to_block(0, 0)
        edge = self.inter._get_block_edge()
        self.assertEqual(edge, (4, 0))
        
    def test_end_execution_on_single_block(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\single_block_64.png", 64)
        with self.assertRaises(SystemExit) as ecm:
            self.inter.piet_step()
        self.assertEqual(ecm.exception.code, "trapped")
    
    def test_end_execution_on_trapped(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\execution_trapped_64.png", 64)
        with self.assertRaises(SystemExit) as ecm:
            for _ in range(3):
                self.inter.piet_step()
        self.assertEqual(ecm.exception.code, "trapped")
        
    def test_dont_break_on_endless_loop(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\endless_loop_64.png", 64)
        for _ in range(10000):
            self.inter.piet_step()
        self.assertEqual(self.inter.step, 10000)
        
    def test_example_program_1(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\example_1_64.png", 64)
        with self.assertRaises(SystemExit) as ecm:
            for _ in range(10000):
                self.inter.piet_step()
        self.assertEqual(ecm.exception.code, "trapped")
        self.assertEqual(self.inter.pvm.stack, [2])
    
    def test_example_program_2(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\example_2_64.png", 64)
        with self.assertRaises(SystemExit) as ecm:
            for _ in range(1000):
                self.inter.piet_step()
        self.assertEqual(ecm.exception.code, "trapped")
        self.assertEqual(self.inter.pvm.stack, [11])
    
    def test_example_program_3(self):
        self.inter = pinter.PietInterpreter(
            r"piet_vitvit_tests\test_images\example_3_64.png", 64)
        with self.assertRaises(SystemExit) as ecm:
            for _ in range(1000):
                self.inter.piet_step()
        self.assertEqual(ecm.exception.code, "trapped")
        self.assertEqual(self.inter.pvm.stack, [3, 1, 2])


if __name__ == "__main__":
    unittest.main()
