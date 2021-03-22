import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import altair as alt
from vega_datasets import data
import plotly.express as px 


#####
##### Data 
#####
alt.data_transformers.disable_max_rows()
df = pd.read_csv("data/processed/bank.csv", sep = ',')
df_g = pd.read_csv("data/processed/bank_group.csv", sep = ',')
df_c = pd.read_csv("data/processed/bank_categorical.csv", sep = ',')
df_n = pd.read_csv("data/processed/bank_numeric.csv", sep = ',')





#####
##### Sidebar Setting
#####
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


CONTENT_STYLE = {
    "margin-left": "21rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}





#####
##### Sidebar Content
#####
sidebar = html.Div(
    [
        html.H1("Portuguese Bank Term Deposit Subscription Analysis", className="display-4",style={"fontSize": "40px", "color": "#02075D"}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Data Exploration", href="/", active="exact"),
                dbc.NavLink("Subsciption Analysis", href="/page-1", active="exact"),

            ],
            vertical=True,
            pills=True,
        ),
		html.Hr(),
        html.P("Design by Mona Jia, Zhiyan Ma ", className="lead")
        

    ],
    style=SIDEBAR_STYLE,
)






#####
##### Dashboard
#####

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])





#####
##### Web Pages
#####
@app.callback(
	Output("page-content", "children"), 
	[Input("url", "pathname")])
	
