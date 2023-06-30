import functools as ft
import matplotlib.pyplot as plt
import numpy as np
import pennylane as qml
import qutip as qt

from pennylane.pauli import PauliWord


def exp_val(state, obs):
    return np.real(np.trace(obs @ np.outer(state, state.conj())))


def multi_bloch_coords(state, n_qubits):
    coords = []

    for i in range(n_qubits):
        paulis = [
            PauliWord({n: "I" if n != i else pauli for n in range(n_qubits)})
            for pauli in ["X", "Y", "Z"]
        ]

        coords += [
            [
                exp_val(state, pauli.to_mat(wire_order=range(n_qubits)))
                for pauli in paulis
            ]
        ]

    return coords


def plot_blochs(circuit):
    figs = []

    snapshots = qml.snapshots(circuit)()
    for k in snapshots.keys():
        vecs = multi_bloch_coords(snapshots[k], 4)

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
