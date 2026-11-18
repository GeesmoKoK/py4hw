import py4hw
import pytest
from py4hw.linecover import LineCoverage


class Mux(py4hw.Logic):
    def __init__(self, parent, name, sel, r):
        super().__init__(parent, name)
        self.sel = self.addIn('sel', sel)
        self.r = self.addOut('r', r)

    def propagate(self):
        if self.sel.get():
            self.r.put(1)
        else:
            self.r.put(0)


class Test_LineCoverage:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        sel = sys.wire('sel')
        r = sys.wire('r')
        Mux(sys, 'mux', sel, r)
        cls.line = LineCoverage(sys)
        cls.circuit = (sys, sel, r)

    def test_lines(self):
        sys, sel, r = self.circuit
        sim = sys.getSimulator()

        assert(self.line.covered_and_total() == (0, 3))   

        self.line.start()
        sel.put(1)                                      
        sim.clk(1)
        self.line.stop()
        assert(r.get() == 1)
        assert(self.line.covered_and_total() == (2, 3))  

        self.line.start()
        sel.put(0)                                       
        sim.clk(1)
        self.line.stop()
        assert(r.get() == 0)
        assert(self.line.covered_and_total() == (3, 3)) 


if __name__ == '__main__':
    pytest.main(args=['-q', 'Test_LineCoverage.py'])
