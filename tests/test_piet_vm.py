import os
import sys
import unittest
from contextlib import contextmanager

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from piet_vitvit import piet_vm as pvm


last_mocked_output = ""


def mock_print(output):
    global last_mocked_output
    last_mocked_output = str(output)


@contextmanager
def mocked_input(input):
    original_input = pvm.__builtins__["input"]
    pvm.__builtins__["input"] = lambda _: input
    yield
    pvm.__builtins__["input"] = original_input


@contextmanager
def mocked_print():
    original_print = pvm.__builtins__["print"]
    pvm.__builtins__["print"] = lambda output: mock_print(output)
    yield
    pvm.__builtins__["print"] = original_print


class PietVMCommandsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.vm = pvm.PietVM()

    def tearDown(self):
        self.vm._dispose()

    def test_pass(self):
        old_dp = self.vm.dp
        old_cc = self.vm.cc
        self.vm.piet_pass()
        self.assertEqual(self.vm.stack, [],
                         f"Stack has changed! ([] -> {self.vm.stack})")
        self.assertEqual(self.vm.dp, old_dp,
                         f"DP has changed! ({old_dp} -> {self.vm.dp})")
        self.assertEqual(self.vm.cc, old_cc,
                         f"CC has changed! ({old_cc} -> {self.vm.cc})")

    def test_push(self):
        self.vm.current_value = 42
        self.vm.piet_push()
        self.assertEqual(self.vm.stack, [42])

    def test_pop(self):
        self.vm.stack = [7, 42]
        self.vm.piet_pop()
        self.assertEqual(self.vm.stack, [7])

    def test_add(self):
        self.vm.stack = [7, 42]
        self.vm.piet_add()
        self.assertEqual(self.vm.stack, [49])

    def test_sub(self):
        self.vm.stack = [7, 42]
        self.vm.piet_sub()
        self.assertEqual(self.vm.stack, [-35])

    def test_mul(self):
        self.vm.stack = [7, 42]
        self.vm.piet_mul()
        self.assertEqual(self.vm.stack, [294])

    def test_div_1(self):
        self.vm.stack = [7, 42]
        self.vm.piet_div()
        self.assertEqual(self.vm.stack, [0])

    def test_div_2(self):
        self.vm.stack = [42, 7]
        self.vm.piet_div()
        self.assertEqual(self.vm.stack, [6])

    def test_mod_1(self):
        self.vm.stack = [7, 42]
        self.vm.piet_mod()
        self.assertEqual(self.vm.stack, [7])

    def test_mod_2(self):
        self.vm.stack = [42, 7]
        self.vm.piet_mod()
        self.assertEqual(self.vm.stack, [0])

    def test_not_on_nonzero(self):
        self.vm.stack = [42]
        self.vm.piet_not()
        self.assertEqual(self.vm.stack, [0])

    def test_not_on_zero(self):
        self.vm.stack = [0]
        self.vm.piet_not()
        self.assertEqual(self.vm.stack, [1])

    def test_gt_on_less(self):
        self.vm.stack = [7, 42]
        self.vm.piet_gt()
        self.assertEqual(self.vm.stack, [0])

    def test_gt_on_equal(self):
        self.vm.stack = [42, 42]
        self.vm.piet_gt()
        self.assertEqual(self.vm.stack, [0])

    def test_gt_on_greater(self):
        self.vm.stack = [42, 7]
        self.vm.piet_gt()
        self.assertEqual(self.vm.stack, [1])

    def test_pointer_on_clockwise(self):
        self.vm.stack = [1]
        self.vm.dp = pvm.DP.RIGHT
        self.vm.piet_pointer()
        self.assertEqual(self.vm.dp, pvm.DP.DOWN)

    def test_pointer_on_counterclockwise(self):
        self.vm.stack = [-1]
        self.vm.dp = pvm.DP.RIGHT
        self.vm.piet_pointer()
        self.assertEqual(self.vm.dp, pvm.DP.UP)

    def test_pointer_should_pop(self):
        self.vm.stack = [42]
        self.vm.piet_pointer()
        self.assertEqual(self.vm.stack, [],
                         "pointer() should pop from stack!")

    def test_switch(self):
        self.vm.stack = [1]
        self.vm.cc = pvm.CC.RIGHT
        self.vm.piet_switch()
        self.assertEqual(self.vm.cc, pvm.CC.LEFT)

    def test_switch_should_pop(self):
        self.vm.stack = [42]
        self.vm.piet_switch()
        self.assertEqual(self.vm.stack, [],
                         "switch() should pop from stack!")

    def test_dup(self):
        self.vm.stack = [42]
        self.vm.piet_dup()
        self.assertEqual(self.vm.stack, [42, 42])

    def test_roll_1(self):
        self.vm.stack = [10, 20, 30, 2, 1]
        self.vm.piet_roll()
        self.assertEqual(self.vm.stack, [10, 30, 20])

    def test_roll_2(self):
        self.vm.stack = [10, 20, 30, 40, 50, 4, 3]
        self.vm.piet_roll()
        self.assertEqual(self.vm.stack, [10, 30, 40, 50, 20])

    def test_roll_reverse(self):
        self.vm.stack = [10, 20, 30, 40, 50, 4, -3]
        self.vm.piet_roll()
        self.assertEqual(self.vm.stack, [10, 50, 20, 30, 40])

    def test_roll_on_nonpositive_depth(self):
        self.vm.stack = [10, 20, 30, 40, 50, -4, 3]
        self.vm.piet_roll()
        self.assertEqual(self.vm.stack, [10, 20, 30, 40, 50],
                         "Shouldn skip on non-positive depth!")

    def test_roll_on_nonpositive_depth(self):
        self.vm.stack = [10, 20, 30, 40, 50, -4, 3]
        self.vm.piet_roll()
        self.assertEqual(self.vm.stack, [10, 20, 30, 40, 50],
                         "Should skip on non-positive depth!")

    def test_innum(self):
        with mocked_input("42"):
            self.vm.stack = []
            self.vm.piet_innum()
            self.assertEqual(self.vm.stack, [42])

    def test_innum_on_bad_input(self):
        with mocked_input("bad input"):
            self.vm.stack = []
            self.vm.piet_innum()
            self.assertEqual(self.vm.stack, [],
                             "Should skip on bad input!")

    def test_inchar(self):
        with mocked_input("*"):
            self.vm.stack = []
            self.vm.piet_inchar()
            self.assertEqual(self.vm.stack, [42])

    def test_inchar_on_bad_input(self):
        with mocked_input("bad input"):
            self.vm.stack = []
            self.vm.piet_inchar()
            self.assertEqual(self.vm.stack, [],
                             "Should skip on bad input!")

    def test_outnum(self):
        with mocked_print():
            self.vm.stack = [42]
            self.vm.piet_outnum()
            self.assertEqual(last_mocked_output, "42")

    def test_outnum_should_pop(self):
        with mocked_print():
            self.vm.stack = [42]
            self.vm.piet_outnum()
            self.assertEqual(self.vm.stack, [],
                             "outnum() should pop from stack!")

    def test_outchar(self):
        with mocked_print():
            self.vm.stack = [42]
            self.vm.piet_outchar()
            self.assertEqual(last_mocked_output, "*")

    def test_outchar_should_pop(self):
        with mocked_print():
            self.vm.stack = [42]
            self.vm.piet_outchar()
            self.assertEqual(self.vm.stack, [],
                             "outchar() should pop from stack!")


if __name__ == "__main__":
    unittest.main()
