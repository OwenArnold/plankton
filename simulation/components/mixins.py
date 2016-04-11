from abc import ABCMeta, abstractmethod
from obsub import event


class CanBeReady(object):
    def __init__(self, initially_ready=False):
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


def make_constructor(name):
    def constructor(self, initial_value=0.0):
        setattr(self, '_' + name, initial_value)
        setattr(self, '_' + name + '_setpoint', initial_value)

    return constructor


def make_getter(name):
    def getter(self):
        return getattr(self, '_' + name)

    return getter


def make_setter(name):
    name_title = name.title()

    def setter(self, new_value):
        if getattr(self, 'canSet{}'.format(name_title))():
            setattr(self, '_{}_setpoint'.format(name), new_value)

            if hasattr(self, 'doSet{}'.format(name_title)):
                getattr(self, 'doSet{}'.format(name_title))()
            else:
                setattr(self, '_{}'.format(name), getattr(self, '_{}_setpoint'.format(name)))
                getattr(self, 'do{}SetpointReached'.format(name_title))()

    return setter


def do_nothing(self):
    pass


class ValueWithSetpointMixinMetaclass(ABCMeta):
    def __new__(cls, name, bases, attr):
        if len(bases) == 1:
            reduced_name = split_camel(name)[-1]
            reduced_name_lower = reduced_name.lower()

            attr['__init__'] = make_constructor(reduced_name_lower)
            attr[reduced_name_lower] = property(make_getter(reduced_name_lower), make_setter(reduced_name_lower))
            attr['canSet{}'.format(reduced_name)] = abstractmethod(lambda self: True)
            attr['do{}SetpointReached'.format(reduced_name)] = abstractmethod(do_nothing)

        return super(ValueWithSetpointMixinMetaclass, cls).__new__(cls, name, bases, attr)


class HasSpeed(object):
    __metaclass__ = ValueWithSetpointMixinMetaclass


class HasPhase(object):
    __metaclass__ = ValueWithSetpointMixinMetaclass
