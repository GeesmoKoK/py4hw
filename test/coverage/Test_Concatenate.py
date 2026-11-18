# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 09:40:27 2022

@author: dcr
"""

import py4hw
import py4hw.debug
import pytest
from py4hw.cover import ToggleCoverage


class Test_Concatenate:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()

        # 8 + 8 -> 16
        a8 = sys.wire("a8", 8)
        b8 = sys.wire("b8", 8)
        c8 = sys.wire("c8", 8)
        r16_msb = sys.wire("r16_msb", 16)
        r16_lsb = sys.wire("r16_lsb", 16)
        py4hw.ConcatenateMSBF(sys, "concat16_msb", [a8, b8], r16_msb)
        py4hw.ConcatenateLSBF(sys, "concat16_lsb", [a8, b8], r16_lsb)

        # 8 + 8 + 8 -> 24
        r24_msb = sys.wire("r24_msb", 24)
        r24_lsb = sys.wire("r24_lsb", 24)
        py4hw.ConcatenateMSBF(sys, "concat24_msb", [a8, b8, c8], r24_msb)
        py4hw.ConcatenateLSBF(sys, "concat24_lsb", [a8, b8, c8], r24_lsb)

        # 1 + 8 + 23 -> 32
        a1 = sys.wire("a1", 1)
        b8_ = sys.wire("b8_", 8)
        c23 = sys.wire("c23", 23)
        r32_msb = sys.wire("r32_msb", 32)
        r32_lsb = sys.wire("r32_lsb", 32)
        py4hw.ConcatenateMSBF(sys, "concat32_msb", [a1, b8_, c23], r32_msb)
        py4hw.ConcatenateLSBF(sys, "concat32_lsb", [a1, b8_, c23], r32_lsb)

        # 5 + 7 + 11 -> 32
        a5 = sys.wire("a5", 5)
        b7 = sys.wire("b7", 7)
        c11 = sys.wire("c11", 11)
        r32 = sys.wire("r32", 32)
        py4hw.ConcatenateMSBF(sys, "concat32", [a5, b7, c11], r32)

        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a8, b8, c8, r16_msb, r16_lsb, r24_msb, r24_lsb,
                a1, b8_, c23, r32_msb, r32_lsb, a5, b7, c11, r32)


    def test_concat_msbf_1(self):
        sys, a8, b8, c8, r16_msb = self.circuit[:5]

        a8.put(0x5F)
        b8.put(0x37)

        sys.getSimulator().clk(1);
        assert (r16_msb.get() == 0x5F37)

    def test_concat_lsbf_1(self):
        sys, a8, b8, c8, r16_msb, r16_lsb = self.circuit[:6]

        a8.put(0x5F)
        b8.put(0x37)

        sys.getSimulator().clk(1);
        assert (r16_lsb.get() == 0x375F)

    def test_concat_msbf_2(self):
        sys, a8, b8, c8, r16_msb, r16_lsb, r24_msb = self.circuit[:7]

        a8.put(0x5F)
        b8.put(0x37)
        c8.put(0xD1)

        sys.getSimulator().clk(1);
        assert (r24_msb.get() == 0x5F37D1)

    def test_concat_lsbf_2(self):
        sys, a8, b8, c8, r16_msb, r16_lsb, r24_msb, r24_lsb = self.circuit[:8]

        a8.put(0x5F)
        b8.put(0x37)
        c8.put(0xD1)

        sys.getSimulator().clk(1);
        assert (r24_lsb.get() == 0xD1375F)

    def test_msbf_3(self):
        sys = self.circuit[0]
        a1, b8_, c23, r32_msb = self.circuit[8:12]

        av = 0
        bv = 127
        cv = 2516585
        ev = (127 << 23) | cv

        a1.put(av)
        b8_.put(bv)
        c23.put(cv)

        sys.getSimulator().clk(1);
        assert (r32_msb.get() == ev)

    def test_lsbf_3(self):
        sys = self.circuit[0]
        a1, b8_, c23, r32_msb, r32_lsb = self.circuit[8:13]

        av = 0
        bv = 127
        cv = 2516585
        ev = (((cv << 8) | bv) << 1) | av

        a1.put(av)
        b8_.put(bv)
        c23.put(cv)

        sys.getSimulator().clk(1);
        assert (r32_lsb.get() == ev)

    def test_2(self):
        sys = self.circuit[0]
        a5, b7, c11, r32 = self.circuit[13:]

        av = 11
        bv = 23
        cv = 111
        ev = (((av << 7) | bv ) << 11) | cv

        a5.put(av)
        b7.put(bv)
        c11.put(cv)

        sys.getSimulator().clk(1);
        assert (r32.get() == ev)


    def test_3(self):
        # concatenating larger wires should raise an error
        sys = py4hw.HWSystem()
        a = sys.wire("a", 13)
        b = sys.wire("b", 23)
        c = sys.wire("c", 11)
        r = sys.wire("r", 32)

        av = 11
        bv = 23
        cv = 111

        try:
            py4hw.ConcatenateMSBF(sys, "concat", [a,b,c], r)

            a.put(av)
            b.put(bv)
            c.put(cv)

            sys.getSimulator().clk(1);
            exception = False
        except:
            exception = True

        assert(exception)


    def test_rtl_inlining(self):
        # concatenating larger wires should raise an error
        sys = py4hw.HWSystem()
        hw = py4hw.LogicHelper(sys)
        r1 = sys.wire("r1", 32)
        r2 = sys.wire("r2", 32)

        a = hw.hw_constant(8, 5)
        b = hw.hw_constant(8, 21)
        c = hw.hw_constant(3, 2)

        py4hw.ConcatenateMSBF(sys, "concat1", [a,b,c], r1)
        py4hw.ConcatenateLSBF(sys, "concat2", [a,b,c], r2)

        rtl = py4hw.VerilogGenerator(sys)
        print(rtl.getVerilogForHierarchy())

if __name__ == '__main__':
    pytest.main(args=['-s', 'Test_Concatenate.py'])
