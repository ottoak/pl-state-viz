from circuit import circuit
from io import BytesIO
import base64
import pennylane as qml


def mpl_to_img_src(fig):
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format="png")
    encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")

    graph = "data:image/png;base64,{}".format(encoded)

    return graph


def draw_circuit():
    fig, ax = qml.draw_mpl(circuit, style="default")()

    return mpl_to_img_src(fig)
