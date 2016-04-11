from ..components import CanBeReady, CanFail, CanSwitchOn, CanSwitchOff

import unittest
from mock import patch, Mock


class TestCanBeReady(unittest.TestCase):
    def test_default_initial_state(self):
        mixin = CanBeReady()
        self.assertFalse(mixin.ready)

    def test_initial_state(self):
        mixin = CanBeReady(False)
        self.assertFalse(mixin.ready)

        mixinReady = CanBeReady(True)
        self.assertTrue(mixinReady.ready)

    def test_set_ready_changes_state(self):
        mixin = CanBeReady(False)
        self.assertFalse(mixin.ready)

        mixin._setReady()
        self.assertTrue(mixin.ready)

    def test_set_not_ready_changes_state(self):
        mixin = CanBeReady(True)
        self.assertTrue(mixin.ready)

        mixin._setNotReady()
        self.assertFalse(mixin.ready)

    def test_set_ready_triggers_event_if_not_ready(self):
        mixin = CanBeReady(False)

        readyEventMock = Mock()
        mixin.ready_event += readyEventMock

        mixin._setReady()

        readyEventMock.assert_called_once()

    def test_set_ready_does_not_trigger_event_if_ready(self):
        mixin = CanBeReady(True)

        readyEventMock = Mock()
        mixin.ready_event += readyEventMock

        mixin._setReady()

        readyEventMock.assert_not_called()

    def test_set_not_ready_triggers_event_if_ready(self):
        mixin = CanBeReady(True)

        notReadyEventMock = Mock()
        mixin.not_ready_event += notReadyEventMock

        mixin._setNotReady()

        notReadyEventMock.assert_called_once()

    def test_set_not_ready_does_not_trigger_event_if_not_ready(self):
        mixin = CanBeReady(False)

        notReadyEventMock = Mock()
        mixin.not_ready_event += notReadyEventMock

        mixin._setNotReady()

        notReadyEventMock.assert_not_called()


class TestCanFail(unittest.TestCase):
    def test_error_message_is_emitted(self):
        mixin = CanFail()

        errorEventMock = Mock()
        mixin.error_event += errorEventMock

        mixin.error_event('An error occured')

        errorEventMock.assert_called_once_with(mixin, 'An error occured')


@patch.multiple(CanSwitchOn, __abstractmethods__=set())
class TestCanSwitchOn(unittest.TestCase):
    def test_switchOn_calls_canSwitchOn(self):
        mixin = CanSwitchOn()

        with patch.object(mixin, 'canSwitchOn') as canSwitchOnMock:
            mixin.switchOn()

        canSwitchOnMock.assert_called_once()

    def test_switchOn_calls_doSwitchOn_if_canSwitchOn_true(self):
        mixin = CanSwitchOn()

        with patch.object(mixin, 'canSwitchOn', return_value=True), patch.object(mixin, 'doSwitchOn',
                                                                                 create=True) as doSwitchOnMock:
            mixin.switchOn()

        doSwitchOnMock.assert_called_once()

    def test_switchOn_does_not_call_doSwitchOn_if_canSwitchOn_false(self):
        mixin = CanSwitchOn()

        with patch.object(mixin, 'canSwitchOn', return_value=False), patch.object(mixin, 'doSwitchOn',
                                                                                  create=True) as doSwitchOnMock:
            mixin.switchOn()

        doSwitchOnMock.assert_not_called()

    def test_switchOn_calls_doSwitchOnComplete_if_doSwitchOn_not_present_and_canSwitchOn_true(self):
        mixin = CanSwitchOn()

        with patch.object(mixin, 'canSwitchOn', return_value=True), patch.object(mixin,
                                                                                 'doSwitchOnComplete') as doSwitchOnCompleteMock:
            mixin.switchOn()

        doSwitchOnCompleteMock.assert_called_once()

    def test_switchOn_does_not_call_doSwitchOnComplete_if_doSwitchOn_not_present_and_canSwitchOn_false(self):
        mixin = CanSwitchOn()

        with patch.object(mixin, 'canSwitchOn', return_value=False), patch.object(mixin,
                                                                                  'doSwitchOnComplete') as doSwitchOnCompleteMock:
            mixin.switchOn()

        doSwitchOnCompleteMock.assert_not_called()


@patch.multiple(CanSwitchOff, __abstractmethods__=set())
class TestCanSwitchOff(unittest.TestCase):
    def test_switchOff_calls_canSwitchOff(self):
        mixin = CanSwitchOff()

        with patch.object(mixin, 'canSwitchOff') as canSwitchOffMock:
            mixin.switchOff()

        canSwitchOffMock.assert_called_once()

    def test_switchOff_calls_doSwitchOff_if_canSwitchOff_true(self):
        mixin = CanSwitchOff()

        with patch.object(mixin, 'canSwitchOff', return_value=True), patch.object(mixin, 'doSwitchOff',
                                                                                  create=True) as doSwitchOffMock:
            mixin.switchOff()

        doSwitchOffMock.assert_called_once()

    def test_switchOff_does_not_call_doSwitchOff_if_canSwitchOff_false(self):
        mixin = CanSwitchOff()

        with patch.object(mixin, 'canSwitchOff', return_value=False), patch.object(mixin, 'doSwitchOff',
                                                                                   create=True) as doSwitchOffMock:
            mixin.switchOff()

        doSwitchOffMock.assert_not_called()

    def test_switchOff_calls_doSwitchOffComplete_if_doSwitchOff_not_present_and_canSwitchOff_true(self):
        mixin = CanSwitchOff()

        with patch.object(mixin, 'canSwitchOff', return_value=True), patch.object(mixin,
                                                                                  'doSwitchOffComplete') as doSwitchOffCompleteMock:
            mixin.switchOff()

        doSwitchOffCompleteMock.assert_called_once()

    def test_switchOff_does_not_call_doSwitchOffComplete_if_doSwitchOff_not_present_and_canSwitchOff_false(self):
        mixin = CanSwitchOff()

        with patch.object(mixin, 'canSwitchOff', return_value=False), patch.object(mixin,
                                                                                   'doSwitchOffComplete') as doSwitchOffCompleteMock:
            mixin.switchOff()

        doSwitchOffCompleteMock.assert_not_called()
