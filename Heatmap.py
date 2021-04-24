import pandas as pd
import plotly.express as pe
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash. dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
     html.Div([
        dcc.Input(
        id="input",
        type="text",
        placeholder="State",
        value='',
        ),
        html.Button('Enter', id='button'),  
        html.Div (id='output-container-button', children='enter a value and press submit'),
     ]),  
     
    dcc.Graph(id='us_heatmap', figure={}),
])

@app.callback(
        Output(component_id='us_heatmap',component_property='figure'),
        [Input(component_id='year',component_property='value')],
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
@app.callback(
        Output(component_id='output-container-button',component_property='children'),
        [Input(component_id='button', component_property='n_clicks')],
        [Input(component_id='input', component_property='value')]
    )
def update_output(n_clicks, value):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0] ## checking if button was clicked
    if 'button' in changed_id:
        tempDeaths = findState(value)  ## returns number of deaths in state
        tempCases = findCases(value)   ## returns number of comfirmed cases
        ##print(temp)
        return '{} has {} total deaths and {} confirmed cases'.format(
            value,
            f"{tempDeaths:,}",
            f"{tempCases:,}",
    ),
    
def findState(value):
    tempList = df['state'].tolist()
    datelist = df['date'].tolist()
    x = df['deaths'].tolist()
    total =0
    for i in range(len(datelist)):
        if value == tempList[i]:
            total = x[i]
            ##print(value)
               
    return total
def findCases(value):
    tempList = df['state'].tolist()
    datelist = df['date'].tolist()
    x = df['cases'].tolist()
    total =0
    for i in range(len(datelist)):
        if value == tempList[i]:
            total = x[i]
    return total
        
if __name__ == '__main__':
    app.run_server(debug=True)
