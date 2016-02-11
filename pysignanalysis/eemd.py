import emd
import time
import numpy as np
from threading import Thread


def eemd(x, sample_frequency, noise_std, max_modes, ensembles, ensembles_per_thread):
    threads = []
    start_overal = time.time()
    for i in range(ensembles/ensembles_per_thread):
        emd_task = Emd(sample_frequency, x, max_modes, noise_std, ensembles_per_thread)
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
    def __init__(self, sample_frequency, x, max_modes, noise_std, ensembles_per_thread):
        super(Emd, self).__init__()
        self.imfs = np.ndarray((max_modes+1, len(x)))
        self.sample_frequency = sample_frequency
        self.x = x
        self.max_modes = max_modes
        self.noise_std = noise_std
        self.ensembles_per_thread = ensembles_per_thread

    def get_imfs(self):
        return self.imfs

    def run(self):
        for i in range(self.ensembles_per_thread):
            noise = np.random.randn(self.sample_frequency)*self.noise_std
            x = self.x + noise
            imfs = emd.emd(x, self.max_modes)
            self.imfs = np.add(self.imfs, imfs)
