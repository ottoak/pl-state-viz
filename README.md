### PennyLane Circuuit Visualizer
___

Simple tool built using `QuTIP` and `Dash` to visualize states in a PennyLane circuit. Utilizies `qml.snapshot()` from PennyLane to capture intermediate states, and `QuTIP`'s bloch sphere tools for visualization.

Requires `poetry`. To run:

```
poetry install
poetry run python lib/app.py
```

You can edit `circuit.py` to change the circuit, including `qml.snapshot()` wherever you want to get a state visualization.

The app will refresh on any file save, so you can in theory edit the circuit in real-time - though if you save the file and there is an error the app will crash :) It may also only work for 4 qubits at the moment...