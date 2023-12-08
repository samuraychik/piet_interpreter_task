try:
    from piet_vitvit.piet_vm import PietVM, CC, DP
    from piet_vitvit.piet_colors import HEX_COLORS, HEX_WHITE, HEX_BLACK
except ModuleNotFoundError:
    from piet_vm import PietVM, CC, DP
    from piet_colors import HEX_COLORS, HEX_WHITE, HEX_BLACK
finally:
    import sys
    from operator import itemgetter
    from os.path import abspath
    from PIL import Image


PIET_COMMANDS = [
    ["piet_pass", "piet_push", "piet_pop"],
    ["piet_add", "piet_sub", "piet_mul"],
    ["piet_div", "piet_mod", "piet_not"],
    ["piet_gt", "piet_pointer", "piet_switch"],
    ["piet_dup", "piet_roll", "piet_innum"],
    ["piet_inchar", "piet_outnum", "piet_outchar"],
    ]


class PietInterpreter:
    def __init__(self, filename, codel_size=1):
        self.pvm = PietVM()
        self.step = 0
        self.curr_x, self.curr_y = 0, 0
        self.edge_x, self.edge_y = 0, 0
        self.next_x, self.next_y = 0, 0
        self.block = [(0, 0)]
        self.seen_white = False

        self.filename = filename
        self.codel_size = codel_size
        self.image = Image.open(abspath(self.filename)).convert("RGB")

        image_size_x, image_size_y = self.image.size
        self.cols = image_size_x // codel_size
        self.rows = image_size_y // codel_size
        self.matrix = [[0 for x in range(self.cols)]
                       for y in range(self.rows)]

        for x in range(self.cols):
            for y in range(self.rows):
                r, g, b = self.image.getpixel((x * codel_size,
                                               y * codel_size))
                self.matrix[y][x] = f"#{r:02x}{g:02x}{b:02x}"
        self.debug = False

    def piet_step(self):
        self.step += 1
        self._debug_log("-" * 40)
        self._debug_log(f"START STEP {self.step}")
        self._debug_action_prompt()

        self._piet_get_curr()
        self._debug_log_state()
        self._debug_action_prompt()

        self._piet_get_next()

        self._piet_move()
        self.pvm.debug_log_stack()
        self._debug_action_prompt()

        self._debug_log(f"END STEP {self.step}")
        self._debug_action_prompt()

    def start_debug(self):
        self.debug = True
        self.pvm.debug = True

    def stop_debug(self):
        self.debug = False
        self.pvm.debug = False

    def _piet_get_curr(self):
        self.block = [(self.curr_x, self.curr_y)]
        self._add_adjacent_to_block(self.curr_x, self.curr_y)
        self.edge_x, self.edge_y = self._get_block_edge()
        self.pvm.current_value = len(self.block)

    def _piet_get_next(self):
        iteration = 1
        self.seen_white = False
        while iteration <= 8:
            self.next_x, self.next_y = self._get_next_in_new_block(
                self.edge_x, self.edge_y)
            self._debug_log_looking_at_next()
            self._debug_action_prompt()

            if not self._is_valid(self.next_x, self.next_y):
                self._debug_log("Can't move there. Rotating...")
                iteration += 1
                self._turn_dp_and_cc(iteration)
                if self.matrix[self.edge_y][self.edge_x] != HEX_WHITE:
                    self.block = [(self.edge_x, self.edge_y)]
                    self._add_adjacent_to_block(self.edge_x, self.edge_y)
                    self.edge_x, self.edge_y = self._get_block_edge()

            elif self.matrix[self.next_y][self.next_x] == HEX_WHITE:
                self._debug_log("Entered WHITE. Passing through...")
                if not self.seen_white:
                    self.seen_white = True
                    iteration = 1
                self.edge_x, self.edge_y = self.next_x, self.next_y

            else:
                self._debug_log("Moving there...")
                return
        else:
            self._debug_log("Execution trapped!")
            sys.exit("trapped")

    def _piet_move(self):
        if not self.seen_white:
            command = self._get_command()
            self._do_command(command)
            self.curr_x, self.curr_y = self.next_x, self.next_y

    def _is_valid(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows \
            and self.matrix[y][x] != HEX_BLACK

    def _add_adjacent_to_block(self, x, y):
        for dx, dy in (0, -1), (0, 1), (-1, 0), (1, 0):
            if (x + dx, y + dy) not in self.block \
                and self._is_valid(x + dx, y + dy) \
                    and self.matrix[y][x] == self.matrix[y + dy][x + dx]:
                self.block.append((x + dx, y + dy))
                self._add_adjacent_to_block(x + dx, y + dy)

    def _get_block_edge(self):
        key1 = 1 - self.pvm.dp % 2
        key2 = 1 - key1
        rev1 = not(self.pvm.dp % 2 - int(self.pvm.cc < 0))
        rev2 = self.pvm.dp < 2
        self.block.sort(key=itemgetter(key1), reverse=rev1)
        self.block.sort(key=itemgetter(key2), reverse=rev2)
        return self.block[0]

    def _get_next_in_new_block(self, x, y):
        if self.pvm.dp == DP.RIGHT:
            x += 1
        elif self.pvm.dp == DP.DOWN:
            y += 1
        elif self.pvm.dp == DP.LEFT:
            x -= 1
        elif self.pvm.dp == DP.UP:
            y -= 1
        return x, y

    def _turn_dp_and_cc(self, iteration_number):
        if iteration_number % 2:
            self.pvm.dp = DP((self.pvm.dp + 1) % 4)
        else:
            self.pvm.cc = CC(self.pvm.cc * -1)
        self._debug_log

    def _get_command(self):
        old_color = HEX_COLORS[self.matrix[self.curr_y][self.curr_x]]
        new_color = HEX_COLORS[self.matrix[self.next_y][self.next_x]]
        self._debug_log_color_shift(old_color, new_color)

        d_hue = new_color["hue"] - old_color["hue"]
        d_light = new_color["light"] - old_color["light"]
        return PIET_COMMANDS[d_hue % 6][d_light % 3]

    def _do_command(self, command):
        piet_command = getattr(self.pvm, command)
        piet_command()

    def _debug_log(self, message):
        if self.debug:
            print(f"[INTER] {message}")

    def _debug_log_state(self):
        self._debug_log("CURRENT STATE:")
        self._debug_log(f"pos: {self.curr_x, self.curr_y}")
        self._debug_log(f"block: {self.block}")
        self.pvm.debug_log_value()
        self.pvm.debug_log_stack()

    def _debug_log_looking_at_next(self):
        self.pvm.debug_log_direction()
        self._debug_log(f"current edge: {self.edge_x, self.edge_y}")
        self._debug_log(f"looking at: {self.next_x, self.next_y}")

    def _debug_log_color_shift(self, old, new):
        self._debug_log(f"{old['light'].name} {old['hue'].name} -> "
                        f"{new['light'].name} {new['hue'].name}")

    def _debug_action_prompt(self):
        if (self.debug):
            input("...")

    def _dispose(self):
        del self
