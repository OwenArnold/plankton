from fysom import Fysom as StateMachine

from mixins import CanBeReady, CanStartStop, CanFail, CanSwitchOn, CanSwitchOff, HasSpeed, HasPhase
from time import sleep
from threading import Thread, Timer


class ExecuteCallbackOnce(object):
    def __init__(self, fsm, state, callback):
        self._fsm = fsm
        self._state = state
        self._callback = callback

    def __call__(self, *args, **kwargs):
        if self._callback is not None:
            self._callback()

        delattr(self._fsm, 'on' + self._state)


def print_state(ev):
    print ev.src + ' ----> ' + ev.dst


class Motor(CanBeReady, CanStartStop, CanFail, CanSwitchOn, CanSwitchOff, HasSpeed, HasPhase, object):
    __metaclass__ = type

    def __init__(self):
        super(Motor, self).__init__()

        self._fsm = StateMachine({
            'initial': 'off',
            'events': [
                ('switch_on', 'off', 'on'),
                ('switch_off', 'on', 'off'),

                ('set_speed', 'on', 'accelerating'),
                ('speed_setpoint_reached', 'accelerating', 'phase_locking'),
                ('set_speed', 'accelerating', 'accelerating'),

                ('phase_setpoint_reached', 'phase_locking', 'phase_locked'),
                ('set_phase', 'phase_locked', 'phase_locking'),
                ('set_phase', 'phase_locking', 'phase_locking'),

                ('set_speed', 'phase_locking', 'accelerating'),
                ('set_speed', 'phase_locked', 'accelerating'),

                ('fail', '*', 'error')
            ],

            'callbacks': {
                'onchangestate': print_state,
                'onspeed_setpoint_reached': self.goToPhaseSetpoint,
                'onaccelerating': self.doSimulateSetSpeed,
                'onphase_locking': self.doSimulateSetPhase,
            }
        })

    def canStart(self):
        return not self.ready

    def doStartComplete(self):
        self._setReady()

    def doStart(self):
        self.switchOn()

    def canStop(self):
        return self.ready

    def doStopComplete(self):
        self._setNotReady()

    def canSwitchOn(self):
        return self._fsm.can('switch_on')

    def doSwitchOnComplete(self):
        self._fsm.switch_on()

    def canSwitchOff(self):
        return self._fsm.can('switch_off')

    def doSwitchOffComplete(self):
        self._fsm.switch_off()

    def canSetSpeed(self):
        return self._fsm.can('set_speed')

    def doSetSpeed(self):
        self._fsm.set_speed()

    def doSimulateSetSpeed(self, *args):
        self._speed = self._speed_setpoint
        self.doSpeedSetpointReached()
        return True

    def doSpeedSetpointReached(self):
        self._fsm.speed_setpoint_reached()

    def canSetPhase(self):
        return self._fsm.can('set_phase')

    def doSetPhase(self):
        self._fsm.set_phase()

    def doSimulateSetPhase(self, *args):
        self._phase = self._phase_setpoint
        self.doPhaseSetpointReached()
        return True

    def doPhaseSetpointReached(self):
        self._fsm.phase_setpoint_reached()

    def setSpeedAndPhase(self, new_speed, new_phase):
        self.speed = new_speed
        self.phase = new_phase


def equal(a, b, tolerance=1.0):
    return abs(a - b) < tolerance


class SlowMotor(Motor):
    def __init__(self, acceleration=1.0):
        super(SlowMotor, self).__init__()
        self._acceleration = acceleration

        self._thread = None

    def accelerate(self):
        acceleration = self._acceleration / 10.0

        while not equal(self._speed, self._speed_setpoint, 0.1):
            if self._speed < self._speed_setpoint:
                self._speed += acceleration
            elif self._speed > self._speed_setpoint:
                self._speed -= acceleration

            sleep(0.1)

        print 'T: ' + str(self._speed)
        self.doSpeedSetpointReached()

    def doSimulateSetSpeed(self, *args):
        if self._thread is None:
            self._thread = Thread(target=self.accelerate)
            self._thread.start()

        return False

    def lock_phase(self):
        self._phase = self._phase_setpoint
        self.doPhaseSetpointReached()

    def doSimulateSetPhase(self, *args):
        diff = abs(self._phase_setpoint - self._phase)
        timer = Timer(function=self.lock_phase, interval=diff / self._acceleration)
        timer.start()

        return False


if __name__ == '__main__':
    m = SlowMotor(5.0)

    m.start()
    m.setSpeedAndPhase(60.0, 15.0)

    while m._fsm.current != 'phase_locked':
        print m.speed, m.phase, m._fsm.current
        sleep(1.0)

    print m.speed, m.phase
    m.stop()
