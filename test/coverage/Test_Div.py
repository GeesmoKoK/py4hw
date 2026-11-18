import py4hw
import py4hw.debug
import pytest
from py4hw.cover import ToggleCoverage


class Test_Div:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        a = sys.wire("a", 32)
        b = sys.wire("b", 32)
        r = sys.wire("r", 32)
        rs = sys.wire("rs", 32)
        py4hw.Div(sys, 'div', a, b, r)
        py4hw.SignedDiv(sys, 'sdiv', a, b, rs)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a, b, r, rs)

    def test_integrity(self):

        sys = py4hw.HWSystem()

        a = sys.wire("a", 4)
        b = sys.wire("b", 4)
        r = sys.wire("r", 4)

        py4hw.Constant(sys, "a", 7, a)
        py4hw.Constant(sys, "b", 3, b)

        py4hw.Div(sys, 'equal', a, b, r)

        py4hw.debug.checkIntegrity(sys)


    def test_div(self):
        sys, a, b, r, rs = self.circuit
        a.put(7)
        b.put(3)

        sys.getSimulator().clk(1)

        assert(r.get() == (7//3))


    def test_neg_den(self):
        sys, a, b, r, rs = self.circuit
        w = 32
        va = 21
        vb = -3
        vr = va // vb

        a.put(va)
        b.put(vb)

        sys.getSimulator().clk(1)

        assert(rs.get() == (vr & ((1<<w)-1)))


    def test_random(self):
        import random
        sys, a, b, r, rs = self.circuit

        for i in range(10000):
            va = int(random.random() * ((1<<32)-1))
            vb =  int(random.random() * ((1<<32)-1))
            a.put(va)
            b.put(vb)
            sys.getSimulator().clk(1)

            assert(r.get() == (va//vb))


if __name__ == '__main__':
    pytest.main(args=['-s', 'Test_Div.py'])
