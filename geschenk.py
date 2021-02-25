import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go



# load dataframe from pickle file (saves by "df.to_pickle('SOME_PATH')")
df = pd.read_pickle('frame_rec_analysis_site_id_28_app_Geschenkefinder_2020-08-15_2020-11-24.pkl')





# collect the set of questions from the given profile-strings
questions = set()

for prof_str in df.profile_str.unique():
    questions.update([quest_option.split('~')[0] for quest_option in prof_str.split()])




# extract the selected option(s) for a given question (from the profile)
def extract(prof_str, question):
    selctions = [q_a.split('~')[1] for q_a in prof_str.split() if q_a.startswith(question)]
    
    if len(selctions) > 0:
        return ' '.join(sorted(selctions))
    else:
        return None





for q in questions:
    # create new empty column for current question
    df['Q_'+q] = df.profile_str.apply(extract, args=(q,))





data= df.drop(columns='profile_str')




data.clicked =data.clicked.astype(int)





# Extract the month from the datetime and insert it into a new column called Monat
data['Monat']= data.timestamp.dt.month





new_data=data.copy()





external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
        html.Div(children='''
        Proportion of the clicked data
    ''', style={
        'textAlign': 'center',
        'font-weight': 'bold'
    }),
    
    html.Div([dcc.Graph(id='graph-with-slider')]),
    html.Div([html.Label(['Please choose a month']
                    )]),
    dcc.RangeSlider(
        id='year-slider',
        min=new_data['Monat'].min(),
        max=new_data['Monat'].max(),
        value=[8,9],
        #marks={str(Month): str(Month) for Month in new_data['Monat'].unique()},
        marks= {
            8: {'label': 'August', 'style': {'color': '#f50'}},
            9:{'label': 'September', 'style': {'color': '#f50'}},
            10:{'label': 'October', 'style': {'color': '#f50'}},
            11:{'label': 'November', 'style': {'color': '#f50'}}
        },
        step=1,
        
        updatemode='drag'

    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_month):
    
    filtered_df=new_data[(new_data['Monat']>=selected_month[0])&(new_data['Monat']<=selected_month[1])]

    fig = px.pie(filtered_df, names="clicked", hole=.3,color_discrete_sequence=px.colors.sequential.Rainbow)
    #fig.add_trace(go.Pie( filtered_df,name='clicked',
                     #marker_colors=irises_colors))
    #fig = go.Figure(fig)

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(port=8060)

















