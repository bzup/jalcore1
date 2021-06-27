from .parser_helpers import *

# Code @generated by parsergen; do not edit!
from parsergen.parser_utils import GeneratedParser, TokenStream, Node, Filler
from parsergen.parser_utils import memoize, memoize_left_rec
from functools import reduce

class CustomParser(GeneratedParser):
    @memoize
    def program(self):
        pos = self.mark()
        parts = []
        for _ in range(1):
            part = self.block()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            # match:
            p = parts[0]
            return p
        self.goto(pos)
        
        return None
        
    @memoize_left_rec
    def block(self):
        pos = self.mark()
        parts = []
        for _ in range(1):
            part = self._loop_0()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            # match:
            stmts = parts[0]
            return Block(stmts)
        self.goto(pos)
        
        return None
        
    def _loop_0(self):
        children = []
        while True:
            pos = self.mark()
            part = self.statement()
            if self.match(part): children.append(part)
            else:
                self.goto(pos)
                break
        return children
    @memoize_left_rec
    def statement(self):
        pos = self.mark()
        parts = []
        for _ in range(1):
            part = self.expect('ID')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.expect('COLON')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            # match:
            i = parts[0]
            return JumpPoint(i.value)
        self.goto(pos)
        
        parts = []
        for _ in range(1):
            part = self.expect('INSTRUCTION')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.params()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            # match:
            opcode = parts[0]
            params = parts[1]
            return Instruction(opcode.value, params)
        self.goto(pos)
        
        parts = []
        for _ in range(1):
            part = self.expect('ID')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.params()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            # match:
            name = parts[0]
            params = parts[1]
            return MacroCall(name.value, params)
        self.goto(pos)
        
        parts = []
        for _ in range(1):
            part = self.expect('MACRO')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.expect('ID')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.params()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.expect('COLON')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.block()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.expect('ENDMACRO')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            # match:
            name = parts[1]
            params = parts[2]
            block = parts[4]
            return MacroDefinition(name.value, params, block)
        self.goto(pos)
        
        return None
        
    @memoize
    def params(self):
        pos = self.mark()
        parts = []
        for _ in range(1):
            part = self._maybe_1()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            # match:
            p = parts[0]
            return process_params(p)
        self.goto(pos)
        
        return None
        
    def _maybe_1(self):
        pos = self.mark()
        part = self._expr_list_2()
        if self.match(part): return part
        self.goto(pos)
        return Filler()
    def _expr_list_2(self):
        pos = self.mark()
        parts = []
        for _ in range(1):
            part = self.factor()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self._loop_3()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            return parts
        self.goto(pos)
        return None
    def _loop_3(self):
        children = []
        while True:
            pos = self.mark()
            part = self._expr_list_4()
            if self.match(part): children.append(part)
            else:
                self.goto(pos)
                break
        return children
    def _expr_list_4(self):
        pos = self.mark()
        parts = []
        for _ in range(1):
            part = self.expect('COMMA')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.factor()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            return parts
        self.goto(pos)
        return None
    @memoize_left_rec
    def factor(self):
        pos = self.mark()
        parts = []
        for _ in range(1):
            part = self.expect('LS_PAREN')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.factor()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.expect('RS_PAREN')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            # match:
            i = parts[1]
            return Address(i)
        self.goto(pos)
        
        parts = []
        for _ in range(1):
            part = self.expect('ID')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            predicate_pos = self.mark()
            part = self.expect('COLON')
            self.goto(predicate_pos)
            if self.match(part):
                self.fail()
                break
            # match:
            i = parts[0]
            return Register(i.value.lower()) if i.value.lower() in REGISTERS else JumpPointer(i.value)
        self.goto(pos)
        
        parts = []
        for _ in range(1):
            part = self.expect('MACRO_PARAM')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self._maybe_5()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            # match:
            i = parts[0]
            type_constraints = parts[1]
            return construct_macro_param(i.value, type_constraints)
        self.goto(pos)
        
        parts = []
        for _ in range(1):
            part = self.num()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            # match:
            i = parts[0]
            return i
        self.goto(pos)
        
        return None
        
    def _maybe_5(self):
        pos = self.mark()
        part = self._expr_list_6()
        if self.match(part): return part
        self.goto(pos)
        return Filler()
    def _expr_list_6(self):
        pos = self.mark()
        parts = []
        for _ in range(1):
            part = self.expect('LPAREN')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.expect('ID')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self._loop_7()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.expect('RPAREN')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            return parts
        self.goto(pos)
        return None
    def _loop_7(self):
        children = []
        while True:
            pos = self.mark()
            part = self._expr_list_8()
            if self.match(part): children.append(part)
            else:
                self.goto(pos)
                break
        return children
    def _expr_list_8(self):
        pos = self.mark()
        parts = []
        for _ in range(1):
            part = self.expect('COMMA')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            part = self.expect('ID')
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            return parts
        self.goto(pos)
        return None
    @memoize
    def num(self):
        pos = self.mark()
        parts = []
        for _ in range(1):
            part = self._or_9()
            if not self.match(part):
                self.fail()
                break
            parts.append(part)
            # match:
            i = parts[0]
            return Number(i.value)
        self.goto(pos)
        
        return None
        
    def _or_9(self):
        pos = self.mark()
        part = self.expect('INT')
        if self.match(part): return part
        self.goto(pos)
        part = self.expect('HEX')
        if self.match(part): return part
        self.goto(pos)
        part = self.expect('BIN')
        if self.match(part): return part
        self.goto(pos)
        self.fail()
        return None
