import json
import time
import sys
import RPi.GPIO as GPIO

class Focuser(object):
    stepcounter = 0
    
    maxsteps = 3500
    started = False
    stopRUN = True
    initalized = False

    # Verwendete Pins des ULN2003A auf die Pins des Rapberry Pi zugeordnet
    StepPins = [4,17,27,22]

    # Define advanced sequence
    # as shown in manufacturers datasheet
    Seq = [[1,0,0,1],
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1]]

    StepCount = len(Seq) # Max Steps in der Sequenz
    StepCounter = 0      # Stand in der Sequenz  

    wait = 6000

    # Umdrehung links herum
    @staticmethod
    def left(step):
            Focuser.step(step, -2)

    # Umdrehung rechts herum
    @staticmethod
    def right(step):
            Focuser.step(step, 2)


    @staticmethod
    def init():
        GPIO.setmode(GPIO.BCM)
        # Set all pins as output
        for pin in Focuser.StepPins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)
        
    @staticmethod
    def end():
        GPIO.cleanup()
        return 'ended'


    @staticmethod
    def go(i):
        if not Focuser.started:
            Focuser.started = True
            Focuser.stopRUN = False
            while not Focuser.stopRUN and Focuser.stepcounter < Focuser.maxsteps:
                time.sleep(1)
                Focuser.stepcounter +=1

    @staticmethod
    def stop(i):
        Focuser.stopRUN = True
        return 'stoped!'

    @staticmethod
    def getstatus(i):
        if Focuser.initalized:
            return json.dumps(Focuser.stepcounter)
        else:
            return json.dumps("Failed. Initialise first")


    ###  Set direction to 1 or 2 for clockwise
    ### Set direction to -1 or -2 for anti-clockwise
    @staticmethod
    def step(steps, direction):

        if(direction > 0):
            Focuser.stepcounter += 1
        else:
            Focuser.stepcounter -= 1

        StepDir = direction 
        # Read wait time from command line
        if len(sys.argv)>1:
            WaitTime = int(sys.argv[1])/float(Focuser.wait)
        else:
            WaitTime = 10/float(Focuser.wait)


        for pin in range(0, 4):
            xpin = Focuser.StepPins[pin]
            if Focuser.Seq[Focuser.StepCounter][pin]!=0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
        Focuser.StepCounter += StepDir

        # If we reach the end of the sequence
        # start again
        if (Focuser.StepCounter>=Focuser.StepCount):
            Focuser.StepCounter = 0
        if (Focuser.StepCounter<0):
            Focuser.StepCounter = Focuser.StepCount+ StepDir

        # Wait before moving on
        time.sleep(WaitTime)

