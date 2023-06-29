import functools as ft
import matplotlib.pyplot as plt
import numpy as np
import pennylane as qml
import qutip as qt

I = np.eye(2, 2)
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])


def exp_val(state, obs):
    return np.real(np.trace(obs @ np.outer(state, state.conj())))


def multi_bloch(state, n_qubits):
    coords = []

    for i in range(n_qubits):
        _X = ft.reduce(np.kron, [I] * i + [X] + [I] * (n_qubits - 1 - i))
        _Y = ft.reduce(np.kron, [I] * i + [Y] + [I] * (n_qubits - 1 - i))
        _Z = ft.reduce(np.kron, [I] * i + [Z] + [I] * (n_qubits - 1 - i))

        coords += [[exp_val(state, _X), exp_val(state, _Y),
                    exp_val(state, _Z)]]

    return coords


def plot_blochs(circuit):
    figs = []

    snapshots = qml.snapshots(circuit)()
    for k in snapshots.keys():
        vecs = multi_bloch(snapshots[k], 4)

        fig, axs = plt.subplots(
            1,
            4,
            constrained_layout=True,
            figsize=(20, 7),
            subplot_kw=dict(projection="3d"),
        )
        fig.suptitle(f"Circuit State {k}")

        for i, v in enumerate(vecs):
            b = qt.Bloch(fig=fig, axes=axs[i])
            b.add_vectors(v)
            b.render()
            axs[i].set_title(f"q[{i}]")

        figs += [fig]

    return figs


def map_to_sphere(z):
    if not z[0]:
        return [0, 0, -1]

    ux = np.real(z[1] / z[0])
    uy = np.imag(z[1] / z[0])

    Px = 2 * ux / (1 + ux**2 + uy**2)
    Py = 2 * uy / (1 + ux**2 + uy**2)
    Pz = (1 - ux**2 - uy**2) / (1 + ux**2 + uy**2)

    return [Px, Py, Pz]
