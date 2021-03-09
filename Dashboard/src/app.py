#sys.path.insert(0, '../src')
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import altair as alt


df = pd.read_csv("./data/bank.csv", sep = ',')
df_corr = pd.read_csv("./data/bank_corr.csv", sep = ',')
df_g = pd.read_csv("./data/bank_group.csv", sep = ',')
df_c = pd.read_csv("./data/bank_c.csv", sep = ',')
df_n = pd.read_csv("./data/bank_n.csv", sep = ',')


# Plot 1
def corr_plot():
    click = alt.selection_multi()
    cor_data = (df_corr.corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'}))
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format) 
    base = alt.Chart(cor_data).encode( 
        x = alt.X('variable2:O', axis=alt.Axis(title = '')),
        y = alt.Y('variable:O', axis=alt.Axis(title = '')))
    text = base.mark_text().encode(
        text='correlation_label', 
        color=alt.condition( alt.datum.correlation > 0.5, alt.value('white'),alt.value('black')))
    cor_plot = base.mark_rect().encode(color = alt.Color('correlation:Q', legend=None))
    chart_2 = (cor_plot + text).encode(
        opacity = alt.condition(click, 
                                alt.value(0.9), 
                                alt.value(0.2))
                                ).add_selection(click).properties(width = 250, height = 250)
    return chart_2.to_html()



# Plot 4
def pre_plot():
    a = alt.Chart(df).mark_boxplot().encode(
        x = "Age", 
        y = "Predicted Subscription for Current Campaign", 
        color = "Predicted Subscription for Current Campaign")
    return a.to_html()





app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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
            dbc.Tab([
                    html.Br(),
                    html.Iframe(srcDoc = corr_plot(), style = {'border-width': '0', 'width': '500px', 'height': '500px'}),
                    html.Iframe(id = 'nc', style = {'border-width': '0', 'width': '500px', 'height': '500px'}),
                    html.Iframe(id = 'distribution', style = {'border-width': '0', 'width': '450px', 'height': '500px'})
                
                ],label='Data Distribution Plots'), 
                
                
            # Plot 4 - ? Prediction Analysis
            dbc.Tab([
                    html.Br(),
                    html.Iframe(srcDoc = pre_plot(), style = {'border-width': '0', 'width': '700px', 'height': '700px', 'marginTop':20})
                ], label='Subscription Prediction Analysis')
                
            ],style={'marginTop':30}) # end of Tabs
             
    ]), # end of Plot Section
    html.Br(),
    html.Br()
    
    
    
], style={'max-width': '90%', 'marginTop': 30})



# Plot 2
@app.callback(
    Output('distribution', 'srcDoc'),
    Input('xcol-widget', 'value'))
def bank_data(xcol):
    click = alt.selection_multi()
    distribution = alt.Chart(df_g).mark_bar().encode(
        y = alt.Y(xcol+':N', sort='-x'), 
        x = 'count()', 
        color = alt.Color(xcol, legend=None), 
        tooltip = 'count()',
        opacity = alt.condition(click, alt.value(0.9), alt.value(0.2))).add_selection(click).properties(width = 250, height = 400)
    return distribution.to_html()


# Plot 3
@app.callback(
    Output('nc', 'srcDoc'),
    Input('numeric-widget', 'value'),
    Input('categorical-widget', 'value'))

def nc_plot(numeric, categorical):
    brush = alt.selection_interval()
    click = alt.selection_multi(fields=[categorical], bind='legend')

    chart = alt.Chart(df).mark_line().encode(
            alt.X(numeric + ':Q', bin=alt.Bin(maxbins=30)),
            y = 'count()',
            color = categorical + ":N",
            opacity = alt.condition(click, alt.value(0.9), alt.value(0.2))
    ).add_selection(brush).add_selection(click).properties(width = 250, height = 400)
    
    return chart.to_html()




if __name__ == '__main__':
    app.run_server(debug=True)


