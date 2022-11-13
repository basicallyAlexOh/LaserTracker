import Tracker

'''
Outline
DistanceFinderThread -> MotorControlThread - (calls) --> MotorLogger
Use mutex to ensure only 1 is locked at a time
Have Motor wait on a condition variable from DistanceFinder.
'''

class DistanceFinder:
    def __init__(self):
        self.__myTracker = Tracker()
        # include any extra class variables


    def calcRelDist(self):
        #call to Tracker.findLaser
        #use math to find distance in vector form to laser





