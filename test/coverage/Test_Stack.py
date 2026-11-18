# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 11:30:56 2025

@author: 2016570
"""

import py4hw
import pytest
from py4hw.cover import ToggleCoverage


class Test_Stack:

    @classmethod
    def setup_class(cls):
        hw = py4hw.HWSystem()

        din = hw.wire('din', 8)
        pre_dout = hw.wire('pre_dout', 8)
        dout = hw.wire('dout', 8)

        push = hw.wire('push')
        pop = hw.wire('pop')

        py4hw.Stack_ShiftRegister(hw, 'stack', din, pre_dout, dout, push, pop, None, None, 3)
        cls.cov = ToggleCoverage(hw)
        cls.circuit = (hw, din, dout, push, pop)

    def test_push_pop(self):
        hw, din, dout, push, pop = self.circuit
        sim = hw.getSimulator()

        din.put(7)                                    # apilar un valor
        push.put(1)
        pop.put(0)
        sim.clk(1)

        push.put(0)                                   # desapilarlo
        pop.put(1)
        sim.clk(1)
        assert(dout.get() == 7)

    def test_lifo(self):
        hw, din, dout, push, pop = self.circuit
        sim = hw.getSimulator()

        stack = []                                    # modelo de referencia
        for v in [1, 2, 3]:                           # apilar 1, 2, 3
            din.put(v)
            push.put(1)
            pop.put(0)
            sim.clk(1)
            stack.append(v)

        for _ in range(3):                            # salen en orden inverso: 3, 2, 1
            push.put(0)
            pop.put(1)
            sim.clk(1)
            assert(dout.get() == stack.pop())


if __name__ == '__main__':
    pytest.main(args=['-s', 'Test_Stack.py'])
