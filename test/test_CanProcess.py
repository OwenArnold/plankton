#  -*- coding: utf-8 -*-
# *********************************************************************
# plankton - a library for creating hardware device simulators
# Copyright (C) 2016 European Spallation Source ERIC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *********************************************************************

from mock import call, patch
import unittest

from simulation.core import CanProcess, CanProcessComposite


class TestCanProcess(unittest.TestCase):
    def test_process_calls_doProcess(self):
        processor = CanProcess()

        with patch.object(processor, 'doProcess', create=True) as doProcessMock:
            processor.process(1.0)

        doProcessMock.assert_called_once_with(1.0)

    def test_process_calls_doBeforeProcess_only_if_doProcess_is_present(self):
        processor = CanProcess()

        with patch.object(processor, 'doBeforeProcess', create=True) as doBeforeProcessMock:
            processor.process(1.0)

            doBeforeProcessMock.assert_not_called()

            with patch.object(processor, 'doProcess', create=True):
                processor.process(2.0)

            doBeforeProcessMock.assert_called_once_with(2.0)

    def test_process_calls_doAfterProcess_only_if_doProcess_is_present(self):
        processor = CanProcess()

        with patch.object(processor, 'doAfterProcess', create=True) as doAfterProcess:
            processor.process(1.0)

            doAfterProcess.assert_not_called()

            with patch.object(processor, 'doProcess', create=True):
                processor.process(2.0)

            doAfterProcess.assert_called_once_with(2.0)

    @patch.object(CanProcess, 'process')
    def test_call_invokes_process(self, processMock):
        processor = CanProcess()

        processor(45.0)

        processMock.assert_called_once_with(45.0)


class TestCanProcessComposite(unittest.TestCase):
    def test_process_calls_doBeforeProcess_if_present(self):
        composite = CanProcessComposite()

        with patch.object(composite, 'doBeforeProcess', create=True) as doBeforeProcessMock:
            composite.process(3.0)

        doBeforeProcessMock.assert_called_once_with(3.0)

    def test_addProcessor_if_argument_CanProcess(self):
        composite = CanProcessComposite()

        with patch.object(composite, '_appendProcessor') as appendProcessorMock:
            composite.addProcessor(CanProcess())

        appendProcessorMock.assert_called_once()

    def test_addProcessor_if_argument_not_CanProcess(self):
        composite = CanProcessComposite()

        with patch.object(composite, '_appendProcessor') as appendProcessorMock:
            composite.addProcessor(None)

        appendProcessorMock.assert_not_called()

    def test_init_from_iterable(self):
        with patch.object(CanProcess, 'doProcess', create=True) as mockProcessMethod:
            simulations = (CanProcess(), CanProcess(),)

            composite = CanProcessComposite(simulations)
            composite(4.0)

            mockProcessMethod.assert_has_calls([call(4.0), call(4.0)])