def render_page_content(pathname):

	###
	### Web Page 1 - Data Exploration
	###
    if pathname == "/":
        return dbc.Container([
            html.Br(),
        	html.Br(),
        	html.H2('Term Deposit Subscription Analysis Dashboard', style={'margin-left':'10px'}),
        	html.Br(),
        	
        	dbc.Tabs([
        		
        		###
			 	### Tab 1 - Distribution Bar 
			 	###
            	dbc.Tab([
                
    				dbc.Row([
                
        				# Bar Menu
        				dbc.Col([
                         	html.Br(),
                         	html.Br(),
           				 	html.Label([
              					   html.P('PLEASE SELECT AN ATTRIBUTE', style={'margin-left':'25px'}),
              					   dcc.Dropdown(
               				 		    id = 'xcol-widget', 
                			  	  		value = 'Age Group',  
                 			     		options = [{'label': col, 'value': col} for col in df_g.columns], 
                  			     		style={'width': '300px', 'fontsize': 5, 'marginTop':10, 'margin-left':'10px'}, clearable=False)]),
                  			 
                		 	html.Br(),                  	
                  		 	html.Br(),
        				 	html.P('* Ordered by count of records descending ', style={'margin-left':'10px'}),
							html.P('* Hover over the plot to see ', style={'margin-left':'10px'}),
							html.P('  count of each subgroup ', style={'margin-left':'22px'}),
							html.P('* Click on the bar to highlight groups', style={'margin-left':'10px'}),
							html.P("* Press 'shift' and click on bars  ", style={'margin-left':'10px'}),
							html.P('  to select more than one group', style={'margin-left':'22px'}),
        				 	html.Br()
                  	
                  	
                  		], style={'marginTop':20}),  # /Bar Menu
                  	
                  	
        
        
        				# Bar Plot
    					dbc.Col([
    			            html.Br(),
                    		html.Br(),
                    		html.Iframe(id = 'distribution', style = {'border-width': '0', 'width':'700px', 'height': '550px', 'position': 'absolute', 'right': '20px'})
                    
						]) # /Bar Plot
        
    				], style = {'width': '1150px', 'height': '550px'}), # /Row
            
            	], label='Data Distribution (Count)'), # /Tab1                  
                
                

                ###
            	### Tab 2 - Donut
            	###
            	dbc.Tab([
                
            		dbc.Row([
              
                		# Donut Menu
              			dbc.Col([
              		
                        	html.Br(),
                        	html.Br(),
    						html.Label([
        						 html.P('PLEASE SELECT AN ATTRIBUTE', style={'margin-left':'25px'}),
        						 dcc.Dropdown(
                			  			id = 'values', 
                			  			value = 'Type of Job',  
                			  			options = [{'label': col, 'value': col} for col in df_g.columns], 
                			  			style={'width': '300px', 'fontsize': 5, 'marginTop':10, 'margin-left':'10px'}, clearable=False)]),
                			
                			
                		 	html.Br(),                  	
                  		 	html.Br(),
        				 	html.P('* Hover over the plot to see the subgroup name ', style={'margin-left':'10px'}),
        				 	html.P('  and count of records', style={'margin-left':'22px'}),
							html.P('* Remove / Add a subgroup on the chart by ', style={'margin-left':'10px'}),
							html.P('  clicking it on the legend', style={'margin-left':'22px'}),
							html.P('* Double click on a subgroup name first and', style={'margin-left':'10px'}),
        				 	html.P('  then click other subgroups you wish to compare', style={'margin-left':'22px'}),
        				 	html.Br()	
                			
                			
                		], style={'marginTop':20}), # /Donut Menu
                
                
                
                		# Donut Plot
                		dbc.Col([
                			html.Br(),

                			dcc.Graph(id="pie-chart", style = {'width': '500px', 'height': '500px','position': 'absolute', 'right': '150px'})
                			
                		]), # /Donut Plot
              
              			
            		], style = {'width': '1150px', 'height': '550px'}) # /Row
                     
        		], label='Data Distribution (Ratio)'),  # /Tab2  
                
                
                

                
                ###
            	### Tab 3 - Line 
            	###
            	dbc.Tab([
            
            		dbc.Row([
            
            			# Line Menu
    					dbc.Col([
                
        					# Numerical Dropdown Menu  
        					dbc.Row([

            					html.Label([
            		        		 html.Br(),
                					 html.P('SELECT AN ATTRIBUTE FOR X AXIS',style={'margin-left':'35px'}),
                					 dcc.Dropdown(
                   			 				id = 'numeric-widget', 
                   			 				value = 'Age',  
                    						options = [{'label': col, 'value': col} for col in df_n.columns], 
                    						style={'width': '300px', 'fontsize': 5, 'marginTop':10,'left':'35px'})])], style={'marginTop':20}),


        					# Categorical Dropdown Menu 
        					dbc.Row([
        				    		 html.Br(),
           				 			 html.Label([
                					 html.P('SELECT AN ATTRIBUTE FOR Y AXIS',style={'margin-left':'35px'}),
                					 dcc.Dropdown(
                   					 		id = 'categorical-widget', 
                   					 		value = 'Education Level',  
                   					 		options = [{'label': col, 'value': col} for col in df_c.columns], 
                   					 		style={'width': '300px', 'fontsize': 5, 'marginTop':10,'left':'35px'})])], style={'marginTop':20}),
        
        
                        	
                  		 	html.Br(),
        				 	html.P('* Click and drag on the plot ', style={'margin-left':'15px'}),
							html.P('  to highligh area', style={'margin-left':'27px'}),
							html.P('* Click on the legend to highlight groups', style={'margin-left':'15px'}),
							html.P("* Press 'shift' and click on legends  ", style={'margin-left':'10px'}),
							html.P('  to select more than one group', style={'margin-left':'27px'}),
        				 	html.Br()
        
    						], style={'marginTop':20}), # /# Line Menus
            
            	
            	
						# Line Plot
    					dbc.Col([  
                    		html.Br(),
                    		html.Br(),
                    		html.Iframe(id = 'nc', style = {'border-width': '0', 'width': '700px', 'height': '550px','position': 'absolute', 'right': '20px'}),
                    	
						]) # /Line Plot
            
            
            		], style = {'width': '1150px', 'height': '550px'}) # /Row
            
            
            	], label='Correlation Distribution (density)'), # /Tab3
            
            

                ###
            	### Plot 4
            	###
            	dbc.Tab([
            
    				dbc.Row([
    			
    					# Box Menu
    					dbc.Col([
    				
      						# Numerical Dropdown Menu  
        					dbc.Row([

            					html.Label([
            		        		 html.Br(),
        							 html.Br(),
                					 html.P('SELECT AN ATTRIBUTE FOR X AXIS',style={'margin-left':'35px'}),
                					 dcc.Dropdown(
                   				 			id = 'numeric', 
                   							value = 'Age',  
                    						options = [{'label': col, 'value': col} for col in df_n.columns], 
                    						style={'width': '300px', 'fontsize': 5, 'marginTop':10, 'left':'35px'})])], style={'marginTop':20}),


        					# Categorical Dropdown Menu 
        					dbc.Row([
        				    		 html.Br(),
           				 			 html.Label([
                					 html.P('SELECT AN ATTRIBUTE FOR Y AXIS',style={'margin-left':'35px'}),
                					 dcc.Dropdown(
                   					 		id = 'categorical', 
                   					 		value = 'Type of Job',  
                   					 		options = [{'label': col, 'value': col} for col in df_c.columns], 
                   					 		style={'width': '300px', 'fontsize': 5, 'marginTop':10, 'left':'35px'})])], style={'marginTop':20}),
    				

                		 	html.Br(),                  	
        				 	html.P('* Hover over the plot to see statistical ', style={'margin-left':'15px'}),
        				 	html.P('  summary for each subgroup', style={'margin-left':'27px'}),

        				 	html.Br()	
    				
    				
    					], style={'marginTop':20}), # /Box Menu
    				
    				
    				
    					# Box Plot
    					dbc.Col([
    						html.Br(),
                    		html.Br(),
                    		html.Iframe(id = 'box', style = {'border-width': '0', 'width': '700px', 'height': '550px','position': 'absolute', 'right': '20px'}),
    				
    				
    					]) # /Box Plot
                
                	], style = {'width': '1150px', 'height': '550px'}) # /Row 
            
            	], label='Correlation Distribution (details)'), # /Tab4        	
        	
        	
        	
        	], style={'marginTop':30}) # /Tab1-4
        	
        ]) # /Page-1



	###
	### Web Page 2 - Subscription Analysis
	###
    elif pathname == "/page-1":
        return dbc.Container([
            html.Br(),
        	html.Br(),
        	html.H2('Term Deposit Subscription Analysis Dashboard'),
        	html.Br(),
        	
        	dbc.Tabs([
        	
        		###
        		### Tab 5
        		### 
            	dbc.Tab([
                
    				dbc.Row([
                        
                        #Left dropdown menu
                        dbc.Col([
                            
                            # Categorical Dropdown Menu 
        					dbc.Row([
        				    		 html.Br(),
           				 			 html.Label([
                					 html.P('SELECT AN ATTRIBUTE FOR X AXIS',style={'margin-left':'35px'}),
                					 dcc.Dropdown(
                   					 		id = 'categorical_prediction', 
                   					 		value = 'Type of Job',  
                   					 		options = [{'label': col, 'value': col} for col in df_c.columns], 
                   					 		style={'width': '300px', 'fontsize': 5, 'marginTop':10, 'left':'35px'})])], style={'marginTop':20}),
                            #Prediction radio item menu
                            dbc.Row([
        				    		 html.Br(),
           				 			 html.Label([
                					 html.P('SELECT AN ATTRIBUTE FOR Y AXIS',style={'margin-left':'35px'}),
                					 dcc.RadioItems(
                                         id='prediction',
                                         options=[
                                            {'label': 'Yes', 'value': 'yes'},
                                            {'label': 'No', 'value': 'no'}],
                                         value='yes',
                                         inputStyle={"margin-left": "80px"},
                                         style={'width': '300px', 'fontsize': 5, 'marginTop':10,"margin-left": "-45px"})
                                     
                                         ])], style={'marginTop':20}),
                            html.Br(),
        				 	html.P('* Use X axis to select categorical variables ', style={'margin-left':'15px'}),
							
							html.P('* Use Y axis to select subsription', style={'margin-left':'15px'}),
                            html.P('or non-subscription', style={'margin-left':'27px'}),
							html.P('* Compare between each categories  ', style={'margin-left':'15px'}),
							
        				 	html.Br()
                        
                        ],style={'marginTop':30}),
                        
                            
                        
                        #Plot 5 Bar plot
                        dbc.Col([
                            html.Br(),
                    		html.Br(),
                    		html.Iframe(id = 'barplot', style = {'border-width': '0', 'width': '750px', 'height': '1000px','position': 'absolute', 'right': '20px'})
                        ])
    			



                
                	
                	], style = {'width': '1150px', 'height': '550px'}) # /Row 

            
           		], label='Categorical Variable VS. Subscription (Count)'), # /Tab5                  
                
                
                
                
                
    
        		###
        		### Tab 6
        		### 
            	dbc.Tab([
                
    				dbc.Row([
                        
                        #Dropdown Menu
                        dbc.Col([
                            # Numerical Dropdown Menu  
        					dbc.Row([

            					html.Label([
            		        		 html.Br(),
        							 html.Br(),
                					 html.P('SELECT AN ATTRIBUTE FOR X AXIS',style={'margin-left':'35px'}),
                					 dcc.Dropdown(
                   				 			id = 'numeric_prediction', 
                   							value = 'Age',  
                    						options = [{'label': col, 'value': col} for col in df_n.columns], 
                    						style={'width': '300px', 'fontsize': 5, 'marginTop':10, 'left':'35px'})])], ),
                            dbc.Row([
        				    		 html.Br(),
           				 			 html.Label([
                					 html.P('SELECT AN ATTRIBUTE FOR Y AXIS',style={'margin-left':'35px'}),
                					 dcc.RadioItems(
                                         id='prediction_2',
                                         options=[
                                            {'label': 'Yes', 'value': 'yes'},
                                            {'label': 'No', 'value': 'no'}],
                                         value='yes',
                                         inputStyle={"margin-left": "80px"},
                                         style={'width': '300px', 'fontsize': 5, 'marginTop':10,"margin-left": "-45px"}),
                            html.Br(),
        				 	html.P('* Use X axis to select numerical variables ', style={'margin-left':'25px'}),
							
							html.P('* Use Y axis to select subsription', style={'margin-left':'25px'}),
                            html.P('or non-subscription', style={'margin-left':'37px'}),
							html.P('* Check the trend of the graph', style={'margin-left':'25px'}),
							
        				 	html.Br()
                                         
                                     
                                         ])], style={'marginTop':20}),
                            
                        ]),
                        
                        #Plot 5 Distribution Plot
                        dbc.Col([
                            html.Br(),
                    		html.Br(),
                    		html.Iframe(id = 'distributionplot', style = {'border-width': '0', 'width': '750px', 'height': '1000px','position': 'absolute', 'right': '20px'})
                        ])
                        
    			



                
                	
                	], style = {'width': '1150px', 'height': '550px'}) # /Row 

            
            	], label='Numerical Variable VS. Subscription (Distribution)'), # /Tab6      
                
        	
        	], style={'marginTop':30}) # /Tab5-6
        	
        ]) # /Page-2





	###
	### Page Error Handling
    ###
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )





