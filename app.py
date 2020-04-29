# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#casosbrstates = pd.read_csv("cases-brazil-states.csv")

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
df = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')

#df=df.drop(df[df.date=='2020-04-29'].index)

states=df.state.unique()
statesClean=[]
for s in states:
    if s!='TOTAL':
        statesClean.append(s)

df.drop

app.layout = html.Div([
    dcc.Graph(
        id='newCases',
        figure={
            'data': [
                dict(
                    #x=df[df['continent'] == i]['gdp per capita'],
                    x=df[df['state'] == i]['date'],
                    y=df[df['state'] == i]['newCases'],
                    #text=df[df['state'] == i]['state'],
                    #mode='markers',
                    #opacity=0.7,
                    #marker={
                    #    'size': 15,
                    #    'line': {'width': 0.5, 'color': 'white'}
                    #},
                    name=i
                ) for i in statesClean
            ],
            'layout': dict(
                xaxis={'type': 'line', 'title': 'data'},
                yaxis={'title': 'casos'},
                title='Novos Casos por Dia', 
                #margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                #legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    dcc.Graph(
        id='newDeaths',
        figure={
            'data': [
                dict(
                    #x=df[df['continent'] == i]['gdp per capita'],
                    x=df[df['state'] == i]['date'],
                    y=df[df['state'] == i]['newDeaths'],
                    #text=df[df['state'] == i]['state'],
                    #mode='markers',
                    #opacity=0.7,
                    #marker={
                    #    'size': 15,
                    #    'line': {'width': 0.5, 'color': 'white'}
                    #},
                    name=i
                ) for i in statesClean
            ],
            'layout': dict(
                xaxis={'type': 'line', 'title': 'data'},
                yaxis={'title': 'mortes'},
                #margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                title='Novas de Mortes por Dia', 
                #legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    dcc.Graph(
        id='deaths_per_100k_inhabitants',
        figure={
            'data': [
                dict(
                    #x=df[df['continent'] == i]['gdp per capita'],
                    x=df[df['state'] == i]['date'],
                    y=df[df['state'] == i]['deaths_per_100k_inhabitants'],
                    #text=df[df['state'] == i]['state'],
                    #mode='markers',
                    #opacity=0.7,
                    #marker={
                    #    'size': 15,
                    #    'line': {'width': 0.5, 'color': 'white'}
                    #},
                    name=i
                ) for i in statesClean
            ],
            'layout': dict(
                xaxis={'type': 'line', 'title': 'data'},
                yaxis={'title': 'Mortes por 100k habitantes'},
                #margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                title='Mortes por 100k habitantes', 
                #legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])
#deaths_per_100k_inhabitants
if __name__ == '__main__':
    app.run_server(debug=True)