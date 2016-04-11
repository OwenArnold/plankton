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
