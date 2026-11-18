# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 11:00:14 2023

@author: dcr
"""

import py4hw
import pytest
from py4hw.helper import *
import random
from py4hw.cover import ToggleCoverage


class Test_FXPMult:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        widths = FixedPoint(1,16,16, 0).getWidths()
        aw = sys.wire('a', 33)
        bw = sys.wire('b', 33)
        rw = sys.wire('r', 33)
        py4hw.FixedPointMult(sys, 'fpa', a=aw, af=widths, b=bw, bf=widths,
                             r=rw, rf=(1,16,16))
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, aw, bw, rw)

    def test_1(self):
        sys, aw, bw, rw = self.circuit

        av = FixedPoint(1,16,16, 1.2)
        bv = FixedPoint(1,16,16, 0.25)
        rv = FixedPoint(1,16,16, 1.2 * 0.25)

        aw.put(av.v)
        bw.put(bv.v)

        sys.getSimulator().clk(1)

        assert (rw.get() == rv.v)


if __name__ == '__main__':
    #pytest.main(args=['-q', 'Test_FXPMult.py'])
    pytest.main(args=['-s', 'Test_FXPMult.py'])
