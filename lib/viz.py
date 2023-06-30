import base64
import functools as ft

import matplotlib.pyplot as plt
import numpy as np
import pennylane as qml
import qutip as qt

from circuit import circuit
from io import BytesIO
from matplotlib.figure import Figure
from pennylane.pauli import PauliWord


def mpl_to_img_src(fig: Figure) -> str:
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format="png")
    encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")

    graph = "data:image/png;base64,{}".format(encoded)

    return graph


def draw_circuit() -> str:
    fig, ax = qml.draw_mpl(circuit, style="default")()

    return mpl_to_img_src(fig)


def exp_val(state: np.ndarray, obs: np.ndarray) -> float:
    return np.real(np.trace(obs @ np.outer(state, state.conj())))


def multi_bloch_coords(state: np.ndarray, n_qubits: int) -> list[list[float]]:
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


def plot_blochs_v2(state) -> list[list[str]]:
    state_spheres = []
    vecs = multi_bloch_coords(state, int(np.log2(len(state))))

    for i, v in enumerate(vecs):
        fig, ax = plt.subplots(
            constrained_layout=True,
            subplot_kw=dict(projection="3d"),
        )
        ax.set_title(f"q[{i}]")

        b = qt.Bloch(fig=fig, axes=ax)
        b.add_vectors(v)
        b.render()

        state_spheres += [mpl_to_img_src(fig)]
        plt.close()

    return state_spheres
