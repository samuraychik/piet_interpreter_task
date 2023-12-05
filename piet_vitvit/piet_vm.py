from enum import IntEnum


class DP(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    
    
class CC(IntEnum):
    LEFT = -1
    RIGHT = 1


class PietVM:
    def __init__(self, debug=False):
        self.debug = debug
        self.dp = DP.RIGHT
        self.cc = CC.LEFT
        self.stack = []
        self.current_value = 1
        
    def piet_pass(self):
        self._debug_print("PASS")
        pass
    
    def piet_push(self):
        self.stack.append(self.current_value)
        self._debug_print(f"PUSH {self.current_value}")
        
    def piet_pop(self):
        top = self._safe_pop()
        if top:
            self._debug_print(f"POP {top}")
    
    def piet_add(self):
        top1 = self._safe_pop()
        top2 = self._safe_pop()
        if not (top1 and top2):
            return
        self.stack.append(top2 + top1)
        self._debug_print(f"ADD {top2}+{top1}")
        
    def piet_sub(self):
        top1 = self._safe_pop()
        top2 = self._safe_pop()
        if not (top1 and top2):
            return
        self.stack.append(top2 - top1)
        self._debug_print(f"SUB {top2}-{top1}")
        
    def piet_mul(self):
        top1 = self._safe_pop()
        top2 = self._safe_pop()
        if not (top1 and top2):
            return
        self.stack.append(top2 * top1)
        self._debug_print(f"MUL {top2}*{top1}")
        
    def piet_div(self):
        top1 = self._safe_pop()
        top2 = self._safe_pop()
        if not (top1 and top2):
            return
        self.stack.append(top2 // top1)
        self._debug_print(f"DIV {top2}/{top1}")
    
    def piet_mod(self):
        top1 = self._safe_pop()
        top2 = self._safe_pop()
        if not (top1 and top2):
            return
        self.stack.append(top2 % top1)
        self._debug_print(f"MOD {top2}%{top1}")
        
    def piet_not(self):
        top = self._safe_pop()
        if not top and top != 0:
            return
        self.stack.append(int(not top))
        self._debug_print(f"NOT {top}")
        
    def piet_gt(self):
        top1 = self._safe_pop()
        top2 = self._safe_pop()
        if not (top1 and top2):
            return
        self.stack.append(int(top2 > top1))
        self._debug_print(f"GT {top2}>{top1}")
        
    def piet_pointer(self):
        top = self._safe_pop()
        if not top:
            return
        self.dp = DP((self.dp + top) % 4)
        self._debug_print(f"POINTER {self.dp.name}")
        
    def piet_switch(self):
        top = self._safe_pop()
        if not top:
            return
        self.cc = CC(self.cc * (-1 ** top))
        self._debug_print(f"SWITCH {self.cc.name}")
        
    def piet_dup(self):
        top = self._safe_pop()
        if not top:
            return
        self.stack.append(top)
        self.stack.append(top)
        self._debug_print(f"DUP {top}")
        
    def piet_roll(self):
        top1 = self._safe_pop()
        top2 = self._safe_pop()
        num = top1 % top2
        if top2 <= 0 or num == 0:
            return
        x = -abs(num) + top2 * (num < 0)
        self.stack[-top2:] = self.stack[x:] + self.stack[-top2:x]
        self._debug_print(f"ROLL {top1} {top2}")
    
    def piet_innum(self):
        try:
            number = int(input("Reading number: "))
        except ValueError:
            return
        self.stack.append(number)
        self._debug_print(f"INNUM {number}")
        
    def piet_inchar(self):
        try:
            char = ord(input("Reading character: "))
        except TypeError:
            return
        self.stack.append(char)
        self._debug_print(f"INCHAR {char}")
    
    def piet_outnum(self):
        top = self._safe_pop()
        if not top:
            return
        print(top)
        self._debug_print(f"OUTNUM {top}")
        
    def piet_outchar(self):
        top = self._safe_pop()
        if not top:
            return
        print(chr(top))
        self._debug_print(f"OUTCHAR {top}")
        
    def _safe_pop(self):
        if not self.stack:
            self._debug_print("Stack underflow!")
            return
        return self.stack.pop()
    
    def _debug_print(self, message):
        if self.debug:
            print(f"[VM]: {message}")
            
    def _dispose(self):
        del self
            