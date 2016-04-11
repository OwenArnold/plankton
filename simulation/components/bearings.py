from fysom import Fysom as StateMachine

from threading import Timer
from time import sleep

from mixins import CanBeReady, CanFail, CanSwitchOn, CanSwitchOff, CanLevitate


class Bearing(CanBeReady, CanFail, object):
    def start(self):
        if not self.ready:
            if hasattr(self, 'doStart'):
                self.doStart()
            else:
                self.doStartComplete()

    def stop(self):
        if self.ready:
            if hasattr(self, 'doStop'):
                self.doStop()
            else:
                self.doStopComplete()

    def doStartComplete(self):
        self._setReady()

    def doStopComplete(self):
        self._setNotReady()


class MechanicalBearing(Bearing):
    def __init__(self):
        super(MechanicalBearing, self).__init__()

        self._ready = True


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
                'onlevitating': self._simulateLevitation,
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

    def doLevitateComplete(self, *args):
        self.doStartComplete()

    def canDelevitate(self):
        return self._fsm.can('delevitate')

    def doDelevitate(self):
        self._fsm.delevitate()

    def doDelevitateComplete(self, ev):
        self.doStopComplete()

    def _simulateLevitation(self, ev):
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

        self._timer = Timer(interval=levitation_time,
                            function=self.simulateLevitationSuccess)

    def doSimulateLevitation(self):
        self._timer.start()


class BlockingTimedMagneticBearing(MagneticBearing):
    def __init__(self, levitation_time):
        super(BlockingTimedMagneticBearing, self).__init__()

        self._levitation_time = levitation_time

    def doSimulateLevitation(self):
        sleep(self._levitation_time)
        self.simulateLevitationSuccess()
