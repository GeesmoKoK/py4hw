# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 11:52:40 2020

@author: dcr
"""

import py4hw
import py4hw.debug
import pytest
from py4hw.cover import ToggleCoverage


class Test_Minterm:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        r = sys.wire("r", 1)
        a0 = sys.wire("a0", 1)
        a1 = sys.wire("a1", 1)
        a2 = sys.wire("a2", 1)
        py4hw.Minterm(sys, 'minterm', [a0, a1, a2], 5, r)

        a = sys.wire("a", 4)
        v = sys.wire('v')
        ev = sys.wire('ev')
        eq = sys.wire('eq')
        py4hw.SumOfMinterms(sys, 'som', a, [1,2,3,5,7,11,13], v)
        py4hw.Equal(sys, 'eq', ev, v, eq)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, r, a0, a1, a2, a, ev, eq)

    def test_integrity(self):
        sys = py4hw.HWSystem()

        a = sys.wire("a", 2)

        bits = sys.wires('b', 2, 1)
        minterm = sys.wire('minterm',1)

        py4hw.BitsLSBF(sys, 'bits', a, bits)
        py4hw.Minterm(sys, 'minterm', bits, 0, minterm)
        py4hw.Constant(sys, "a", 0, a)

        for i in range(len(bits)):
            py4hw.Scope(sys, 'b{}'.format(i), bits[i])

        py4hw.Scope(sys, 'minterm_5', minterm)


        py4hw.debug.checkIntegrity(sys)

    def test_1(self):
        sys, r, a0, a1, a2, a, ev, eq = self.circuit

        exp_a0 = [0,1,0,1,0,1,0,1]
        exp_a1 = [0,0,1,1,0,0,1,1]
        exp_a2 = [0,0,0,0,1,1,1,1]

        for i in range(8):
            a0.put(exp_a0[i])
            a1.put(exp_a1[i])
            a2.put(exp_a2[i])
            sys.getSimulator().clk(1)
            rv = r.get()

            assert (rv == (1 if i == 5 else 0))

    def test_sum_of_minterms(self):
        sys, r, a0, a1, a2, a, ev, eq = self.circuit

        sa = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        sev =  [0,1,1,1,0,1,0,1,0,0, 0, 1, 0, 1, 0, 0]

        for i in range(32):
            a.put(sa[i % 16])
            ev.put(sev[i % 16])
            sys.getSimulator().clk(1)
            assert(eq.get() == 1)

if __name__ == '__main__':
    pytest.main(args=['-q', 'Test_Minterm.py'])
