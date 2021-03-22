import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import altair as alt
from vega_datasets import data


df = pd.read_csv("data/processed/bank.csv", sep = ',')
#df_corr = pd.read_csv("data/processed/bank_corr.csv", sep = ',')
df_g = pd.read_csv("data/processed/bank_group.csv", sep = ',')
df_c = pd.read_csv("data/processed/bank_categorical.csv", sep = ',')
df_n = pd.read_csv("data/processed/bank_numeric.csv", sep = ',')


# Plot 1




app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    
    html.H2('Portuguese Banking Institution Term Deposit Subscription Dashboard'),
    
    # Dropdown Menu Section
    dbc.Row([
                
        # Numerical Dropdown Menu  
        dbc.Col([
            html.Label([
                'Numerical Data',
                dcc.Dropdown(
                    id = 'numeric-widget', 
                    value = 'Age',  
                    options = [{'label': col, 'value': col} for col in df_n.columns], 
                    style={'width': '440px', 'fontsize': 5, 'marginTop':10})])], md=4, style={'marginTop':20}),

        # Categorical Dropdown Menu 
        dbc.Col([
            html.Label([
                'Categorical Data',
                dcc.Dropdown(
                    id = 'categorical-widget', 
                    value = 'Type of Job',  
                    options = [{'label': col, 'value': col} for col in df_c.columns], 
                    style={'width': '440px', 'fontsize': 5, 'marginTop':10})])], md=4, style={'marginTop':20}),
        
        # Data Distribution Drop Down Menu
        dbc.Col([
            html.Label([
                'Data Distribution Menu',
                dcc.Dropdown(
                    id = 'xcol-widget', 
                    value = 'Age Group',  
                    options = [{'label': col, 'value': col} for col in df_g.columns], 
                    style={'width': '440px', 'fontsize': 5, 'marginTop':10})])], md=4, style={'marginTop':20})
        
        
    ]), # end of Menu & Text Section
    
    
    
    
    # Plots Section
    dbc.Row([
        dbc.Tabs([
                
            # Plot 1 - 3 Data Distribution 
            
                
                
            # Plot 4 - 5 Prediction Analysis
            dbc.Tab([
                
                #New Row for prediction RadioItem 
    
                dbc.Row([
                    dbc.Col([
                    html.Label(['Predicted Subscription for Current Campaign',
                                dcc.RadioItems(
                                    id='ycol',
                                    options=[
                                        {'label': 'Yes', 'value': 'yes'},
                                        {'label': 'No', 'value': 'no'}],
                                    value='yes',
                                    inputStyle={"margin-left": "80px"},
                                    style={"padding": "10px", "max-width": "800px", "margin-left": "-80px"},)])], md=4, style={'marginTop':20})
    ]),
                html.Br(),
                html.Br(),
                #Row for plots
                dbc.Row([
                
                
                    html.Br(),
                    html.Iframe(id = "boxplot", style = {'border-width': '0', 'width': '700px', 'height': '700px','marginLeft':30}),
                    html.Iframe(id = "lineplot", style = {'border-width': '0', 'width': '700px', 'height': '700px'})
                ])
            
            
            ], label='Subscription Prediction Analysis')
                
            ],style={'marginTop':30}) # end of Tabs
             
    ]), # end of Plot Section
    html.Br(),
    html.Br()
    
    
    
], style={'max-width': '90%', 'marginTop': 30})





#plot5
@app.callback(
    Output('boxplot','srcDoc'),
    Input('numeric-widget','value'),
    Input('ycol', 'value')
)


def plot_boxplot(xcol_q,ycol):
    alt.data_transformers.disable_max_rows()
    chart = alt.Chart(df[(df["Predicted Subscription (current)"] == ycol)]).mark_bar().encode(
        x = xcol_q,
        y = "count()")
    return chart.to_html()



if __name__ == '__main__':
    app.run_server(debug=True)


