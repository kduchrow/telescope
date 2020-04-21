import json
import time

class Focuser(object):
    counter = 1
    started = False
    stopRUN = True

    @staticmethod
    def go(i):
        if not Focuser.started:
            Focuser.started = True
            Focuser.stopRUN = False
            while not Focuser.stopRUN:
                time.sleep(1)
                Focuser.counter +=1

    @staticmethod
    def stop(i):
        Focuser.stopRUN = True
        return 'stoped!'

    @staticmethod
    def getstatus(i):
        return json.dumps(Focuser.counter)


