from abc import ABCMeta, abstractmethod


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
