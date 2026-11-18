# -*- coding: utf-8 -*-
"""
Unit testbench for Axi2Reg module
Tests AXI4-Stream to register conversion functionality

@author: dcr
"""

import pytest
import py4hw
from py4hw.logic.bus.axi import AXI4StreamInterface
from py4hw.emulation.vitiswrapping import Axi2Reg
from py4hw.cover import ToggleCoverage


def restart(circuit):
    """El circuito es compartido: lo dejamos en el estado inicial antes de cada test."""
    sys, ap_start, ap_reset, ap_done, stream, q, loaded, active, dut = circuit
    ap_start.put(0)
    stream.tvalid.put(0)
    stream.tdata.put(0)
    ap_reset.put(1)
    sys.getSimulator().clk(2)
    ap_reset.put(0)
    sys.getSimulator().clk(1)


class Test_Axi2Reg:

    @classmethod
    def setup_class(cls):
        sys = py4hw.HWSystem()

        ap_start = sys.wire("ap_start", 1)
        ap_reset = sys.wire("ap_reset", 1)
        ap_done = sys.wire("ap_done", 1)
        q = sys.wire("q", 64)
        loaded = sys.wire("loaded", 1)
        active = sys.wire("active", 1)

        stream = AXI4StreamInterface(sys, "stream", dw=64)

        dut = Axi2Reg(sys, "axi2reg",  ap_start, ap_reset, ap_done, stream, q, loaded, active)
        cls.cov = ToggleCoverage(sys)
        cls.circuit = (sys, ap_start, ap_reset, ap_done, stream, q, loaded, active, dut)

    def test_basic_capture(self):
        """Test basic capture of first 64 bits on handshake  """
        restart(self.circuit)
        sys, ap_start, ap_reset, ap_done, stream, q, loaded, active, dut = self.circuit

        ap_reset.put(1)
        sys.getSimulator().clk(1)

        ap_reset.put(0)
        sys.getSimulator().clk(1)

        assert loaded.get() == 0, 'loaded should be zero after reset'


        # Test 1: Capture on valid data
        test_data = 0x123456789ABCDEF0
        stream.tvalid.put(1)
        stream.tdata.put(test_data)

        assert active.get() == 0, 'active should be 0 if no ap_start issued'

        # Give time for signals to propagate
        sys.getSimulator().clk(2)

        # Should not capture since no ap_start was issued
        assert q.get() == 0,  'reg should be zero'
        assert loaded.get() == 0, 'loaded should be zero if no ap_start issued'

        ap_start.put(1)
        sys.getSimulator().clk(2)

        # Should capture after ap_start
        assert q.get() == test_data, 'reg should be test_data'
        assert loaded.get() == 1, 'loaded should be one after ap_start and tvalid'

    def test_reset_behavior(self):
        """Test reset clears the register and loaded signal"""
        restart(self.circuit)
        sys, ap_start, ap_reset, ap_done, stream, q, loaded, active, dut = self.circuit

        ap_reset.put(1)
        sys.getSimulator().clk(1)

        ap_reset.put(0)
        sys.getSimulator().clk(1)

        assert loaded.get() == 0, 'loaded should be zero after ap_reset'

        # Test 1: Capture on valid data
        test_data = 0x123456789ABCDEF0
        stream.tvalid.put(1)
        stream.tdata.put(test_data)
        ap_start.put(1)

        # Give time for signals to propagate
        sys.getSimulator().clk(2)
        #ap_start.put(0)

        assert active.get() == 1, 'circuit should be active after ap_start'
        assert dut._wires['handshake'].get() == 1, 'hanshake should be one after ap_start and tvalid'

        stream.tvalid.put(0)
        sys.getSimulator().clk(1)

        # Should capture on first cycle with valid data
        assert q.get() == test_data, 'unexpected test_data'

        assert loaded.get() == 1, 'loaded should be one after ap_start and tvalid'

        ap_reset.put(1)
        sys.getSimulator().clk(1)

        ap_reset.put(0)
        sys.getSimulator().clk(2)

        assert loaded.get() == 0, 'loaded should be zero'

    def test_ap_start_reset(self):
        """Test ap_start clears loaded signal"""
        restart(self.circuit)
        sys, ap_start, ap_reset, ap_done, stream, q, loaded, active, dut = self.circuit

        # Capture data
        test_data = 0xCCCCCCCCCCCCCCCC
        stream.tvalid.put(1)
        stream.tdata.put(test_data)
        sys.getSimulator().clk(1)

        assert q.get() == 0
        assert loaded.get() == 0

        # Apply ap_start (should not clear anything)
        ap_start.put(1)
        sys.getSimulator().clk(1)
        ap_start.put(0)
        sys.getSimulator().clk(1)

        assert q.get() == test_data  # q should retain value
        assert loaded.get() == 1     # loaded should be cleared

        # Remove ap_start
        ap_start.put(0)

        # Try to capture again
        test_data2 = 0xDDDDDDDDDDDDDDDD
        stream.tdata.put(test_data2)
        stream.tvalid.put(1)

        sys.getSimulator().clk(1)
        assert q.get() == test_data2
        assert loaded.get() == 1

    def test_ap_reset_behavior(self):
        """Test ap_reset clears loaded signal"""
        restart(self.circuit)
        sys, ap_start, ap_reset, ap_done, stream, q, loaded, active, dut = self.circuit

        # Capture data
        test_data = 0xEEEEEEEEEEEEEEEE
        stream.tvalid.put(1)
        stream.tdata.put(test_data)
        ap_start.put(1)
        sys.getSimulator().clk(2)
        assert q.get() == test_data
        assert loaded.get() == 1

        ap_start.put(0)
        # Apply ap_reset (should clear loaded but not q)
        ap_reset.put(1)
        sys.getSimulator().clk(2)

        # assert q.get() == test_data  # q should retain value
        assert loaded.get() == 0     # loaded should be cleared

        # Remove ap_reset
        ap_reset.put(0)

        # Try to capture again
        test_data2 = 0xFFFFFFFFFFFFFFFF
        stream.tdata.put(test_data2)
        stream.tvalid.put(1)

        sys.getSimulator().clk(2)

        assert q.get() == 0, 'we expect no loading after reset if not ap_start'
        assert loaded.get() == 0

    def test_multiple_cycles_no_data(self):
        """Test behavior when no valid data for multiple cycles"""
        restart(self.circuit)
        sys, ap_start, ap_reset, ap_done, stream, q, loaded, active, dut = self.circuit

        # Initial state
        q_initial = q.get()

        # Run for 10 cycles with no valid data
        for i in range(10):
            stream.tvalid.put(0)
            sys.getSimulator().clk(1)
            assert loaded.get() == 0
            assert q.get() == q_initial

    def test_edge_cases(self):
        """Test edge cases like maximum and minimum values"""
        restart(self.circuit)
        sys, ap_start, ap_reset, ap_done, stream, q, loaded, active, dut = self.circuit

        # Test all zeros
        stream.tvalid.put(1)
        stream.tdata.put(0)
        ap_start.put(1)
        sys.getSimulator().clk(2)
        ap_start.put(0)
        assert q.get() == 0
        assert loaded.get() == 1

        # Test all ones
        stream.tdata.put((1<<64)-1)
        sys.getSimulator().clk(1)
        assert q.get() == (1<<64)-1
        assert loaded.get() == 1

        # Test alternating pattern
        pattern = 0x5555555555555555
        stream.tdata.put(pattern)
        sys.getSimulator().clk(1)
        assert q.get() == pattern
        assert loaded.get() == 1

        # Test multiple captures in a row
        for i in range(5):
            test_val = i * 0x1111111111111111
            stream.tdata.put(test_val)
            sys.getSimulator().clk(1)
            assert q.get() == test_val
            assert loaded.get() == 1

if __name__ == '__main__':
    pytest.main(args=['-s', __file__])
