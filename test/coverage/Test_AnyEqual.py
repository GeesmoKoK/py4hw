# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 18:28:12 2022

@author: dcr
"""

import py4hw
import pytest
from py4hw.cover import ToggleCoverage


class TestAnyEqual:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        ins = sys.wires('wi', 3, 8)
        r = sys.wire('r', 1)
        py4hw.AnyEqual(sys, 'any', ins, r)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, ins, r)
    
    def test_oneEqual(self):
        sys, ins, r = self.circuit
        for w, v in zip(ins, [3, 7, 3]):
            w.put(v)
        
        sys.getSimulator().clk(1)
        assert (r.get() == 1)

    def test_noneEqual(self):
        sys, ins, r = self.circuit
        for w, v in zip(ins, [3, 7, 9]):
            w.put(v)
        
        sys.getSimulator().clk(1)
        assert (r.get() == 0)
        
    def test_verilog_gen(self):
        sys = py4hw.HWSystem()
        
        a = sys.wire("a", 32)
        b = sys.wire("b", 32)
        r = sys.wire("r")
        
        dut = py4hw.AnyEqual(sys, 'any', [a, b], r)

        rtl = py4hw.VerilogGenerator(dut)
        print(rtl.getVerilogForHierarchy(dut))
        
        
if __name__ == '__main__':
    pytest.main(args=['-s', 'Test_AnyEqual.py'])