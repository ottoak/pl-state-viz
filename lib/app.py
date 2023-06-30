from dash import Dash, html, Input, Output, callback
import dash_mantine_components as dmc

from circuit import states
from viz import plot_blochs_v2, draw_circuit

state_labels = list(states.keys())
state_spheres = {state: plot_blochs_v2(states[state]) for state in states.keys()}

with open("lib/circuit.py") as f:
    lines = f.readlines()

app = Dash()

code_card = dmc.Card(
    dmc.Prism(
        children="".join(lines[5:-2]),
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
    max=len(states) - 1,
    step=1,
    style={"width": 250},
    id="selector",
)

state_viz = dmc.Grid(id="state-viz", children=[])

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
def show_state(sel_state: int):
    children = []

    for i, fig_src in enumerate(state_spheres[state_labels[sel_state]]):
        card = dmc.Card(
            children=[
                dmc.Center(
                    dmc.Badge(f"q[{i}]", color="red", variant="light", size="lg")
                ),
                dmc.Center(
                    dmc.Image(
                        src=fig_src,
                        style={"width": "75%", "height": "75%"},
                    ),
                    mt=10,
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"width": "90%", "height": 250},
        )

        children += [
            dmc.Col(
                card,
                span=6,
            )
        ]

    return children


if __name__ == "__main__":
    app.run(debug=True)
