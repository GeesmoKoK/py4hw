# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 10:22:14 2022

@author: dcr
"""
import py4hw
import pytest
from py4hw.cover import ToggleCoverage


class Test_FPComparator_SP:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()

        a = sys.wire('a', 32)
        b = sys.wire('b', 32)

        gt = sys.wire('gt')
        eq = sys.wire('eq')
        lt = sys.wire('lt')
        gt_abs = sys.wire('gt_abs')
        eq_abs = sys.wire('eq_abs')
        lt_abs = sys.wire('lt_abs')

        py4hw.FPComparator_SP(sys, 'cmp', a, b, gt, eq, lt)
        py4hw.FPComparator_SP(sys, 'cmp_abs', a, b, gt_abs, eq_abs, lt_abs, absolute=True)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, a, b, gt, eq, lt, gt_abs, eq_abs, lt_abs)

    def test_1(self):
        sys, a, b, gt, eq, lt = self.circuit[:6]
        fp = py4hw.FloatingPointHelper()

        av = 305.531528442573
        bv = 443.5870680854455

        a.put(fp.sp_to_ieee754(av))
        b.put(fp.sp_to_ieee754(bv))

        sys.getSimulator().clk(1)

        assert(bool(gt.get()) == (av > bv))
        assert(bool(eq.get()) == (av == bv))
        assert(bool(lt.get()) == (av < bv))

    def test_3(self):
        sys, a, b, gt, eq, lt = self.circuit[:6]
        fp = py4hw.FloatingPointHelper()

        av = -4.2
        bv = 3.5
        a.put(fp.sp_to_ieee754(av))
        b.put(fp.sp_to_ieee754(bv))

        sys.getSimulator().clk(1)

        assert (gt.get() == 0)
        assert (eq.get() == 0)
        assert (lt.get() == 1)

    def test_abs(self):
        sys, a, b = self.circuit[:3]
        gt, eq, lt = self.circuit[6:]
        fp = py4hw.FloatingPointHelper()

        av = -971.0587159810018
        bv = -353.1498041093273

        a.put(fp.sp_to_ieee754(av))
        b.put(fp.sp_to_ieee754(bv))

        sys.getSimulator().clk(1)

        assert(bool(gt.get()) == (abs(av) > abs(bv)))
        assert(bool(eq.get()) == (abs(av) == abs(bv)))
        assert(bool(lt.get()) == (abs(av) < abs(bv)))

    def test_random(self):
        import random
        sys, a, b, gt, eq, lt = self.circuit[:6]
        fp = py4hw.FloatingPointHelper()

        for i in range(1000):
            av = (random.random()-0.5) * 2000
            bv = (random.random()-0.5) * 2000

            a.put(fp.sp_to_ieee754(av))
            b.put(fp.sp_to_ieee754(bv))

            sys.getSimulator().clk(1)

            assert(bool(gt.get()) == (av > bv))
            assert(bool(eq.get()) == (av == bv))
            assert(bool(lt.get()) == (av < bv))

    def test_random_abs(self):
        import random
        sys, a, b = self.circuit[:3]
        gt, eq, lt = self.circuit[6:]
        fp = py4hw.FloatingPointHelper()

        for i in range(100):
            av = (random.random()-0.5) * 2000
            bv = (random.random()-0.5) * 2000

            a.put(fp.sp_to_ieee754(av))
            b.put(fp.sp_to_ieee754(bv))

            sys.getSimulator().clk(1)

            assert(bool(gt.get()) == (abs(av) > abs(bv)))
            assert(bool(eq.get()) == (abs(av) == abs(bv)))
            assert(bool(lt.get()) == (abs(av) < abs(bv)))

if __name__ == '__main__':
    pytest.main(args=['-q', 'Test_FPComparator_SP.py'])