#####
##### Plot 1 - Bar
#####
@app.callback(
    Output('distribution', 'srcDoc'),
    Input('xcol-widget', 'value'))
def bank_data(xcol):
    click = alt.selection_multi()
    distribution = alt.Chart(df_g).mark_bar().encode(
        y = alt.Y(xcol+':N', sort='-x'), 
        x = 'count()', 
        color = alt.Color(xcol, legend=None, scale=alt.Scale(scheme='blueorange')), 
        tooltip = 'count()',
        opacity = alt.condition(click, alt.value(0.9), alt.value(0.2))).add_selection(click).properties(width = 400, height = 400).configure_axis(
    labelFontSize=20,
    titleFontSize=25)
    return distribution.to_html()
    
    

    
    
#####
##### Plot 2 - Donut
#####
@app.callback(
    Output("pie-chart", "figure"),  
     Input("values", "value"))

def generate_chart(valu):
    data1 = df_g.groupby(valu)[valu].count().reset_index(name='counts')
    fig = px.pie(data1, values='counts', names=valu, color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(hole=.6, hoverinfo="label+percent+name")
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig





#####
##### Plot 3 - Line
#####
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
            color = alt.Color(categorical + ":N", scale=alt.Scale(scheme='blueorange')),
            opacity = alt.condition(click, alt.value(0.9), alt.value(0.2))
    ).add_selection(brush).add_selection(click).properties(width = 400, height = 400).configure_axis(
    labelFontSize=20,
    titleFontSize=25)
    
    return chart.to_html()





