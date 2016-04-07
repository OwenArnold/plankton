from ..components import Bearing

import unittest
from mock import Mock, patch


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
