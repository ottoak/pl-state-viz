import pennylane as qml

dev = qml.device("default.qubit", wires=4)


@qml.qnode(dev)
def circuit():
    qml.Snapshot()

    qml.pow(qml.PauliY(wires=0), 1 / 4)
    qml.pow(qml.PauliY(wires=1), 1 / 4)
    qml.pow(qml.PauliY(wires=2), 1 / 4)
    qml.pow(qml.PauliY(wires=3), 1 / 4)
    qml.Snapshot()

    qml.ctrl(qml.T, 0)(wires=1)
    qml.Snapshot()

    qml.ctrl(qml.T, 1)(wires=2)
    qml.Snapshot()

    qml.ctrl(qml.T, 2)(wires=3)
    qml.Snapshot()

    qml.ctrl(qml.T, 3)(wires=0)

    return qml.state()
