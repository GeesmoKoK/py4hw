# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 09:56:24 2022

@author: dcr
"""

import py4hw
import pytest
from py4hw.helper import BitManipulation
import random
import math
from py4hw.cover import ToggleCoverage


class Test_FPtoInt_SP:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        a = sys.wire('a', 32)
        r = sys.wire('r', 32)
        p_lost = sys.wire('p_lost')
        py4hw.InttoFP_SP(sys, 'fi2a', a, r, p_lost)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a, r, p_lost)

    def test_1(self):
        sys, a, r, p_lost = self.circuit
        fp = py4hw.FloatingPointHelper()

        av = 2345
        a.put(av)
        exp_a = fp.sp_to_ieee754(av)

        sys.getSimulator().clk(1)

        ri = int(fp.ieee754_to_sp(r.get()))

        assert (r.get() == exp_a)
        assert (p_lost.get() == int(abs(ri- av) > 0))

    def test_negative(self):
        sys, a, r, p_lost = self.circuit
        fp = py4hw.FloatingPointHelper()

        av = -2345
        a.put(av)
        exp_a = fp.sp_to_ieee754(av)

        sys.getSimulator().clk(1)

        ri = int(fp.ieee754_to_sp(r.get()))

        assert (r.get() == exp_a)
        assert (p_lost.get() == int(abs(ri- av) > 0))

    def test_random(self):
        sys, a, r, p_lost = self.circuit
        fp = py4hw.FloatingPointHelper()

        for i in range(10):
            large = math.pow(2, 29)
            av = int(random.uniform(-large, large))

            rav = fp.ieee754_stored_internally(av)
            exp_a = fp.sp_to_ieee754(rav)

            a.put(av)
            sys.getSimulator().clk(1)

            ri = r.get()

            assert (abs(r.get() - exp_a) < 2)
            assert (p_lost.get() == int(abs(av- rav) > 0))


if __name__ == '__main__':
    #pytest.main(args=['-q', 'Test_FPAdder_SP.py'])
    pytest.main(args=['-s', 'Test_InttoFP_SP.py'])
