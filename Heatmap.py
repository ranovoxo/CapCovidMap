import pandas as pd
import plotly.express as pe
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash. dependencies import Input, Output
import plotly.io as pio
app = dash.Dash(__name__)

df = pd.read_csv("us-statesdates.csv")#changed
df2 = pd.read_csv("csvData.csv")
df = pd.merge(df, df2)

print (df)
app.layout = html.Div([

    dcc.Dropdown(id="year",
        options=[
            {"label": "2021", "value":2021}],
        value=2021,
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
            locations='Code',#changed
            animation_frame='date',
            scope='usa',
            color='cases',#changed
            hover_data=['state','cases','date'],#changed
            color_continuous_scale=pe.colors.sequential.Aggrnyl[::-1],
            labels={'cases': 'Number of positive cases: '},#changed
            template='seaborn'
            #template='plotly_dark'
        
        )
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 10
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
