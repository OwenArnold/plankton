from fysom import Fysom as StateMachine

from mixins import CanBeReady, CanStartStop, CanFail, CanSwitchOn, CanSwitchOff, HasSpeed, HasPhase


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
                ('set_phase', 'accelerating', 'accelerating'),

                ('set_speed', 'phase_locking', 'accelerating'),
                ('set_speed', 'phase_locked', 'accelerating'),

                ('fail', '*', 'error')
            ],
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
        self._speed = self._speed_setpoint
        self.doSpeedSetpointReached()

    def doSpeedSetpointReached(self):
        self._fsm.speed_setpoint_reached()

    def canSetPhase(self):
        return self._fsm.can('set_phase')

    def doPhaseSetpointReached(self):
        self._fsm.phase_setpoint_reached()


if __name__ == '__main__':
    m = Motor()

    m.start()
    m.speed = 100.0

    print m._fsm.current
    print m.speed, m._speed_setpoint
