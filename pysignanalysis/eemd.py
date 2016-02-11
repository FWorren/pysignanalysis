import emd
import time
import numpy as np
from multiprocessing import Process, Queue


def eemd(x, sample_frequency, noise_std, max_modes, max_siftings, ensembles, ensembles_per_process):
    processes = []
    output = Queue(ensembles_per_process)
    start_overal = time.time()

    for i in range(ensembles/ensembles_per_process):
        emd_process = EnsembleProcess(sample_frequency, x, max_modes, max_siftings, noise_std, ensembles_per_process)
        emd_process.name = "Thread " + str(i+1)
        emd_process.start()
        output.put(emd_process)
        processes.append(emd_process)

    print "Process all processes total time: ", time.time() - start_overal

    imfs = np.ndarray((max_modes+1, len(x)))

    results = [output.get() for p in processes]

    for j in range(max_modes + 1):
        imfs[j] = np.multiply(results[j], 1.0/float(ensembles))

    return imfs


def eemd_without_threading(x, noise_std, max_modes, max_siftings, ensembles):
    imfs = np.ndarray((max_modes+1, len(x)))

    for i in range(ensembles):
        noise = np.random.randn(len(x))*noise_std
        x = x + noise
        imfs = emd.emd(x, max_modes, max_siftings)
        imfs = np.add(imfs, imfs)

    for j in range(max_modes + 1):
        imfs[j] = np.multiply(imfs[j], 1.0/float(ensembles))

    return imfs


def ensemble_emd(sample_frequency, x, max_modes, max_siftings, noise_std, ensembles_per_process, output):
    return 0


class EnsembleProcess(Process):
    def __init__(self, sample_frequency, x, max_modes, max_siftings, noise_std, ensembles_per_process):
        super(EnsembleProcess, self).__init__()
        self.imfs = np.ndarray((max_modes+1, len(x)))
        self.sample_frequency = sample_frequency
        self.x = x
        self.max_modes = max_modes
        self.max_siftings = max_siftings
        self.noise_std = noise_std
        self.ensembles_per_process = ensembles_per_process

    def get_imfs(self):
        return self.imfs

    def run(self):
        for i in range(self.ensembles_per_process):
            noise = np.random.randn(self.sample_frequency)*self.noise_std
            x = self.x + noise
            imfs = emd.emd(x, self.max_modes, self.max_siftings)
            self.imfs = np.add(self.imfs, imfs)

