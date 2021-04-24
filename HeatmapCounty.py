import pandas as pd
import plotly.express as pe
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash. dependencies import Input, Output
import dash_bootstrap_components as dbc

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df= pd.read_csv('us-counties.csv')
df['new_date'] = pd.to_datetime(df['date'])
df['Year-Week'] = df['new_date'].dt.strftime('%Y-%U')
df.head()

df.shape
df = df.sort_values(by=['county', 'state', 'new_date'])
df_us = df.groupby(['county', 'state', 'fips', 'Year-Week']).first().reset_index()
df_us
df_us.head(100)
df_us['cases'].max(), df_us['cases'].min()
counties["features"][100]
df_us = df_us.sort_values(by=['Year-Week'])
#df = pd.read_csv("us-counties.csv")#changed
#df2 = pd.read_csv("csvData.csv")
#df = pd.merge(df, df2)
#dropstates = dropstates.drop("Alabama", "Alaska", "American Samoa", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Guam", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Minor Outlying Islands", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Northern Mariana Islands", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "U.S. Virgin Islands", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming")
#df.drop(df.state!='Texas')
print (df)

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

    dcc.Graph(figure=fig)
])
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
