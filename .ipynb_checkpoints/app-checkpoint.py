import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import pandas as pd
import numpy as np

#Data processing
data = pd.read_csv("bank-full.csv", sep = ';')
group = []
for i in (1,2,3,4,6,7,8,10,15,16):
    lst = pd.Series(pd.unique(data.iloc[:,i].values.ravel()))
    group.append(lst)
table = pd.concat(group, ignore_index=True, axis=1)
table = table.replace(np.nan, '', regex=True)
table.index = np.arange(1,len(table)+1)
table.columns = ['Job', 'Marriage', 'Education', 'Default', 'H.Loan', 'P.Loan', 
              'Contact', 'Last Contact','Previous Outcome', 'Predicted Subscription']
df = pd.read_csv("bank-full.csv", sep = ';')
df['housing'] = df['housing'].str.replace('yes','H')
df['housing'] = df['housing'].str.replace('no','-')
df['loan'] = df['loan'].str.replace('yes','P')
df['loan'] = df['loan'].str.replace('no','-')
df['Loan'] = df['housing'].astype(str) + df['loan']
df = df[(df.poutcome == 'success') | (df.poutcome == 'failure')]
df = df.drop(['housing', 'loan', 'contact', 'day', 'month'], axis=1)
df.columns = ['Age', 'Job', 'Marital', 'Education', 'Default', 'Balance(annual)', 
              'Last_Contact(sec)','#Contact', 'Days_Between', '#Contact_P', 'Last_Outcome','Predict', 'Loan']
df = df[['Age', 'Job', 'Marital', 'Education', 'Default', 'Balance(annual)', 'Loan',
         'Last_Contact(sec)','#Contact','#Contact_P','Days_Between',  'Last_Outcome','Predict']]
df = df.reset_index(drop=True)
df.index = np.arange(1,len(df)+1)

#Making Charts
categorical_data = ["Job","Marital","Education","Default","Loan","Last_Outcome"]
numerical_data = ["Age","Balance(annual)","Last_Contact(sec)","#Contact","#Contact_P","Days_Between"]

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])


app.layout = html.Div([
        html.Iframe(
            id = "barplot",
            #srcDoc=plot_barchart(xcol = "Job",ycol= "yes"),
                   style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        html.Iframe(
            id = "boxplot",
            #srcDoc=plot_boxplot(xcol_q = "Age",ycol= "yes"),
                   style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        dcc.Dropdown(
            id='xcol', value='Job',
            options=[{'label': i, 'value': i} for i in categorical_data]),
        dcc.Dropdown(
            id='xcol_q', value='Age',
            options=[{'label': j, 'value': j} for j in numerical_data]),
        dcc.Dropdown(
            id='ycol',value='yes',
            options=[{'label': col, 'value': col} for col in df["Predict"].unique()])
])



#call back
@app.callback(
    Output('barplot', 'srcDoc'),
    Input('xcol', 'value'),
    Input('ycol', 'value')
    )
#def update_output(xcol,ycol):
#    return plot_barchart(xcol,ycol)
def plot_barchart(xcol,ycol):
    alt.data_transformers.disable_max_rows()
    chart = alt.Chart(df[(df["Predict"] == ycol)]).mark_bar().encode(
    alt.X('count(Job)',title = xcol), 
    y= "Predict",
    color=xcol
    )
    return chart.to_html()

@app.callback(
    Output('boxplot','srcDoc'),
    Input('xcol_q','value'),
    Input('ycol', 'value')
)

#def update_output(xcol,ycol):
#    return plot_boxplot(xcol,ycol)
def plot_boxplot(xcol_q,ycol):
    alt.data_transformers.disable_max_rows()
    chart = alt.Chart(df[(df["Predict"] == ycol)]).mark_boxplot().encode(
        x = xcol_q,
        y = "Predict")
    return chart.to_html()

if __name__ == "__main__":
    app.run_server(debug=True)
