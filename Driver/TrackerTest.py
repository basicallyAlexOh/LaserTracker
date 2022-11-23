import sys
# path to Lasertracker must be changed to run on pi
sys.path.append('D:\WIndows\Documents\LaserTracker\LaserTracking')
import Tracker

t = Tracker.Tracker()
t.findLaser()

