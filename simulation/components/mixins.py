from abc import ABCMeta, abstractmethod
from obsub import event


class CanBeReady(object):
    def __init__(self, initially_ready=False):
        super(CanBeReady, self).__init__()
        self._ready = initially_ready

    @event
    def ready_event(self):
        pass

    @event
    def not_ready_event(self):
        pass

    @property
    def ready(self):
        return self._ready

    def _setReady(self):
        if not self.ready:
            self._ready = True
            self.ready_event()

    def _setNotReady(self):
        if self.ready:
            self._ready = False
            self.not_ready_event()


class CanFail(object):
    @event
    def error_event(self, message):
        pass


class CanStartStop(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(CanStartStop, self).__init__()

    @abstractmethod
    def canStart(self):
        return False

    @abstractmethod
    def doStartComplete(self):
        pass

    def start(self):
        if self.canStart():
            if hasattr(self, 'doStart'):
                self.doStart()
            else:
                self.doStartComplete()

    @abstractmethod
    def canStop(self):
        return False

    @abstractmethod
    def doStopComplete(self):
        pass

    def stop(self):
        if self.canStop():
            if hasattr(self, 'doStop'):
                self.doStop()
            else:
                self.doStopComplete()


class CanSwitchOn(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(CanSwitchOn, self).__init__()

    @abstractmethod
    def canSwitchOn(self):
        return False

    @abstractmethod
    def doSwitchOnComplete(self):
        pass

    def switchOn(self):
        if self.canSwitchOn():
            if hasattr(self, 'doSwitchOn'):
                self.doSwitchOn()
            else:
                self.doSwitchOnComplete()


class CanSwitchOff(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def canSwitchOff(self):
        return False

    @abstractmethod
    def doSwitchOffComplete(self):
        pass

    def switchOff(self):
        if self.canSwitchOff():
            if hasattr(self, 'doSwitchOff'):
                self.doSwitchOff()
            else:
                self.doSwitchOffComplete()


class CanLevitate(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(CanLevitate, self).__init__()

    @abstractmethod
    def canLevitate(self):
        return False

    @abstractmethod
    def doLevitateComplete(self):
        pass

    def levitate(self):
        if self.canLevitate():
            if hasattr(self, 'doLevitate'):
                self.doLevitate()
            else:
                self.doLevitateComplete()

    @abstractmethod
    def canDelevitate(self):
        return False

    @abstractmethod
    def doDelevitateComplete(self):
        pass

    def delevitate(self):
        if self.canDelevitate():
            if hasattr(self, 'doDelevitate'):
                self.doDelevitate()
            else:
                self.doDelevitateComplete()


import re


def split_camel(camelCaseName):
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', camelCaseName)


class ValueWithSetpointMixinMetaclass(ABCMeta):
    def __new__(cls, name, bases, attr):
        if len(bases) == 1 and bases[0] == object:
            reduced_name = split_camel(name)[-1]
            reduced_name_lower = reduced_name.lower()

            def constructor(self, initial_value=0.0):
                # Found at http://stackoverflow.com/questions/12757468
                MixinClass = next(c for c in type(self).__mro__ if c.__module__ == __name__ and c.__name__ == name)
                super(MixinClass, self).__init__()
                setattr(self, '_' + reduced_name_lower, initial_value)
                setattr(self, '_' + reduced_name_lower + '_setpoint', initial_value)

            def getter(self):
                return getattr(self, '_' + reduced_name_lower)

            def setter(self, new_value):
                setattr(self, '_{}_setpoint'.format(reduced_name_lower), new_value)

            def setAndExecute(self, new_value, execute=True):
                print 'Setting {} to new value {}'.format(reduced_name_lower, new_value)
                setattr(self, reduced_name_lower, new_value)

                if execute:
                    getattr(self, 'goTo{}Setpoint'.format(reduced_name))()

            def getSetpoint(self):
                return getattr(self, '_{}_setpoint'.format(reduced_name_lower))

            def isAtSetpoint(self):
                return getattr(self, '_{}'.format(reduced_name_lower)) == getattr(self,
                                                                                  '_{}'.format(reduced_name_lower))

            def goToSetpoint(self, *args):
                if getattr(self, 'canSet{}'.format(reduced_name))():
                    if hasattr(self, 'doSet{}'.format(reduced_name)):
                        getattr(self, 'doSet{}'.format(reduced_name))()
                    else:
                        setattr(self, '_{}'.format(reduced_name_lower),
                                getattr(self, '_{}_setpoint'.format(reduced_name_lower)))
                        getattr(self, 'do{}SetpointReached'.format(reduced_name))()

            def do_nothing(self, *args):
                pass

            attr['__init__'] = constructor
            attr[reduced_name_lower] = property(getter, setter)
            attr['set{}'.format(reduced_name)] = setAndExecute
            attr['isAt{}Setpoint'.format(reduced_name)] = isAtSetpoint
            attr['goTo{}Setpoint'.format(reduced_name)] = goToSetpoint

            attr['canSet{}'.format(reduced_name)] = abstractmethod(lambda self: True)
            attr['do{}SetpointReached'.format(reduced_name)] = abstractmethod(do_nothing)

        return super(ValueWithSetpointMixinMetaclass, cls).__new__(cls, name, bases, attr)


class HasSpeed(object):
    __metaclass__ = ValueWithSetpointMixinMetaclass


class HasPhase(object):
    __metaclass__ = ValueWithSetpointMixinMetaclass
