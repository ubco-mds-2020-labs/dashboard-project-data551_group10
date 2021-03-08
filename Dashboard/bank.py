import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import altair as alt


df = pd.read_csv("bank.csv", sep = ',')
df1 = pd.read_csv("bank_wrangle.csv", sep = ',')

def corr_plot():
    cor_data = (df.corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'}))
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format) 
    base = alt.Chart(cor_data).encode( 
        x = alt.X('variable2:O', axis=alt.Axis(title = '')),
        y = alt.Y('variable:O', axis=alt.Axis(title = '')))
    text = base.mark_text().encode(text='correlation_label', color=alt.condition( alt.datum.correlation > 0.5, alt.value('white'),alt.value('black')))
    cor_plot = base.mark_rect().encode(color='correlation:Q')
    chart_2 = (cor_plot + text).properties(width = 180, height = 180)
    return chart_2.to_html()

def pre_plot():
    a = alt.Chart(df).mark_boxplot().encode(x = "Age", y = "Predict", color = "Predict")
    return a.to_html()

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    
    html.H2('Portuguese Banking Institution Term Deposit Subscription Dashboard'),
    
    dbc.Row([
    
    # Dropdown Menu Section
    dbc.Col([
        
        # Data Prediction Dropdown Menu  
        dbc.Row([
                 html.P('Data Prediction Drop Down Menu', style={'margin-left': 'auto', 'margin-right': 'auto', 'marginTop':10})
        ], style={'border': '1px solid #d3d3d3', 'border-radius': '10px', 'width': '480px','height': '300px',  'marginTop':20}),  # end of Col_1_Row_1 - Menu 1
        
        # Data Distribution Drop Down Menu
        dbc.Row([
                dcc.Dropdown(
                    id = 'xcol-widget',
                    value = 'Age Group',  
                    options = [{'label': col, 'value': col} for col in df1.columns], 
                    style={'width': '440px', 'fontsize': 5, 'margin-left': 'auto', 'margin-right': 'auto', 'marginTop':10})
        ],style={'border': '1px solid #d3d3d3', 'border-radius': '10px', 'width': '480px','height': '300px', 'marginTop':20}) # end of Col_1_Row_2 - Menu 2
        
    ]), # end of Col_1 - Menu & Text Section
    
    
    # Plots Section
    dbc.Col([
        
        # Data Prediction Plot
        dbc.Row([
            html.Iframe(srcDoc = pre_plot(), style = {'border-width': '0', 'width': '550px', 'height': '300px', 'marginTop':20})

        ]), # end of Col_2_Row_1 - Prediction Plot
        
        # Data Distribution Plot & Heatmap
        dbc.Row([
            dbc.Tabs([
                dbc.Tab([html.Br(),
                         # Data Distribution Plot
                         dbc.Col([
                             html.Iframe(id = 'distribution', style = {'border-width': '0', 'width': '550px', 'height': '300px'})
                                 ]) # end of Col_2_Row_2_Col_1 - Data Distribution Plot 
                        ], label='Data Distribution Plots'),
                dbc.Tab([html.Br(),
                         # Heatmap
                         dbc.Col([
                             html.Iframe(srcDoc = corr_plot(), style = {'border-width': '0', 'width': '550px', 'height': '300px'})
                                 ])  # end of Col_2_Row_2_Col_2 - Heatmap
                        ], label='Correlation Heatmap for Numeric Variables')
                
            ],style={'marginTop':20}) # end of Tabs
            
            
        ]) # end of Col_2_Row_2 - Data Distribution Plot & Heatmap
         
    ]) # end of Col_2 - Plot Section
    

,html.Br()])], style={'max-width': '90%', 'marginTop':20})


@app.callback(
    Output('distribution', 'srcDoc'),
    Input('xcol-widget', 'value'))

def bank_data(xcol):
    click = alt.selection_multi()
    distribution = alt.Chart(df1).mark_bar().encode(
        y=alt.Y(xcol+':N', sort='-x'), 
        x='count()', 
        color=alt.Color(xcol, legend=None), 
        tooltip='count()',
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))).add_selection(click).properties(width = 400, height = 180)
    return distribution.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)

