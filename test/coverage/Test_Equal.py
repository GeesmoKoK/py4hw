import py4hw
import py4hw.debug
import pytest
from py4hw.cover import ToggleCoverage


class Test_Equal:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()
        a = sys.wire("a", 3)
        b = sys.wire("b", 3)
        bit = sys.wire("bit", 1)
        r_eq0 = sys.wire("r_eq0", 1)
        r_ne0 = sys.wire("r_ne0", 1)
        r_eq5 = sys.wire("r_eq5", 1)
        r_bit = sys.wire("r_bit", 1)
        r_ab = sys.wire("r_ab", 1)
        py4hw.EqualConstant(sys, 'eq0', a, 0, r_eq0)
        py4hw.NotEqualConstant(sys, 'ne0', a, 0, r_ne0)
        py4hw.EqualConstant(sys, 'eq5', a, 5, r_eq5)
        py4hw.EqualConstant(sys, 'eqbit', bit, 1, r_bit)
        py4hw.Equal(sys, 'equal_ab', a, b, r_ab)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a, b, bit, r_eq0, r_ne0, r_eq5, r_bit, r_ab)

    def test_integrity(self):

        sys = py4hw.HWSystem()

        a = sys.wire("a", 2)
        r = sys.wire("r", 1)

        py4hw.Constant(sys, "a", 0, a)

        py4hw.EqualConstant(sys, 'equal', a, 0, r)

        py4hw.debug.checkIntegrity(sys)

    def test_1(self):
        sys, a, b, bit, r_eq0, r_ne0, r_eq5, r_bit, r_ab = self.circuit
        a.put(3)

        sys.getSimulator().clk(1)

        assert (r_ne0.get() == 1)


    def test_notEqual(self):
        sys, a, b, bit, r_eq0, r_ne0, r_eq5, r_bit, r_ab = self.circuit
        a.put(3)

        sys.getSimulator().clk(1)

        assert (r_eq0.get() == 0)

    def test_equal5(self):
        sys, a, b, bit, r_eq0, r_ne0, r_eq5, r_bit, r_ab = self.circuit

        for v in [0,1,2,3,4,5,6,7]:
            a.put(v)
            sys.getSimulator().clk(1)
            exp = 1 if (v==5) else 0
            assert (r_eq5.get() == exp)

    def test_oneBitWire(self):
        sys, a, b, bit, r_eq0, r_ne0, r_eq5, r_bit, r_ab = self.circuit

        for v in [0,1,0,1]:
            bit.put(v)
            sys.getSimulator().clk(1)
            exp = 1 if (v==1) else 0
            assert (r_bit.get() == exp)

    def test_EqualWire(self):
        sys, a, b, bit, r_eq0, r_ne0, r_eq5, r_bit, r_ab = self.circuit

        a.put(3)
        b.put(3)
        sys.getSimulator().clk(1)
        assert (r_ab.get() == 1)

        b.put(5)
        sys.getSimulator().clk(1)
        assert (r_ab.get() == 0)

if __name__ == '__main__':
    pytest.main(args=['-q', 'Test_Equal.py'])
