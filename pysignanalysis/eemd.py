import emd
import numpy as np
from multiprocessing import Process, Queue


def eemd(x, noise_std, max_modes, max_siftings, ensembles, ensembles_per_process):
    n_processes = ensembles / ensembles_per_process
    data_length = len(x)
    noise_std *= np.max(x)
    output = Queue(n_processes)

    processes = [
        Process(
            target=ensemble_process,
            args=(
                x,
                data_length,
                max_modes,
                max_siftings,
                noise_std,
                ensembles_per_process,
                output
            )
        )
        for p in range(n_processes)
    ]

    for p in processes:
        p.start()

    results = [output.get() for p in processes]

    imfs = ensemble_all_processes(data_length, results, n_processes, ensembles, max_modes)

    return imfs


def init_procesess(x, noise_std, max_modes, max_siftings, n_processes, data_length, ensembles_per_process):
    processes = [
        Process(
            target=ensemble_process,
            args=(
                x,
                data_length,
                max_modes,
                max_siftings,
                noise_std,
                ensembles_per_process,
                output
            )
        )
        for p in range(n_processes)
    ]
    return processes

def ensemble_all_processes(data_length, results, n_processes, ensembles, max_modes):
    imfs = np.zeros((max_modes + 1, data_length))

    for j in range(n_processes):
        imfs = np.add(imfs, results[j])

    imfs = np.multiply(imfs, 1.0/float(ensembles))

    return imfs


def ensemble_process(x, data_length, max_modes, max_siftings, noise_std, ensembles_per_process, output):
    imfs = np.zeros((max_modes + 1, data_length))

    for i in range(ensembles_per_process):
        noise = np.multiply(np.random.randn(data_length), noise_std)
        noise_assisted_data = np.add(x, noise)
        ensemble = emd.emd(noise_assisted_data, max_modes, max_siftings)
        imfs = np.add(imfs, ensemble)

    output.put(imfs)
