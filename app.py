# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import datetime

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

# casosbrstates = pd.read_csv("cases-brazil-states.csv")

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
df = pd.read_csv(
    'https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
# date,country,state,city,newDeaths,deaths,newCases,totalCases,deathsMS,totalCasesMS,deaths_per_100k_inhabitants,totalCases_per_100k_inhabitants,deaths_by_totalCases,recovered

# df=df.drop(df[df.date=='2020-04-29'].index)

states = df.state.unique()
statesClean = []
for s in states:
    if s != 'TOTAL':
        statesClean.append(s)

# df.drop


# def getCasesRate(cases,column):
#    casesRate = df.dataFrame()
#    for i in range(0,cases[column].shape[0]-2):
#        casesRate.loc[df.index[i+2],'SMA_3'] = np.round(((cases[column].iloc[i,1]+ cases[column].iloc[i+1,1] +cases[column].iloc[i+2,1])/3),1)
#    return casesRate

# casosBahia=df.query("state=='BA'")
# taxaNCbahia=(casosBahia.newCases/casosBahia.totalCases)*100
# dfTaxaNCBahia=pd.DataFrame({'date':  casosBahia.date,
#        'taxaNovosCasos': taxaNCbahia})
# dfTaxaNCBahia.date=pd.to_datetime(dfTaxaNCBahia.date,format='%Y-%m-%d')

df["rateNewDeaths"] = (df.newDeaths/df.deaths)*100
df["rateNewCases"] = (df.newCases/df.totalCases)*100

today = datetime.datetime.now()
umMesAtras = datetime.datetime(today.year, today.month-1, today.day)

app.layout = html.Div(className='container', children=[
    html.H1('Monitoramento de COVID19', className='text-center'),
    html.Div(className='container', children=[
        html.H2('Casos na Bahia', className='text-center'),
        html.Div(className='row', children=[
            html.Div(className='col-sm', children=[
                dcc.Graph(
                    id='casosBahia',
                    figure={
                        'data': [
                            dict(
                                x=df[df['state'] == 'BA']['date'],
                                y=df[df['state'] == 'BA']['totalCases'],
                                name='BA'
                            )
                        ],
                        'layout': dict(
                            xaxis={'type': 'line', 'title': 'data'},
                            yaxis={
                                'title': 'casos',
                                'range': [0, df.query("state=='BA'")['totalCases'].max()],
                            },
                            title='Total de Casos na Bahia',
                            # hovermode='closest'
                        )
                    }
                )
            ]),
            html.Div(className='col-sm', children=[
                dcc.Graph(
                    id='taxaNovosCasosBahia',
                    figure={
                        'data': [
                            dict(
                                x=df[df['state'] == 'BA']['date'],
                                # newCases is collumn 6

                                y=df[df['state'] == 'BA']['rateNewCases'],
                                name='Taxa de Novos Casos',
                                type='bar'
                            ),
                            dict(
                                x=df[df['state'] == 'BA']['date'],
                                # newCases is collumn 6

                                y=df[df['state'] == 'BA']['rateNewCases'].rolling(
                                    window=5).mean(),
                                name='Média Movel de 5 Dias',
                                type='line'
                            )
                        ],
                        'layout': dict(
                            xaxis={'type': 'line', 'title': 'data',
                                   'range': [umMesAtras, today]},
                            yaxis={
                                'title': 'taxa (%)',
                                # 'range':[0,df.query("state=='BA'")['rateNewDeaths'].tail(31).max()]
                                'range': [0, 50]
                            },
                            title='Taxa de Crescimento de Novos Casos na Bahia',
                            legend={'x': 1, 'xanchor': 'right', 'y': 1},
                            # hovermode='closest'
                        )
                    }
                )
            ])
        ]),
        html.Div(className='row', children=[
            html.Div(className='col-sm', children=[
                dcc.Graph(
                    id='mortesBahia',
                    figure={
                        'data': [
                            dict(
                                x=df[df['state'] == 'BA']['date'],
                                y=df[df['state'] == 'BA']['deaths'],
                                name='BA'
                            )
                        ],
                        'layout': dict(
                            xaxis={
                                'type': 'line',
                                'title': 'data',
                                # 'range':[umMesAtras,today]
                            },
                            yaxis={
                                'title': 'casos',
                                'range': [0, df.query("state=='BA'")['deaths'].max()],
                            },
                            title='Total de Mortes na Bahia',

                            # hovermode='closest'
                        )
                    }
                )
            ]),
            html.Div(className='col-sm', children=[
                dcc.Graph(
                    id='taxaNovasMortesBahia',
                    figure={
                        'data': [
                            dict(
                                x=df[df['state'] == 'BA']['date'],
                                # newCases is collumn 6

                                y=df[df['state'] == 'BA']['rateNewDeaths'],
                                name='Taxa de Novas Mortes',
                                type='bar'
                            ),
                            dict(
                                x=df[df['state'] == 'BA']['date'],
                                # newCases is collumn 6

                                y=df[df['state'] == 'BA']['rateNewDeaths'].rolling(
                                    window=5).mean(),
                                name='Média Movel de 5 Dias',
                                type='line'
                            )
                        ],
                        'layout': dict(
                            xaxis={
                                'type': 'line',
                                'title': 'data',
                                'range': [umMesAtras, today]
                            },
                            yaxis={
                                'title': 'taxa (%)',
                                # 'range':[0,df.query("state=='BA'")['rateNewDeaths'].tail(31).max()]
                                'range': [0, 50]
                            },
                            title='Taxa de Crescimento de Novas Mortes na Bahia',
                            legend={'x': 1, 'xanchor': 'right', 'y': 1},
                            # hovermode='closest'
                        )
                    }
                )
            ])
        ]),
    ]),
    html.Div(className='container', children=[
        html.H2('Comparação Entre Estados do Brasil', className='text-center'),
        html.Div(className='row', children=[
            html.Div(className='col-sm', children=[
                dcc.Graph(
                    id='rateNewCasesStates',
                    figure={
                        'data': [
                            dict(
                                # x=df[df['continent'] == i]['gdp per capita'],
                                x=df[df['state'] == i]['date'],
                                y=df[df['state'] == i]['rateNewCases'].rolling(
                                    window=5).mean(),
                                # text=df[df['state'] == i]['state'],
                                # mode='markers',
                                # opacity=0.7,
                                # marker={
                                #    'size': 15,
                                #    'line': {'width': 0.5, 'color': 'white'}
                                # },
                                name=i
                            ) for i in statesClean
                        ],
                        'layout': dict(
                            xaxis={
                                'type': 'line',
                                'title': 'data',
                                'range': [umMesAtras, today]
                            },
                            yaxis={
                                'title': 'taxa (%)',
                                'range': [0, 50]
                            },
                            title='Média Móvel de 5 dias da Taxa de Novos Casos por Dia',
                            # margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                            # legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    }
                )
            ]),
            html.Div(className='col-sm', children=[
                dcc.Graph(
                    id='rateNewDeathsStates',
                    figure={
                        'data': [
                            dict(
                                # x=df[df['continent'] == i]['gdp per capita'],
                                x=df[df['state'] == i]['date'],
                                y=df[df['state'] == i]['rateNewDeaths'].rolling(
                                    window=5).mean(),
                                # text=df[df['state'] == i]['state'],
                                # mode='markers',
                                # opacity=0.7,
                                # marker={
                                #    'size': 15,
                                #    'line': {'width': 0.5, 'color': 'white'}
                                # },
                                name=i
                            ) for i in statesClean
                        ],
                        'layout': dict(
                            xaxis={
                                'type': 'line',
                                'title': 'data',
                                'range': [umMesAtras, today]
                            },
                            yaxis={
                                'title': 'taxa (%)',
                                'range': [0, 50]
                            },
                            # margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                            title='Média Móvel de 5 dias da Taxa de Novos Casos por Dia',
                            # legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    }
                ),
            ]),
        ]),
        html.Div(className='row', children=[
            html.Div(className='col-sm', children=[
                dcc.Graph(
                    id='deaths_per_100k_inhabitants',
                    figure={
                        'data': [
                            dict(
                                # x=df[df['continent'] == i]['gdp per capita'],
                                x=df[df['state'] == i]['date'],
                                y=df[df['state'] ==
                                     i]['deaths_per_100k_inhabitants'],
                                # text=df[df['state'] == i]['state'],
                                # mode='markers',
                                # opacity=0.7,
                                # marker={
                                #    'size': 15,
                                #    'line': {'width': 0.5, 'color': 'white'}
                                # },
                                name=i
                            ) for i in statesClean
                        ],
                        'layout': dict(
                            xaxis={
                                'type': 'line',
                                'title': 'data',
                                'range': [umMesAtras, today]
                            },
                            yaxis={'title': 'Mortes por 100k habitantes'},
                            # margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                            title='Mortes por 100k habitantes',
                            # legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    }
                )
            ])
        ])
    ])

])
# deaths_per_100k_inhabitants
if __name__ == '__main__':
    app.run_server(debug=True)
