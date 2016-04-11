from ..components import Bearing, MechanicalBearing, MagneticBearing

import unittest
from mock import Mock, patch
from functools import partial


def MakeBearing(ready='not ready'):
    bearing = Bearing()
    bearing._ready = ready == 'ready'

    return bearing


class TestBearingBaseFunctionality(unittest.TestCase):
    def test_initial_state_is_not_ready(self):
        bearing = MakeBearing()

        self.assertFalse(bearing.ready)

    def test_start_transitions_ready_state(self):
        bearing = MakeBearing()
        bearing.start()

        self.assertTrue(bearing.ready)

    def test_stop_transitions_ready_state(self):
        bearing = MakeBearing('ready')
        bearing.stop()

        self.assertFalse(bearing.ready)

    def test_start_produces_ready_event(self):
        bearing = MakeBearing()

        mock = Mock()
        bearing.ready_event += mock
        bearing.start()

        mock.assert_called_once()

    def test_start_does_nothing_when_ready(self):
        bearing = MakeBearing('ready')

        mock = Mock()
        bearing.ready_event += mock
        bearing.start()

        mock.assert_not_called()

    def test_stop_produces_not_ready_event(self):
        bearing = MakeBearing('ready')

        mock = Mock()
        bearing.not_ready_event += mock
        bearing.stop()

        mock.assert_called_once()

    def test_stop_does_nothing_when_not_ready(self):
        bearing = MakeBearing()

        mock = Mock()
        bearing.ready_event += mock
        bearing.stop()

        mock.assert_not_called()

    def test_start_calls_doStart_if_present(self):
        bearing = MakeBearing()
        bearing.doStart = Mock()

        bearing.start()

        bearing.doStart.assert_called_once()

    def test_stop_calls_doStop_if_present(self):
        bearing = MakeBearing('ready')
        bearing.doStop = Mock()

        bearing.stop()

        bearing.doStop.assert_called_once()


class TestMechanicalBearing(unittest.TestCase):
    def test_MechanicalBearing_is_ready_by_default(self):
        bearing = MechanicalBearing()
        self.assertTrue(bearing.ready)


class TestMagneticBearing(unittest.TestCase):
    def test_MagneticBearing_is_not_ready_by_default(self):
        bearing = MagneticBearing()
        self.assertFalse(bearing.ready)

    def test_initial_canSwitchOn(self):
        bearing = MagneticBearing()
        self.assertTrue(bearing.canSwitchOn())

        bearing.switchOn()
        self.assertFalse(bearing.canSwitchOn())

    def test_canSwitchOff(self):
        bearing = MagneticBearing()
        self.assertFalse(bearing.canSwitchOff())

        bearing.switchOn()
        self.assertTrue(bearing.canSwitchOff())

    def test_canLevitate(self):
        bearing = MagneticBearing()
        self.assertFalse(bearing.canLevitate())

        bearing.switchOn()
        self.assertTrue(bearing.canLevitate())

        bearing.levitate()
        self.assertFalse(bearing.canLevitate())

    def test_ready(self):
        bearing = MagneticBearing()
        self.assertFalse(bearing.ready)

        bearing.start()
        self.assertTrue(bearing.ready)

        bearing.stop()
        self.assertFalse(bearing.ready)

    def test_canDelevitate(self):
        bearing = MagneticBearing()
        self.assertFalse(bearing.canDelevitate())

        bearing.switchOn()
        self.assertFalse(bearing.canDelevitate())

        bearing.levitate()
        self.assertTrue(bearing.canDelevitate())

        bearing.delevitate()
        self.assertFalse(bearing.canDelevitate())

    def test_doSimulateLevitation_is_called(self):
        bearing = MagneticBearing()
        bearing.switchOn()

        with patch.object(bearing, 'doSimulateLevitation', create=True) as doSimulateSimulationMock:
            bearing.levitate()

        doSimulateSimulationMock.assert_called_once()

    def test_simulateLevitationSuccess(self):
        bearing = MagneticBearing()
        bearing.switchOn()

        bearing.doSimulateLevitation = bearing.simulateLevitationSuccess

        bearing.levitate()
        self.assertTrue(bearing.ready)

    def test_simulateLevitationFailure(self):
        bearing = MagneticBearing()

        errorMock = Mock()
        bearing.doSimulateLevitation = partial(bearing.simulateLevitationFailure, 'Could not reach levitation.')
        bearing.error_event += errorMock

        bearing.start()

        errorMock.assert_called_once()
