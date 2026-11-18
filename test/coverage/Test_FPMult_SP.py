# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 19:31:11 2022

@author: dcr
"""

import py4hw
import pytest
from py4hw.helper import BitManipulation
import random
import math
from py4hw.cover import ToggleCoverage


class Test_FPMult_SP:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        a = sys.wire('a', 32)
        b = sys.wire('b', 32)
        r = sys.wire('r', 32)
        py4hw.FPMult_SP(sys, 'fpm', a, b, r)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a, b, r)

    def test_1(self):
        sys, a, b, r = self.circuit
        fp = py4hw.FloatingPointHelper()

        av = 3.2
        bv = 5.00002
        a.put(fp.sp_to_ieee754(av))
        b.put(fp.sp_to_ieee754(bv))

        sys.getSimulator().clk(1)

        err = fp.ieee754_to_sp(r.get()) - (av*bv)
        assert (abs(err) < 1E-5)

    def test_random(self):
        sys, a, b, r = self.circuit
        fp = py4hw.FloatingPointHelper()

        large = math.pow(2, 29)

        for i in range(100):
            av = random.uniform(-large, large)
            bv = random.uniform(-large, large)

            a.put(fp.sp_to_ieee754(av))
            b.put(fp.sp_to_ieee754(bv))

            sys.getSimulator().clk(1)

            rv = fp.ieee754_to_sp(r.get())
            rerr = abs(rv - (av*bv)) / (av*bv)
            assert (rerr < 1E-6)


if __name__ == '__main__':
    #pytest.main(args=['-q', 'Test_FPAdder_SP.py'])
    pytest.main(args=['-s', 'Test_FPMult_SP.py'])
