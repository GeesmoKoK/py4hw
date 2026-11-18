# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 13:46:38 2022

@author: dcr
"""
import py4hw
import pytest
from py4hw.cover import ToggleCoverage


class Test_Sub:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        a = sys.wire('a', 32)
        b = sys.wire('b', 32)
        r = sys.wire('r', 32)
        rs = sys.wire('rs', 32)
        py4hw.Sub(sys, 'sub', a, b, r)
        py4hw.SignedSub(sys, 'ssub', a, b, rs)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a, b, r, rs)

    def get_result(self, circuit, signed, va, vb):
        sys, a, b, r, rs = circuit
        a.put(va)
        b.put(vb)
        sys.getSimulator().clk(1)
        return rs.get() if signed else r.get()

    def test_sub_unsigned(self):
        battery = [[1, 1, 0],
                   [2, 1, 1],
                   [0, 1, -1],
                   [1<<7, 127, 1]]

        for t in battery:
            va = t[0]
            vb = t[1]
            vr = t[2] & ((1<<32)-1)

            assert(self.get_result(self.circuit, False, va, vb) == vr)

    def test_sub_signed(self):
        battery = [[1, 1, 0],
                   [2, 1, 1],
                   [-128, -1, -127]]

        for t in battery:
            va = t[0]
            vb = t[1]
            vr = t[2] & ((1<<32)-1)

            assert(self.get_result(self.circuit, True, va, vb) == vr)

    def test_verilog_gen(self):
        sys = py4hw.HWSystem()

        a = sys.wire("a", 32)
        b = sys.wire("b", 32)
        r = sys.wire("r", 32)

        dut = py4hw.Sub(sys, "sub", a, b, r)

        rtl = py4hw.VerilogGenerator(dut)
        print(rtl.getVerilogForHierarchy(dut))

if __name__ == '__main__':
    pytest.main(args=['-s', 'Test_Sub.py'])
