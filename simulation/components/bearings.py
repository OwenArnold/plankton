from fysom import Fysom as StateMachine
from obsub import event


class Bearing(object):
    def __init__(self):
        self._ready = False

    @event
    def ready_event(self):
        pass

    @event
    def not_ready_event(self):
        pass

    @event
    def error_event(self, message):
        pass

    @property
    def ready(self):
        return self._ready

    def start(self):
        if not self._ready:
            if hasattr(self, 'doStart'):
                self.doStart()
            else:
                self._start_complete()

    def stop(self):
        if self._ready:
            if hasattr(self, 'doStop'):
                self.doStop()
            else:
                self._stop_complete()

    def _start_complete(self):
        self._ready = True
        self.ready_event()

    def _stop_complete(self):
        self._ready = False
        self.not_ready_event()


class MechanicalBearing(Bearing):
    def __init__(self):
        super(MechanicalBearing, self).__init__()

        self._ready = True


class MagneticBearing(Bearing):
    def __init__(self):
        super(MagneticBearing, self).__init__()

        self._fsm = StateMachine({
            'initial': 'off',
            'events': [
                ('switch_on', 'off', 'resting'),
                ('switch_off', 'resting', 'off'),

                ('levitate', 'resting', 'levitating'),
                ('levitation_stable', 'levitating', 'levitated'),
                ('delevitate', 'levitated', 'delevitating'),
                ('delevitation_complete', 'delevitating', 'resting'),

                ('fail', '*', 'error')
            ],
            'callbacks': {
                'onlevitated': self.ready_event,
                'onresting': self.not_ready_event,
                'onerror': self._handle_error,
            }

        })

    def _handle_error(self, event):
        self.error_event('Error occured in state \'{}\': {}'.format(self._state, event.error_message))

    def doStart(self):
        if self._fsm.isstate('off'):
            self._fsm.switch_on()

        if self._fsm.isstate('resting'):
            self._fsm.levitate()

        if self._fsm.isstate('levitating'):
            self._fsm.levitation_stable()

        self._start_complete()

    def doStop(self):
        if self._fsm.isstate('levitated'):
            self._fsm.delevitate()

        if self._fsm.isstate('delevitating'):
            self._fsm.delevitation_complete()

        self._stop_complete()
