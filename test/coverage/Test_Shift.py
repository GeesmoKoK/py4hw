# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 09:53:22 2022

@author: dcr
"""
import py4hw
import pytest
from py4hw.helper import *
import random
import math
from py4hw.cover import ToggleCoverage


class Test_Shift:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()

        # 32 bits: shift by a variable amount
        a32 = sys.wire('a32', 32)
        b5 = sys.wire('b5', 5)
        l32 = sys.wire('l32', 32)
        r32 = sys.wire('r32', 32)
        py4hw.ShiftLeft(sys, 'left', a32, b5, l32 )
        py4hw.ShiftRight(sys, 'right', a32, b5, r32 )

        # 56 bits: variable shift right and constant shifts
        a56 = sys.wire('a56', 56)
        b8 = sys.wire('b8', 8)
        r64 = sys.wire('r64', 64)
        rk64 = sys.wire('rk64', 64)
        lk64 = sys.wire('lk64', 64)
        py4hw.ShiftRight(sys, 'right56', a56, b8, r64 )
        py4hw.ShiftRightConstant(sys, 'rightk', a56, 5, rk64 )
        py4hw.ShiftLeftConstant(sys, 'leftk', a56, 5, lk64 )

        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a32, b5, l32, r32, a56, b8, r64, rk64, lk64)

    def test_integrity(self):
        sys = py4hw.HWSystem()

        reset = sys.wire('reset')
        a = sys.wire('a', 32)
        b = sys.wire('b', 5)
        l = sys.wire('l', 32)
        r = sys.wire('r', 32)

        ca = py4hw.Constant(sys, 'a', 0, a)
        cb = py4hw.Constant(sys, 'b', 3, b)


        py4hw.ShiftLeft(sys, 'left', a, b, l )
        py4hw.ShiftRight(sys, 'right', a, b, r )

        py4hw.debug.checkIntegrity(sys)

    def test_shiftr_1(self):
        sys, a32, b5, l32, r32, a56, b8, r64, rk64, lk64 = self.circuit

        av = 0x9020f800000000
        bv = 0x5
        a56.put(av)
        b8.put(bv)

        exp_r = (av >> bv) & ((1<<64)-1)

        sys.getSimulator().clk(1)

        assert(r64.get() == exp_r)

    def test_random(self):
        sys, a32, b5, l32, r32, a56, b8, r64, rk64, lk64 = self.circuit

        for i in range(100):
            av = int(random.uniform(0x100, 0x00FFFF00))
            bv = int(random.uniform(0, 16))
            a32.put(av)
            b5.put(bv)

            sys.getSimulator().clk(1)

            exp_l = (av << bv) & 0xFFFFFFFF
            exp_r = (av >> bv) & 0xFFFFFFFF

            assert(l32.get() == exp_l)
            assert(r32.get() == exp_r)


    def test_shiftrk_1(self):
        sys, a32, b5, l32, r32, a56, b8, r64, rk64, lk64 = self.circuit

        av = 0x9020f800000000
        bv = 0x5
        a56.put(av)

        exp_r = (av >> bv) & ((1<<64)-1)

        sys.getSimulator().clk(1)

        assert(rk64.get() == exp_r)


    def test_shiftlk_1(self):
        sys, a32, b5, l32, r32, a56, b8, r64, rk64, lk64 = self.circuit

        av = 0x9020f8
        bv = 0x5
        a56.put(av)

        exp_r = (av << bv) & ((1<<64)-1)

        sys.getSimulator().clk(1)

        assert(lk64.get() == exp_r), f'{lk64.get():X} != {exp_r:X}'

    def test_shift_right_k_verilog_gen(self):
        sys = py4hw.HWSystem()

        a = sys.wire("a", 32)
        bv = 5
        r = sys.wire("r", 32)

        dut = py4hw.ShiftRightConstant(sys, 'right', a, bv, r )

        rtl = py4hw.VerilogGenerator(dut)
        print(rtl.getVerilogForHierarchy(dut))

    def test_shift_left_k_verilog_gen(self):
        sys = py4hw.HWSystem()

        a = sys.wire("a", 32)
        bv = 5
        r = sys.wire("r", 32)

        dut = py4hw.ShiftLeftConstant(sys, 'left', a, bv, r )

        rtl = py4hw.VerilogGenerator(dut)
        print(rtl.getVerilogForHierarchy(dut))

if __name__ == '__main__':
    pytest.main(args=['-s', 'Test_Shift.py'])
