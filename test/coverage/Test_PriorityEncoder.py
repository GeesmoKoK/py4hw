# -*- coding: utf-8 -*-
import py4hw
import py4hw.debug
import pytest
from py4hw.cover import ToggleCoverage


class Test_Add:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        a = sys.wire("a", 32)
        b = sys.wire("b", 32)
        ab = sys.wires('ab', 32, 1)
        bb = sys.wires('bb', 32, 1)
        py4hw.BitsLSBF(sys, "ab", a, ab)
        py4hw.PriorityEncoder(sys, 'bb', ab, bb)
        py4hw.ConcatenateLSBF(sys, 'b', bb, b)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a, b)
    
    def test_1(self):
        sys, a, b = self.circuit
        a.put(127)
        
        sim = sys.getSimulator()
        sim.clk(1)

        #print('B=', b.get())
        assert(b.get() == 64)
        # print()
        # print('CLK')
        

if __name__ == '__main__':
    pytest.main(args=['-q', 'Test_PriorityEncoder.py'])