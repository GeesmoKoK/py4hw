# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:29:57 2023

@author: dcr
"""


import py4hw
import py4hw.debug
import pytest
from py4hw.cover import ToggleCoverage


class Test_Abs:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        pos = sys.wire("pos", 32)
        neg = sys.wire("neg", 32)
        py4hw.Constant(sys, "k_pos", 0x22, pos)
        py4hw.Constant(sys, "k_neg", -0x22, neg)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, pos, neg)

    def test_pos(self):
        sys, pos, neg = self.circuit
        w = 32
        v = 0x22

        sys.getSimulator().clk(1)

        assert(pos.get() == v & ((1<<w)-1))


    def test_neg(self):
        sys, pos, neg = self.circuit
        w = 32
        v = -0x22

        sys.getSimulator().clk(1)

        assert(neg.get() == v & ((1<<w)-1))

    def test_verilog_gen(self):
        sys = py4hw.HWSystem()

        r = sys.wire("r", 32)

        dut = py4hw.Constant(sys, "k", 0x25, r)

        rtl = py4hw.VerilogGenerator(dut)
        print('RTL:', rtl.getVerilogForHierarchy(dut))

if __name__ == '__main__':
    pytest.main(args=['-s', 'Test_Constant.py'])
