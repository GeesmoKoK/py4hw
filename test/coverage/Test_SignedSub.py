# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 13:46:38 2022

@author: dcr
"""
import py4hw
import pytest
from py4hw.cover import ToggleCoverage

# Note: The test battery relies on Python's behavior where a negative number
# masked with (1<<w)-1 correctly yields the two's complement representation
# that the py4hw simulator will output.


class Test_SignedSub:
    """
    Unit tests for the py4hw.SignedSub component.

    Tests include:
    1. Standard signed subtraction (positive and negative results).
    2. Verilog generation integrity.
    """

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        a = sys.wire('a', 32)
        b = sys.wire('b', 32)
        r = sys.wire('r', 32)
        py4hw.SignedSub(sys, 'signed_sub_dut', a, b, r)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a, b, r)

    def test_signed_subtraction(self):
        """
        Fields: [Input A (signed), Input B (signed), Expected Result (signed)]
        All tests use the fixed 32-bit circuit.
        """
        sys, a, b, r = self.circuit

        battery = [
            [10, 5, 5],          # 10 - 5 = 5
            [5, 10, -5],         # 5 - 10 = -5
            [-1, 1, -2],         # -1 - 1 = -2
            [-10, -5, -5],       # -10 - (-5) = -5
            [127, 0, 127],
            [-128, 0, -128],
            [127, -1, 128],
            [-128, 1, -129],

            [1000, 500, 500],
            [500, 1000, -500],
            [-1, 1, -2],
            [-1000, -2000, 1000], # -1000 - (-2000) = 1000
        ]

        for va, vb, expected_signed_result in battery:
            vr = expected_signed_result & ((1 << 32) - 1)

            a.put(va)
            b.put(vb)
            sys.getSimulator().clk(1)
            result = r.get()

            assert(result == vr), f"Failed: {va} - {vb}. Expected HW value: {vr}, Got: {result}"

    def test_verilog_gen_signed_sub(self):
        """
        Tests the Verilog code generation for the SignedSub component.
        """
        sys = py4hw.HWSystem()

        a = sys.wire("a", 16)
        b = sys.wire("b", 16)
        r = sys.wire("r", 16)

        # Instantiate the SignedSub DUT
        dut = py4hw.SignedSub(sys, "signed_sub", a, b, r)

        # Generate Verilog
        rtl = py4hw.VerilogGenerator(dut)
        print('RTL:', rtl.getVerilogForHierarchy(dut))


if __name__ == '__main__':
    pytest.main(args=['-s', 'Test_SignedSub.py'])
