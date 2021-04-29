# CapCovidMap

In this repositoty you can find useful resources which will provide you with
daily state COVID data as well as county data. This repository also include a
heatmap for the statewide total number of cases(included in Heatmap.py).
You can also find a similar heatmap for the countywide total number of cases
in the file "HeatmapCounty.py".

if you wish to run the following heatmaps in your local computer please follow
the following set of instructions:

# Install Following Dependencies:
Pandas: https://pandas.pydata.org/
Plotly: https://pypi.org/project/plotly/
Dash: https://dash.plotly.com/installation
Dash bootstap commonents: https://dash-bootstrap-components.opensource.faculty.ai/

to run simply clone repo with: https://github.com/ranovoxo/CapCovidMap.git
Then for running Heatmap.py use:
python3 Heatmap
wait for the prompt that gives: Dash is running on http://127.0.0.1:8050/

wait for the table to load then ctrl+click the above url in your terminal.
If load initaly gives you an error saying unable to connect wait a moment then reload.
To run HeatmapCounty.py repete above steps but give 10 - 20 mins to load initaly.

# Refrences:
Credit to the New York Times for the csv files used. These files can be found in their git repo at:

https://github.com/nytimes/covid-19-data.git
