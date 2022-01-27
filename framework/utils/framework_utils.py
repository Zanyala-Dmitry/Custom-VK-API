import time
from project.resources.constains.constants import Constants


class ConditionalWait:
    @staticmethod
    def wait_for(condition):
        timer = ConditionalWait.get_millis() + Constants.TIMEOUT_SECONDS*1000
        cycle_time = Constants.CYCLE_MILLISECONDS
        timer_cycle = ConditionalWait.get_millis()
        while timer > ConditionalWait.get_millis():
            if ConditionalWait.get_millis() - timer_cycle > cycle_time:
                timer_cycle = ConditionalWait.get_millis()
                if condition:
                    return True
        return False

    @staticmethod
    def get_millis():
        return time.time() * 1000
