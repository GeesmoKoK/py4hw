# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 12:32:33 2024

@author: dcastel1
"""

import py4hw
import pytest
from py4hw.helper import *
import random
import math

from py4hw.logic.arithmetic_fp import FixedPointtoFP_SP
from py4hw.cover import ToggleCoverage


class Test_FXPtoFP_SP:

    @classmethod
    def setup_class(cls):
        hw = py4hw.HWSystem()
        widths = FixedPoint(1, 8, 16, 0).getWidths()
        a = hw.wire('a', 25)
        r = hw.wire('r', 32)
        p_lost = hw.wire('p_lost')
        FixedPointtoFP_SP(hw, 'fxp2fp', a, widths, r, p_lost)
        cls.cov = ToggleCoverage(hw)
        cls.circuit = (hw, a, r, p_lost)

    def test_1(self):
        hw, a, r, p_lost = self.circuit
        ka = FixedPoint(1, 8, 16, 1.5)

        a.put(ka.v)

        hw.getSimulator().clk()

        rv = FPNum(r.get(), 'sp')

        assert(rv.to_float() == 1.5)

    def test_2(self):
        hw, a, r, p_lost = self.circuit
        data = [2.5, 3.5, 4.5,
                19.018951416015625, # we do no support rounding yet
                -2.5]

        for v in data:
            ka = FixedPoint(1, 8, 16, v)
            a.put(ka.v)

            hw.getSimulator().clk()

            rv = FPNum(r.get(), 'sp')

            assert(rv.to_float() == v)


if __name__ == '__main__':
    #pytest.main(args=['-q', 'Test_FXPSub.py'])
    pytest.main(args=['-s', 'Test_FXPtoFP.py'])
