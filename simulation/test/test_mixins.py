from ..components import CanSwitchOn, CanSwitchOff

import unittest
from mock import patch, Mock


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
