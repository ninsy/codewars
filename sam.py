# https://www.codewars.com/kata/54c1bf903f0696f04600068b/train/python - 4kyu

# Test
class Machine(object):
    
    REGISTERS = ['a', 'b', 'c', 'd']

    def __init__(self, cpu):
        self.cpu = cpu

        # self.cpu.read_reg(self, name): Returns the value of the named register.
        # self.cpu.write_reg(self, name, value): Stores the value into the given register.

        # self.cpu.pop_stack(self): Pops the top element of the stack, returning the value.
        # self.cpu.write_stack(self, value): Pushes an element onto the stack.

    # STACK OPS

    # TODO: stack ops shares interface with arithmetic ops for simplicity, may be refactored later on...
    def handle_push(self, arg, arg2, suffix):
        if isinstance(arg, int):
            self.cpu.write_stack(arg)
        else:
            val = self.cpu.read_reg(arg)
            self.cpu.write_stack(val)
    
    def handle_pop(self, arg, arg2, suffix):
        self.cpu.pop_stack()

    def handle_pushr(self, arg, arg2, suffix):
        pass

    def handle_pushrr(self, arg, arg2, suffix):
        pass

    def handle_popr(self, arg, arg2, suffix):
        pass

    def handle_poprr(self, arg, arg2, suffix):
        pass

    # ARITHMETIC OPS

    def _handle_arithm(self, arg, arg2, suffix, op):
        if suffix is True:
            v = self.cpu.read_reg('a')
            self.cpu.write_stack(v)
        tmp = self.cpu.pop_stack()
        count = self.get_count(arg)
        for i in range(count-1):
            tmp = op(tmp)
        self.cpu.write_reg('a' if arg2 is None else arg2, int(tmp))

    def handle_add(self, **kw):
        op = lambda x: x + self.cpu.pop_stack()
        return self._handle_arithm(**{**kw, 'op': op})

    def handle_sub(self, **kw):
        op = lambda x: x - self.cpu.pop_stack()
        return self._handle_arithm(**{**kw, 'op': op})

    def handle_mul(self, **kw):
        op = lambda x: x * self.cpu.pop_stack()
        return self._handle_arithm(**{**kw, 'op': op})

    def handle_div(self, **kw):
        op = lambda x: x / self.cpu.pop_stack()
        return self._handle_arithm(**{**kw, 'op': op})

    def handle_and(self, arg, arg2, suffix):
        pass    

    def handle_or(self, arg, arg2, suffix):
        pass

    def handle_xor(self, arg, arg2, suffix):
        pass
    

    # MISC OPS

    def handle_mov(self, arg, arg2):
        pass

    # UTILS

    def get_count(self, arg):
        if isinstance(arg, int):
            return arg
        else:
            return self.cpu.read_reg(arg)


    def try_parse_int(self, x):
        try:
            return int(x)
        except ValueError:
            return x

    def parse_args(self, instr, suffix=False):
        parsed_no_op = instr.split(' ')[1:]
        if len(parsed_no_op) == 1:
            return {
                'arg': self.try_parse_int(parsed_no_op[0]),
                'arg2': None,
                'suffix': suffix
            }
        elif len(parsed_no_op) == 2:
            return {
                'arg': self.try_parse_int(parsed_no_op[0].strip(',')),
                'arg2': self.try_parse_int(parsed_no_op[1]),
                'suffix': suffix
            }
        elif len(parsed_no_op) == 0:
            return {
                'arg': None,
                'arg2': None,
                'suffix': suffix
            }


    def execute(self, instr):
        op = instr.split(' ')[0]
        args_dict = self.parse_args(instr)
        # STACK OPS
        if op == 'push':
            self.handle_push(**args_dict)
        elif op == 'pop':
            self.handle_pop()
        elif op == 'pushr':
            self.handle_pushr()
        elif op == 'pushrr':
            self.handle_pushrr()
        elif op == 'popr':
            self.handle_popr()
        elif op == 'poprr':
            self.handle_poprr()
        # ARITHM OPS
        elif op == 'add' or op == 'addr':
            args_dict = self.parse_args(instr, suffix=op=='addr')
            self.handle_add(**args_dict)
        elif op == 'sub' or op == 'subr':
            args_dict = self.parse_args(instr, suffix=op=='subr')
            self.handle_sub(**args_dict)
        elif op == 'mul' or op == 'mulr':
            args_dict = self.parse_args(instr, suffix=op=='mulr')
            self.handle_mul(**args_dict)
        elif op == 'div' or op == 'divr':
            args_dict = self.parse_args(instr, suffix=op=='divr')
            self.handle_div(**args_dict)
        elif op == 'and' or op == 'andr':
            args_dict = self.parse_args(instr, suffix=op=='andr')
            self.handle_and(**args_dict)
        elif op == 'or' or op == 'orr':
            args_dict = self.parse_args(instr, suffix=op=='orr')
            self.handle_or(**args_dict)
        elif op == 'xor' or op == 'xorr':
            args_dict = self.parse_args(instr, suffix=op=='xorr')
            self.handle_xor(**args_dict)
        # MISC OPS
        elif op == 'mov':
            self.handle_mov()