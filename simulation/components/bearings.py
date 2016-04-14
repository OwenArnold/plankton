from fysom import Fysom as StateMachine

from threading import Timer
from time import sleep

from mixins import CanBeReady, CanFail, CanStartStop, CanSwitchOn, CanSwitchOff, CanLevitate


def print_state(ev):
    print ev.src + ' ----> ' + ev.dst


class Bearing(CanBeReady, CanStartStop, CanFail, object):
    def canStart(self):
        return not self.ready

    def canStop(self):
        return self.ready

    def doStartComplete(self):
        self._setReady()

    def doStopComplete(self):
        self._setNotReady()


class MechanicalBearing(Bearing):
    def __init__(self):
        super(MechanicalBearing, self).__init__()

        self._setReady()

    def doStop(self):
        pass


class MagneticBearing(CanSwitchOn, CanSwitchOff, CanLevitate, Bearing):
    def __init__(self):
        super(MagneticBearing, self).__init__()

        self._fsm = StateMachine({
            'initial': 'off',
            'events': [
                ('switch_on', 'off', 'resting'),
                ('switch_off', 'resting', 'off'),

                ('levitate', 'resting', 'levitating'),
                ('levitation_stable', 'levitating', 'levitated'),
                ('delevitate', 'levitated', 'resting'),

                ('fail', '*', 'error')
            ],

            'callbacks': {
                'onchangestate': print_state,
                'onlevitated': self.doLevitateComplete,
                'onleavelevitated': self.doDelevitateComplete,
                'onerror': self._handle_error,
            }

        })

    def _handle_error(self, ev):
        self.error_event('Error occured in state \'{}\': {}'.format(ev.src, ev.error_message))

    def doStart(self):
        self.switchOn()
        self.levitate()

    def doStop(self):
        self.delevitate()

    def canSwitchOn(self):
        return self._fsm.can('switch_on')

    def doSwitchOnComplete(self):
        self._fsm.switch_on()

    def canSwitchOff(self):
        return self._fsm.can('switch_off')

    def doSwitchOffComplete(self):
        self._fsm.switch_off()

    def canLevitate(self):
        return self._fsm.can('levitate')

    def doLevitate(self):
        self._fsm.levitate()
        self._simulateLevitation()

    def doLevitateComplete(self, *args):
        self.doStartComplete()

    def canDelevitate(self):
        return self._fsm.can('delevitate')

    def doDelevitate(self):
        self._fsm.delevitate()

    def doDelevitateComplete(self, ev):
        self.doStopComplete()

    def _simulateLevitation(self):
        if hasattr(self, 'doSimulateLevitation'):
            self.doSimulateLevitation()
        else:
            self.simulateLevitationSuccess()

    def simulateLevitationSuccess(self):
        self._fsm.levitation_stable()

    def simulateLevitationFailure(self, message):
        self._fsm.fail(error_message=message)


class TimedMagneticBearing(MagneticBearing):
    def __init__(self, levitation_time):
        super(TimedMagneticBearing, self).__init__()

        self._levitation_time = levitation_time

    def doSimulateLevitation(self):
        sleep(self._levitation_time)
        self.simulateLevitationSuccess()


if __name__ == '__main__':
    b = TimedMagneticBearing(2.0)
    b.start()
    b.stop()
