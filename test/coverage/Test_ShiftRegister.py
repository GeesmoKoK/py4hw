# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 10:07:59 2025

@author: dcr
"""

import py4hw
import pytest
from py4hw.cover import ToggleCoverage


class Test_ShiftRegister:

    @classmethod
    def setup_class(cls):
        hw = py4hw.HWSystem()

        lin = hw.wire('lin', 8)
        lout = hw.wire('lout', 8)

        rin = hw.wire('rin', 8)
        rout = hw.wire('rout', 8)

        sl = hw.wire('sl')
        sr = hw.wire('sr')

        py4hw.ShiftRegisterBidirectional(hw, 'shift', lin, rin, lout, rout, sl, sr, 3)
        cls.cov = ToggleCoverage(hw)
        cls.circuit = (hw, lin, rin, lout, rout, sl, sr)

    def test_shift_right(self):
        hw, lin, rin, lout, rout, sl, sr = self.circuit
        sim = hw.getSimulator()

        sl.put(0)                                     # vaciar: tras 3 desplazamientos
        sr.put(1)                                     # sale todo lo que hubiera antes
        lin.put(0)
        for _ in range(3):
            sim.clk(1)

        q = [0, 0, 0]                                 # modelo: contenido de los 3 registros
        for v in [1, 2, 3, 4, 5]:                     # entra v por la izquierda (lin)
            lin.put(v)
            sim.clk(1)
            q = [v] + q[:-1]
            assert(lout.get() == q[0])
            assert(rout.get() == q[2])

    def test_shift_left(self):
        hw, lin, rin, lout, rout, sl, sr = self.circuit
        sim = hw.getSimulator()

        sl.put(1)                                     # vaciar
        sr.put(0)
        rin.put(0)
        for _ in range(3):
            sim.clk(1)

        q = [0, 0, 0]
        for v in [1, 2, 3, 4, 5]:                     # entra v por la derecha (rin)
            rin.put(v)
            sim.clk(1)
            q = q[1:] + [v]
            assert(lout.get() == q[0])
            assert(rout.get() == q[2])

if __name__ == '__main__':
    pytest.main(args=['-s', 'Test_ShiftRegister.py'])
