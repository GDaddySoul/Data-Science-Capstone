# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites = [{'label': 'All Sites', 'value': 'ALL'}]
for site in pd.unique(spacex_df['Launch Site']):
    sdict = {}
    sdict['label'] = site
    sdict['value'] = site
    sites.append(sdict)

pie_data = spacex_df[['Launch Site', 'class']].groupby(['Launch Site']).sum()
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                options= sites,
                               
                                value='ALL',
                                placeholder="Select Launch Site",
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),

                                #px.pie(pie_data, values='class', title="{} : Successful Launches by Site {}".format(input_region,input_year))
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                    1000: '1000', 2000:'2000', 3000:'3000', 4000: '4000', 5000:'5000', 6000:'6000', 7000:'7000', 8000:'8000', 9000:'9000', 10000:'MAX'},
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df[['Launch Site', 'class']].groupby(['Launch Site']).sum()
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names=['CCAFS LC-40','VAFB SLC-4E','KSC LC-39A','CCAFS SLC-40'], 
        title='Success by Launch Site')
        return fig
    else:
        site_data = spacex_df [spacex_df['Launch Site'] == entered_site]
        site_data['Launches'] = 1
        site_data = site_data[['Launch Site', 'class','Launches']]
        site_data = site_data.groupby(['Launch Site', 'class']).sum()
        fig = px.pie(site_data, values='Launches', 
        names=['Failed','Success'], 
        title='Launch Site Details')
        return fig       

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), 
            Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, min_payload):
    
    if entered_site == 'ALL':
        launch_data = spacex_df [spacex_df['Payload Mass (kg)'] >= min_payload[0]]
        launch_data = launch_data [launch_data['Payload Mass (kg)'] <= min_payload[1]]
        fig1 = px.scatter(launch_data, y='Payload Mass (kg)' ,x='class', 
        color = "Booster Version Category", 
        title='Success by Payload Mass')
        return fig1
    else:
        launch_data = spacex_df [spacex_df['Launch Site'] == entered_site]
        launch_data = launch_data [launch_data['Payload Mass (kg)'] >= min_payload[0]]
        launch_data = launch_data [launch_data['Payload Mass (kg)'] <= min_payload[1]]
        fig1 = px.scatter(launch_data, y='Payload Mass (kg)' ,x='class', 
        color = "Booster Version Category", 
        title='Success by Payload Mass')
        return fig1       


# Run the app
if __name__ == '__main__':
    app.run_server()

