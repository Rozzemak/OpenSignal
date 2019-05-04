import numpy as np
import scipy as sc
from scipy import signal

class sim_sig_search:
    def __init__(self, it):
        self.l = []
        self.it = it

    def search_for_sim_sig(self):
        x1y1 = ([-3, 2, -1, 1], [-1, 0, -3, 2])
        x2y2 = ([-5, 3, -2, 1], [-4, 4, -2, 1])

        #return np.correlate(x1, y1, "same")
        #return np.corrcoef(x, y)
        return sc.signal.correlate2d(x1y1, x2y2, boundary='symm', mode='same')
