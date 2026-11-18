# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 21:27:55 2023

@author: dcastel1
"""

import py4hw
import py4hw.debug
import pytest
from py4hw.cover import ToggleCoverage


class Test_Sign:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()

        a_reg = sys.wire('a_reg', 8)
        r_reg = sys.wire('r_reg', 8)
        a_treg = sys.wire('a_treg', 8)
        r_treg = sys.wire('r_treg', 8)

        py4hw.Reg(sys, 'reg', a_reg, r_reg)
        py4hw.TReg(sys, 'treg', a_treg, r_treg)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a_reg, r_reg, a_treg, r_treg)

    def test_reg(self):
        sys, a_reg, r_reg, a_treg, r_treg = self.circuit
        sim = sys.getSimulator()

        for v in [0x00, 0xFF, 0xAA, 0x55, 0x00]:      # Reg copia su entrada en cada ciclo
            a_reg.put(v)
            sim.clk(1)
            assert(r_reg.get() == v)


    def test_treg(self):
        sys, a_reg, r_reg, a_treg, r_treg = self.circuit
        sim = sys.getSimulator()

        exp = 0                                       # modelo: TReg conmuta cuando t = 1
        for t in [0, 1, 0, 1, 1, 0, 1]:
            a_treg.put(t)
            sim.clk(1)
            exp = exp ^ t
            assert(r_treg.get() == exp)


if __name__ == '__main__':
    pytest.main(args=['-s', 'Test_Storage.py'])
