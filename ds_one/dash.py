
from dash import html
from dash import dcc

import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash

app = DjangoDash('dash')



df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")


app.layout = html.Div(style={}, children=[


    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
])
