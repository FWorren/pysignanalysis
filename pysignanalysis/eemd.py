import emd
import time
import numpy as np
from threading import Thread


def eemd(x, sample_frequency, noise_std, max_modes, ensembles):
    threads = []
    start_overal = time.time()
    for i in range(ensembles):
        noise = np.random.randn(sample_frequency)*noise_std
        x = x + noise
        emd_task = Emd(x, max_modes)
        emd_task.setName("Thread " + str(i+1))
        emd_task.start()
        threads.append(emd_task)
    print "Process time all threads: ", time.time() - start_overal
    imfs = np.ndarray((max_modes+1, len(x)))
    i = 0

    for thread in threads:
        thread.join()
        for k in range(max_modes+1):
            imfs[k] = np.add(imfs[k], thread.get_imfs()[k])
        i += 1

    for j in range(max_modes + 1):
        imfs[j] = np.multiply(imfs[j], 1.0/float(ensembles))

    return imfs


class Emd(Thread):
    def __init__(self, x, max_modes):
        super(Emd, self).__init__()
        self.imfs = np.ndarray((max_modes+1, len(x)))
        self.x = x
        self.max_modes = max_modes

    def get_imfs(self):
        return self.imfs

    def run(self):
        self.imfs = emd.emd(self.x, self.max_modes)
