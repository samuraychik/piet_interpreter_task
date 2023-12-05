try:
    from piet_vitvit.piet_vm import PietVM, CC, DP
    from piet_vitvit.piet_colors import HEX_COLORS, HEX_WHITE, HEX_BLACK
except ModuleNotFoundError:
    from piet_vm import PietVM, CC, DP
    from piet_colors import HEX_COLORS, HEX_WHITE, HEX_BLACK
finally:
    import sys
    from operator import itemgetter
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
    def __init__(self, filename, codel_size=1, debug=False, vmdebug=False):
        self.debug = debug
        self._debug_log("INTERPRETER DEBUG MODE ON")
        
        self.pvm = PietVM(vmdebug)
        self.step = 0
        self.codel_x = 0
        self.codel_y = 0
        self.block = [(0, 0)]
        
        self.filename = filename
        self.codel_size = codel_size
        self.image = Image.open(self.filename).convert("RGB")
        
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
    
    def piet_step(self):
        self.step += 1
        
        self._debug_log_step_start()
        self._debug_log_pvm_state()
        
        self.block = [(self.codel_x, self.codel_y)]
        self._add_adjacent_to_block(self.codel_x, self.codel_y)
        edge_x, edge_y = self._get_block_edge()
        self.pvm.current_value = len(self.block)
        
        seen_white = False
        iteration = 1
        
        while iteration <= 8:
            next_x, next_y = self._get_next_in_new_block(edge_x, edge_y)
            
            if not self._is_valid(next_x, next_y):
                iteration += 1
                self._turn_dp_and_cc(iteration)
                if self.matrix[edge_y][edge_x] != HEX_WHITE:
                    self.block = [(edge_x, edge_y)]
                    self._add_adjacent_to_block(edge_x, edge_y)
                    edge_x, edge_y = self._get_block_edge()
            
            elif self.matrix[next_y][next_x] == HEX_WHITE:
                if not seen_white:
                    seen_white = True
                    iteration = 1
                edge_x, edge_y = next_x, next_y
            
            else:
                if not seen_white:
                    command = self._get_command(next_x, next_y)
                    self._do_command(command)
                
                self.codel_x, self.codel_y = next_x, next_y
                self._debug_log_step_finish()
                self._debug_log_pvm_state()
                return
        else:
            self._debug_log("EXECUTION TRAPPED")
            sys.exit("trapped")
        
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
    
    def _get_command(self, new_x, new_y):
        old_color = HEX_COLORS[self.matrix[self.codel_y][self.codel_x]]
        new_color = HEX_COLORS[self.matrix[new_y][new_x]]
        self._debug_log_color_change(old_color, new_color)
        
        d_hue = new_color["hue"] - old_color["hue"]
        d_light = new_color["light"] - old_color["light"]
        return PIET_COMMANDS[d_hue % 6][d_light % 3]
    
    def _do_command(self, command):
        self._debug_log_command_sent(command)
        piet_command = getattr(self.pvm, command)
        piet_command()
        
    def _debug_log_step_start(self):
        if not self.debug:
            return
        self._debug_log("#" * 40)
        self._debug_log(f"START STEP {self.step}")
        
    def _debug_log_step_finish(self):
        if not self.debug:
            return
        self._debug_log(f"FINISH STEP {self.step}")
        
    def _debug_log_pvm_state(self):
        if not self.debug:
            return
        self._debug_log(f"DP:{self.pvm.dp.name}, " \
                        f"CC:{self.pvm.cc.name}, " \
                        f"STACK:{self.pvm.stack}")
        
    def _debug_log_color_change(self, old, new):
        self._debug_log(f"{old['light'].name} {old['hue'].name} -> " \
                        f"{new['light'].name} {new['hue'].name}")
    
    def _debug_log_command_sent(self, command):
        self._debug_log(f"DO {str.upper(command)}")
                
    def _debug_log(self, message):
        if self.debug:
            print(f"[INTER]: {message}")
            
    def _dispose(self):
        del self
