
import weakref
import Servo

from actor import Actor, actormethod
from publish import PublisherMixIn, Message


__all__ = ['ServoActor']

class ServoActor(Actor, PublisherMixIn):
    def __init__(self, port, servoConfig):
        self.port = port
        self.servo = Servo.Servo(self.port)

        PublisherMixIn.__init__(self)
        Actor.__init__(self)

    def die(self):
        self.servo.closeServoPort()
        self.queue.join()
        self.reallydie()
        del self.servo
    
    @actormethod
    def reallydie(self):
        raise ActorQuit

        

__actors = {}
def getServoActor(port):
        ip,p = port
        if ip in __actors :
            servotor = __actors[ip]()
            if servotor:
                return servotor
            else:
                del __actors[ip]
        
        servotor = ServoActor(port)
        __actors[ip] = weakref.ref(servotor)

        return servotor