# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 10:50:59 2022

@author: dcr
"""

import py4hw
import py4hw.debug
from py4hw.helper import BitManipulation
import pytest
from py4hw.cover import ToggleCoverage


class Test_CountLeadingZeros:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        w = 32
        a = sys.wire("a", w)
        r = sys.wire("r", w)
        z = sys.wire("z")
        py4hw.CountLeadingZeros(sys, "clz", a, r, z)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a, r, z)


    def test_8bit(self):
        sys, a, r, z = self.circuit
        w = 32

        v = 64

        a.put(v)
        sys.getSimulator().clk(1);
        assert(r.get() == BitManipulation.countLeadingZeros(v, w))
        assert(z.get() == int(v == 0))

    def test_32bit(self):
        sys, a, r, z = self.circuit
        w = 32

        v = 0x3456

        a.put(v)
        sys.getSimulator().clk(1);
        assert(r.get() == BitManipulation.countLeadingZeros(v, w))
        assert(z.get() == int(v == 0))


    def test_zero(self):
        sys, a, r, z = self.circuit

        a.put(0)
        sys.getSimulator().clk(1);
        assert(r.get() == 32)
        assert(z.get() == 1)


if __name__ == '__main__':
    #pytest.main(args=['-q', 'Test_CountLeadingZeros.py'])
    pytest.main(args=['-s', 'Test_CountLeadingZeros.py'])
