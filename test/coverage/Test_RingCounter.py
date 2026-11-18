# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 08:50:24 2026

@author: dcr
"""


import py4hw
import py4hw.debug
import pytest
from py4hw.cover import ToggleCoverage


class Test_RingCounter:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        reset = sys.wire('reset')
        enable = sys.wire('enable')
        q = sys.wire('q', 8)
        q_init = sys.wire('q_init', 8)
        py4hw.RingCounter(sys, 'ringcounter', reset, enable, q)
        py4hw.RingCounter(sys, 'ringcounter_init', reset, enable, q_init, init=1)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, reset, enable, q, q_init)

    def test_integrity(self):
        sys = py4hw.HWSystem()

        reset = sys.wire('reset')
        enable = sys.wire('enable')
        q = sys.wire('q', 8)

        py4hw.Constant(sys, 'reset', 0, reset)
        py4hw.Constant(sys, 'enable', 1, enable)

        py4hw.RingCounter(sys, 'ringcounter', reset, enable, q)

        py4hw.debug.checkIntegrity(sys)

    def test_integrity_init(self):
        sys = py4hw.HWSystem()

        reset = sys.wire('reset')
        enable = sys.wire('enable')
        q = sys.wire('q', 8)

        py4hw.Constant(sys, 'reset', 0, reset)
        py4hw.Constant(sys, 'enable', 1, enable)

        py4hw.RingCounter(sys, 'ringcounter', reset, enable, q, init=1)

        py4hw.debug.checkIntegrity(sys)

    def test_rotate(self):
        # reset, then enable pulses: q rota un bit a la izquierda en cada pulso
        sys, reset, enable, q, q_init = self.circuit
        sim = sys.getSimulator()

        reset.put(1)                                  # reset: vuelven a su valor inicial
        enable.put(0)
        sim.clk(1)
        reset.put(0)

        exp, exp_init = 0b00000001, 0b00000010        # init=0 e init=1
        assert(q.get() == exp)
        assert(q_init.get() == exp_init)
        for e_v in [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]:
            enable.put(e_v)
            sim.clk(1)
            if e_v:
                exp = ((exp << 1) | (exp >> 7)) & 0xFF
                exp_init = ((exp_init << 1) | (exp_init >> 7)) & 0xFF
            assert(q.get() == exp)
            assert(q_init.get() == exp_init)

    def test_one_hot(self):
        # ASSUMPTION: a ring counter keeps exactly one bit set while enabled.
        # Adjust if your RingCounter implementation behaves differently.
        sys, reset, enable, q, q_init = self.circuit

        reset.put(0)
        enable.put(1)

        sim = sys.getSimulator()
        sim.clk(1)  # let the initial value settle

        for _ in range(16):  # two full rotations
            value = q_init.get()
            assert bin(value).count('1') == 1, f'q is not one-hot: {value:#010b}'
            sim.clk(1)


if __name__ == '__main__':
    pytest.main(args=['-q', 'Test_RingCounter.py'])
