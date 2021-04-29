import pandas as pd
import plotly.express as pe
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash. dependencies import Input, Output
import dash_bootstrap_components as dbc

#loading information about the counties
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

state_df = pd.read_csv("us-statesdates.csv")#changed
df2 = pd.read_csv("csvData.csv")
state_df = pd.merge(state_df, df2)

county_df= pd.read_csv('us-counties.csv')
county_df['new_date'] = pd.to_datetime(county_df['date'])
county_df['Year-Week'] = county_df['new_date'].dt.strftime('%Y-%U')
county_df.head()

county_df.shape
county_df = county_df.sort_values(by=['county', 'state', 'new_date'])
df_us = county_df.groupby(['county', 'state', 'fips', 'Year-Week']).first().reset_index()
df_us
df_us.head(100)
df_us['cases'].max(), df_us['cases'].min()
counties["features"][100]
df_us = df_us.sort_values(by=['Year-Week'])
# print (df)

# fig = pe.choropleth(
#     data_frame=df,
#     locationmode='USA-states',
#     locations='Code',#changed
#     animation_frame='date',
#     scope='usa',
#     color='cases',#changed
#     hover_data=['state','cases','date'],#changed
#     color_continuous_scale=pe.colors.sequential.Aggrnyl[::-1],
#     labels={'cases': 'Number of positive cases: '},#changed
#     template='seaborn'
#     #template='plotly_dark'

#     )
# fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
# fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 10

app.layout = html.Div([
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

    dcc.RadioItems(id="slct_map",
        options=[
            {'label': 'County', 'value': 'county'},
            {'label': 'State',  'value': 'state'}
        ],
        value='county'
    ),
    html.Br(),
    dcc.Graph(id='heatmap', figure={})
])

@app.callback(
    Output(component_id='heatmap', component_property='figure'),
    Input(component_id='slct_map', component_property='value')
)
def update_map(option_slctd):

    if option_slctd == 'county':
        fig = pe.choropleth(
            data_frame=df_us,
            geojson=counties,
            #locationmode='USA-states',
            locations='fips',#changed
            animation_frame='Year-Week',
            scope='usa',
            color='cases',#changed
            hover_data=['county','cases','date'],#changed
            color_continuous_scale=pe.colors.sequential.Aggrnyl[::-1],
            labels={'cases': 'Number of positive cases: '},#changed
            template='seaborn'
            #template='plotly_dark'

            )
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 10

    if option_slctd == 'state':
        fig = pe.choropleth(
            data_frame=state_df,
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
    tempList = state_df['state'].tolist()
    datelist = state_df['date'].tolist()
    x = state_df['deaths'].tolist()
    total =0
    for i in range(len(datelist)):
        if value == tempList[i]:
            total = x[i]
            ##print(value)

    return total
def findCases(value):
    tempList = state_df['state'].tolist()
    datelist = state_df['date'].tolist()
    x = state_df['cases'].tolist()
    total =0
    for i in range(len(datelist)):
        if value == tempList[i]:
            total = x[i]
    return total

if __name__ == '__main__':
    app.run_server(debug=True)
