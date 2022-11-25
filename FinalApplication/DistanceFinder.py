import threading
from runner import Runner

class DistanceFinder(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        print("Created Distance Finder")

    def run(self):
        while Runner.initialPath:
            with Runner.condVar:
                while not Runner.pointReady:
                    Runner.condVar.wait()
                Runner.lock1.acquire()
                x,y = self.find_distance()
                Runner.relPos = (x,y)
                Runner.lock1.release()


    def find_distance(self):
        a, b = Runner.laserPos
        if a == -1 and b == -1:
            return -1, -1
        d = 40017 * pow(b, -1.376)

        ######################################
        # Bounds to find off-center distance #
        ######################################
        fL10 = lambda x: -0.11 * x * x + 12.86 * x - 164.4
        fL5 = lambda x: -0.0864 * x * x + 9.3043 * x + 16.8
        fCenter = lambda x: 314
        fR5 = lambda x: 0.0764 * x * x - 8.3843 * x + 603.4
        fR10 = lambda x: 0.1064 * x * x - 12.784 * x + 811.9

        if a < fL10(d):
            # TODO: Fix this for linearization
            # print("Greater than L10")
            return d, -10
        elif a < fL5(d):
            # print("Between 10 and 5 L")
            k = a - fL10(d)
            j = fL5(d) - a
            return d, (-10) * (j / (k + j)) + (-5) * (k / (k + j))
        elif a < fCenter(d):

            # print("Between 5 and 0 L")
            k = a - fL5(d)
            j = fCenter(d) - a
            return d, (-5) * (j / (k + j)) + (0) * (k / (k + j))
        elif a < fR5(d):

            # print("Between 0 and 5 R")
            k = a - fCenter(d)
            j = fR5(d) - a
            return d, (0) * (j / (k + j)) + (5) * (k / (k + j))

        elif a < fR10(d):
            # print("Between 5 and 10 R")
            k = a - fR5(d)
            j = fR10(d) - a
            return d, (5) * (j / (k + j)) + (10) * (k / (k + j))
        else:
            # TODO: Fix this for linearization
            # print("Greater than R10")
            return d, 10