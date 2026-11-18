import py4hw
import py4hw.debug
import pytest
from py4hw.cover import ToggleCoverage


class Test_Mul:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        a = sys.wire("a", 32)
        b = sys.wire("b", 32)
        r = sys.wire("r", 32)
        rs = sys.wire("rs", 32)
        py4hw.Mul(sys, 'mul', a, b, r)
        py4hw.SignedMul(sys, 'smul', a, b, rs)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a, b, r, rs)

    def test_integrity(self):

        sys = py4hw.HWSystem()

        a = sys.wire("a", 4)
        b = sys.wire("b", 4)
        r1 = sys.wire("r1", 4)
        r2 = sys.wire("r2", 4)

        py4hw.Constant(sys, "a", 7, a)
        py4hw.Constant(sys, "b", 3, b)

        py4hw.Mul(sys, 'mul', a, b, r1)
        py4hw.SignedMul(sys, 'signed_mul', a, b, r2)

        py4hw.debug.checkIntegrity(sys)


    def test_mul(self):
        sys, a, b, r, rs = self.circuit
        a.put(7)
        b.put(3)

        sys.getSimulator().clk(1)

        assert(r.get() == (7*3))


    def test_neg(self):
        sys, a, b, r, rs = self.circuit
        w = 32
        va = 21
        vb = -3
        vr = va * vb

        a.put(va)
        b.put(vb)

        sys.getSimulator().clk(1)

        assert(rs.get() == (vr & ((1<<w)-1)))


if __name__ == '__main__':
    pytest.main(args=['-s', 'Test_Mul.py'])