#####
##### Plot 4 - Box
#####
@app.callback(
    Output('box', 'srcDoc'),
    Input('numeric', 'value'),
    Input('categorical', 'value'))

def nc_plot(numeric, categorical):
	chart = alt.Chart(df).mark_boxplot().encode(
    	x=categorical,
    	y=numeric,
    	color = alt.Color(categorical, scale=alt.Scale(scheme='blueorange'))
    	).properties(width = 400, height = 400).configure_axis(
    labelFontSize=20,
    titleFontSize=25)

	return chart.to_html()
	
	
	
	
	
#####
##### Plot 5 - Bar
#####

@app.callback(
    Output('barplot','srcDoc'),
    Input('categorical_prediction','value'),
    Input('prediction','value'))

def bar_plot(xcol,ycol):
    alt.data_transformers.disable_max_rows()
    click = alt.selection_multi()
    chart = alt.Chart(df[(df["Predicted Subscription (current)"] == ycol)]).mark_bar().encode(
    alt.X(xcol,title = xcol), 
    y= "count(Type of Job)",
    color = alt.Color(xcol, legend=None)
    ).properties(width=alt.Step(50)).configure_axis(
    labelFontSize=20,
    titleFontSize=25)
    return chart.to_html()








#####
##### Plot 6 - Distribution
#####

@app.callback(
    Output('distributionplot','srcDoc'),
    Input('numeric_prediction','value'),
    Input('prediction_2','value'))

def distribution_plot(xcol,ycol):
    alt.data_transformers.disable_max_rows()
    chart = alt.Chart(df[(df["Predicted Subscription (current)"] == ycol)]).mark_bar().encode(
    alt.X(xcol,title = xcol), 
    y= "count()"
    ).configure_axis(
    labelFontSize=20,
    titleFontSize=25)
    return chart.to_html()






if __name__ == "__main__":
    app.run_server()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
