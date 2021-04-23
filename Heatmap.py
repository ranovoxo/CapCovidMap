import pandas as pd
import plotly.express as pe
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash. dependencies import Input, Output
import timeline

app = dash.Dash(__name__)

df = pd.read_csv("States.csv")
print (df[:5])

app.layout = html.Div([

    dcc.Dropdown(id="year",
        options=[
            {"label": "2021", "value":2021}],
        value=2021,
        ),
    dcc.RangeSlider(
        id='my_slider',
        min = 1,
        max = timeline.maxMarks,
        step = 1,
        value = [1],
        marks = timeline.tags,
    ),
    dcc.Graph(id='us_heatmap', figure={})

])

@app.callback(
        Output(component_id='us_heatmap',component_property='figure'),
        [Input(component_id='year',component_property='value')]
    )
def graph(current_year):

    fig = pe.choropleth(
            data_frame=df,
            locationmode='USA-states',
            locations='State_code',
            scope='usa',
            color= 'Deaths',
            hover_data=['State','Deaths'],
            color_continuous_scale=pe.colors.sequential.Aggrnyl[::-1],
            labels={'Deaths': 'Cumulative Number of Deaths as of Apr 6 2021'},
            template='seaborn'
            #template='plotly_dark'
        )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
