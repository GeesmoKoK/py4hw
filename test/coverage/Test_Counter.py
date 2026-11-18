# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 08:55:35 2022

@author: dcr
"""

import py4hw
import py4hw.debug
import pytest
from py4hw.cover import ToggleCoverage


class Test_Counter:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        reset = sys.wire('reset')
        inc = sys.wire('inc')
        q = sys.wire('q', 32)
        py4hw.Counter(sys, 'counter', reset, inc, q)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, reset, inc, q)

    def test_integrity(self):
        sys = py4hw.HWSystem()

        reset = sys.wire('reset')
        inc = sys.wire('inc')
        q = sys.wire('q', 32)

        py4hw.Constant(sys, 'reset', 0, reset)
        py4hw.Constant(sys, 'inc', 1, inc)


        py4hw.Counter(sys, 'counter', reset, inc, q )


        py4hw.debug.checkIntegrity(sys)

    def test_reset_inc(self):
        sys, reset, inc, q = self.circuit
        sim = sys.getSimulator()

        exp = 0                                  
        for r_v, i_v in [(1, 0), (0, 1), (0, 1), (0, 1), (0, 0), (0, 1), (1, 1), (0, 1), (0, 0), (0, 1)]:
            reset.put(r_v)
            inc.put(i_v)
            sim.clk(1)
            if r_v:
                exp = 0                      
            elif i_v:
                exp = exp + 1
            assert(q.get() == exp)

class Test_ModuloCounter:

    @classmethod
    def setup_class(cls):
        hw = py4hw.HWSystem()
        reset = hw.wire('reset')
        inc = hw.wire('inc')
        qm = hw.wire('qm', 8)
        carryout = hw.wire('carryout')
        py4hw.ModuloCounter(hw, 'modcounter', 5, reset, inc, qm, carryout)
        cls.cov = ToggleCoverage(hw)
        cls.circuit = (hw, reset, inc, qm, carryout)

    def test_integrity(self):
        hw = py4hw.HWSystem()

        reset = hw.wire('reset')
        inc = hw.wire('inc')
        q = hw.wire('q', 32)
        carryout = hw.wire('carryout')

        py4hw.Constant(hw, 'reset', 0, reset)
        py4hw.Constant(hw, 'inc', 1, inc)

        py4hw.ModuloCounter(hw, 'counter', 5, reset,  inc, q, carryout )

        py4hw.debug.checkIntegrity(hw)

    def test_count(self):
        hw, reset, inc, qm, carryout = self.circuit

        reset.put(1)   
        inc.put(0)
        hw.getSimulator().clk()
        reset.put(0)
        inc.put(1)

        hw.getSimulator().clk()
        assert(qm.get() == 1)
        hw.getSimulator().clk(3)
        assert(qm.get() == 4)
        hw.getSimulator().clk()
        assert(qm.get() == 0)


    def test_carryout(self):
        hw, reset, inc, qm, carryout = self.circuit
        sim = hw.getSimulator()

        reset.put(1)   
        inc.put(0)
        sim.clk()
        reset.put(0)

        exp = 0                                   
        for i_v in [1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1]:
            inc.put(i_v)
            sim.clk(1)
            if i_v:
                exp = (exp + 1) % 5
            assert(qm.get() == exp)
            assert(carryout.get() == int(exp == 4))

if __name__ == '__main__':
    pytest.main(args=['-q', 'Test_Counter.py'])
