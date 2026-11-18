# -*- coding: utf-8 -*-
import py4hw
import py4hw.debug
import pytest
from py4hw.cover import ToggleCoverage


class Test_Comparator:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        a = sys.wire("a", 32)
        b = sys.wire("b", 32)
        gt = sys.wire("gt")
        eq = sys.wire("eq")
        lt = sys.wire("lt")
        gtu = sys.wire("gtu")
        equ = sys.wire("equ")
        ltu = sys.wire("ltu")
        gts = sys.wire("gts")
        lts = sys.wire("lts")
        py4hw.Comparator(sys, "cmp", a, b, gt, eq, lt)
        py4hw.ComparatorSignedUnsigned(sys, "cmpsu", a, b, gtu, equ, ltu, gts, lts)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a, b, gt, eq, lt, gtu, equ, ltu, gts, lts)


    def test_comparator(self):
        sys, a, b, gt, eq, lt = self.circuit[:6]
        data = [[1, 0, 1, 0, 0],
                [1, 1, 0, 1, 0],
                [0, 1, 0, 0, 1],
                [0x5b72874f, 0xfc332ded, 0, 0, 1]]

        for va, vb, vgt, veq, vlt in data:
            a.put(va)
            b.put(vb)

            sys.getSimulator().clk(1);

            assert (gt.get() == vgt)
            assert (eq.get() == veq)
            assert (lt.get() == vlt)

    def test_comparator_signed_unsigned(self):
        sys, a, b = self.circuit[:3]
        gtu, equ, ltu, gts, lts = self.circuit[6:]
        data = [[1, 0, 1, 0, 0, 1, 0],
                [1, 1, 0, 1, 0, 0, 0],
                [0, 1, 0, 0, 1, 0, 1],
                [0x5b72874f, 0xfc332ded, 0, 0, 1, 1, 0],
                [0xfc332ded, 0x5b72874f, 1, 0, 0, 0, 1]]

        for va, vb, vgtu, veq, vltu, vgt, vlt in data:
            a.put(va)
            b.put(vb)

            sys.getSimulator().clk(1);

            assert(gtu.get() == vgtu)
            assert(equ.get() == veq)
            assert(ltu.get() == vltu)
            assert(gts.get() == vgt)
            assert(lts.get() == vlt)

    def test_Integrity(self):
        sys = py4hw.HWSystem()

        a = sys.wire("a", 32)
        b = sys.wire("b", 32)
        gt = sys.wire("gt")
        eq = sys.wire("eq")
        lt = sys.wire("lt")

        py4hw.Comparator(sys, "cmp", a, b, gt, eq, lt)

        py4hw.Constant(sys, "a", 10, a)
        py4hw.Constant(sys, "b", 20, b)

        py4hw.Scope(sys, "gt", gt)
        py4hw.Scope(sys, "eq", eq)
        py4hw.Scope(sys, "lt", lt)

        py4hw.debug.checkIntegrity(sys)

    def test_verilog_gen(self):
        sys = py4hw.HWSystem()

        a = sys.wire("a", 32)
        b = sys.wire("b", 32)
        gt = sys.wire("gt")
        eq = sys.wire("eq")
        lt = sys.wire("lt")

        dut = py4hw.Comparator(sys, "cmp", a, b, gt, eq, lt)

        rtl = py4hw.VerilogGenerator(dut)
        print(rtl.getVerilogForHierarchy(dut))

if __name__ == '__main__':
    pytest.main(args=['-s', 'Test_Comparator.py'])
