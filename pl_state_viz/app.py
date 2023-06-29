from dash import Dash, html, Input, Output, callback
import dash_mantine_components as dmc

from circuit import circuit
from utils import mpl_to_img_src, draw_circuit
from viz import plot_blochs

figs = [mpl_to_img_src(f) for f in plot_blochs(circuit)]

with open("pl_state_viz/circuit.py") as f:
    lines = f.readlines()

app = Dash()

code_card = dmc.Card(
    dmc.Prism(
        children="".join(lines[5:]),
        language="python",
        withLineNumbers=True,
    )
)

circ_card = dmc.Card(
    dmc.Image(
        src=draw_circuit(),
        width="100%",
    )
)

selector = dmc.NumberInput(
    label="Circuit Step",
    value=0,
    min=0,
    max=len(figs) - 1,
    step=1,
    style={"width": 250},
    id="selector",
)

state_viz = html.Div(
    id="state-viz",
)

app_cols = [
    dmc.Col(
        dmc.Stack([code_card, circ_card]),
        span=5,
    ),
    dmc.Col(
        dmc.Stack([selector, state_viz]),
        span=7,
    ),
]

app.layout = html.Div(
    dmc.Grid(app_cols),
)


@callback(
    Output(component_id="state-viz", component_property="children"),
    Input(component_id="selector", component_property="value"),
)
def show_state(sel_state):
    return dmc.Card(
        dmc.Image(
            src=figs[sel_state],
            width="100%",
        )
    )


if __name__ == "__main__":
    app.run(debug=True)
