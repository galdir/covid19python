


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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
meta_tags=[
    # A description of the app, used by e.g.
    # search engines when displaying search results.
    {
        'name': 'description',
        'content': 'My description'
    },
    # A tag that tells Internet Explorer (IE)
    # to use the latest renderer version available
    # to that browser (e.g. Edge)
    {
        'http-equiv': 'X-UA-Compatible',
        'content': 'IE=edge'
    },
    # A tag that tells the browser not to scale
    # desktop widths to fit mobile screens.
    # Sets the width of the viewport (browser)
    # to the width of the device, and the zoom level
    # (initial scale) to 1.
    #
    # Necessary for "true" mobile support.
    {
      'name': 'viewport',
      'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
    },
]

)

app.title='Monitoramento COVID19 na Bahia'

server = app.server


# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
df = pd.read_csv(
    'https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
# date,country,state,city,newDeaths,deaths,newCases,totalCases,deathsMS,totalCasesMS,deaths_per_100k_inhabitants,totalCases_per_100k_inhabitants,deaths_by_totalCases,recovered

dfLeitosBahia = pd.read_csv(
    'leitos-exclusivos-covid-ba.csv')


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
                html.H3('Total de Casos na Bahia',className='text-center'),
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
                            #title='Total de Casos na Bahia',
                            margin={'l':40,'b':80,'r':40,'t': 40},
                            hovermode='closest'
                        )
                    }
                )
            ]),
            html.Div(className='col-sm', children=[
                html.H3('Taxa de Crescimento de Novos Casos na Bahia',className='text-center'),
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
                            #title='Taxa de Crescimento de Novos Casos na Bahia',
                            legend={'x': 1, 'xanchor': 'right', 'y': 1},
                            margin={'l':40,'b':80,'r':40,'t': 40},
                            hovermode='closest'
                        )
                    }
                )
            ])
        ]),
        html.Div(className='row', children=[
            html.Div(className='col-sm', children=[
                html.H3('Total de Mortes na Bahia',className='text-center'),
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
                            #title='Total de Mortes na Bahia',
                            margin={'l':40,'b':80,'r':40,'t': 40},

                            hovermode='closest'
                        )
                    }
                )
            ]),
            html.Div(className='col-sm', children=[
                html.H3('Taxa de Crescimento de Novas Mortes na Bahia',className='text-center'),
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
                            #title='Taxa de Crescimento de Novas Mortes na Bahia',
                            #legend={'x': 1, 'xanchor': 'center', 'yanchor':'top', 'y': 0.5},
                            legend={'x': 1, 'xanchor': 'right', 'y': 1},
                            margin={'l':40,'b':80,'r':40,'t': 40},
                            hovermode='closest'
                        )
                    }
                )
            ])
        ]),
        html.Div(className='row', children=[
            html.Div(className='col-sm', children=[
                html.H3('UTIs exclusivas para COVID19 na Bahia',
                        className='text-center'),
                html.P(
                    '''
                    Esses números são divulgados quase que diariamente pela Secretaria de Saúde da Bahia (SESAB) por seus boletins. 
                    Quando o número não foi divulgado, o número anterior foi repetido aqui. 
                    Segundo a SESAB o número de leitos é flutuante, representando o quantitativo exato de vagas disponíveis no dia. Intercorrências com equipamentos, rede de gases ou equipes incompletas, por exemplo, inviabilizam a disponibilidade do leito.
                '''
                ),
                
                dcc.Graph(
                    id='leitosUTIBahia',
                    figure={
                        'data': [
                            dict(
                                x=dfLeitosBahia['data'],
                                y=dfLeitosBahia['uti ocupadas'],
                                name='UTIs ocupadas'
                            ),
                            dict(
                                x=dfLeitosBahia['data'],
                                y=dfLeitosBahia['utis totais'],
                                name='UTIs totais'
                            )
                        ],
                        'layout': dict(
                            xaxis={
                                'type': 'line',
                                'title': 'data',
                                # 'range':[umMesAtras,today]
                            },
                            yaxis={
                                'title': 'UTIs',
                                # 'range': [0, df.query("state=='BA'")['deaths'].max()],
                            },
                            #margin={'t': 20},
                            #legend={'x': 0, 'y': 1},
                            legend={'x': 0.5, 'xanchor': 'center', 'yanchor':'center','y': 0.5},
                            margin={'l':40,'b':80,'r':40,'t': 40},
                            #title='UTIs exclusivas para COVID19 na Bahia',

                            hovermode='closest'
                        )
                    }
                )
            ]),

        ]),



    ]),



    html.Div(className='container', children=[
        html.H2('Comparação Entre Estados do Brasil', className='text-center'),
        html.Div(className='row', children=[
            html.Div(className='col-sm', children=[
                html.H3('Média dos últimos 5 dias da Taxa de Novos Casos por Dia',className='text-center'),
                dcc.Graph(
                    id='rateNewCasesStates',
                    figure={
                        'data': [
                            dict(
                                x=statesClean,
                                y=[
                                    (
                                        df[df['state'] == i]['rateNewCases'].rolling(
                                            window=5).mean().tail(1).tolist()[0]
                                    ) for i in statesClean
                                ],
                                type='bar',
                                name='taxa dos estados'
                            )

                            # dict(
                            # x=df[df['continent'] == i]['gdp per capita'],
                            #x=df[df['state'] == i]['date'],
                            # y=df[df['state'] == i]['rateNewCases'].rolling(
                            #    window=5).mean(),
                            # text=df[df['state'] == i]['state'],
                            # mode='markers',
                            # opacity=0.7,
                            # marker={
                            #    'size': 15,
                            #    'line': {'width': 0.5, 'color': 'white'}
                            # },
                            # name=i
                            # ) for i in statesClean
                        ],
                        'layout': dict(
                            xaxis={
                                'type': 'bar',
                                'title': 'Estado',
                                # 'range': [umMesAtras, today]
                            },
                            yaxis={
                                'title': 'taxa (%)',
                                #'range': [0, 50]
                            },
                            #title='Média dos Últimos 5 dias da Taxa de Novos Casos por Dia',
                            # margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                            # legend={'x': 0, 'y': 1},
                            hovermode='closest',
                            margin={'l':40,'b':80,'r':40,'t': 40},
                        )
                    }
                )
            ]),
            html.Div(className='col-sm', children=[
                html.H3('Média dos últimos 5 dias da Taxa de Novas Mortes por Dia',className='text-center'),
                dcc.Graph(
                    id='rateNewDeathsStates',
                    figure={
                        'data': [
                            dict(
                                # x=df[df['continent'] == i]['gdp per capita'],
                                x=statesClean,
                                y=[
                                    (
                                        df[df['state'] == i]['rateNewDeaths'].rolling(
                                            window=5).mean().tail(1).tolist()[0]
                                    ) for i in statesClean
                                ],
                                type='bar',
                                name='taxa dos estados',
                                
                                # text=df[df['state'] == i]['state'],
                                # mode='markers',
                                # opacity=0.7,
                                # marker={
                                #    'size': 15,
                                #    'line': {'width': 0.5, 'color': 'white'}
                                # },
                            )
                        ],
                        'layout': dict(
                            xaxis={
                                'type': 'line',
                                'title': 'Estado',
                                #'range': [umMesAtras, today]
                            },
                            yaxis={
                                'title': 'taxa (%)',
                                #'range': [0, 50]
                            },
                            margin={'l': 40, 'b': 80, 't': 40, 'r': 40},
                            #title='Média Móvel de 5 dias da Taxa de Novas Mortes por Dia',
                            # legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    }
                ),
            ]),
        ]),
        html.Div(className='row', children=[
            html.Div(className='col-sm', children=[
                html.H3('Mortes por 100k habitantes',className='text-center'),
                dcc.Graph(
                    id='deaths_per_100k_inhabitants',
                    figure={
                        'data': [
                            dict(
                                # x=df[df['continent'] == i]['gdp per capita'],
                                #x=df[df['state'] == i]['date'],
                                x=statesClean,
                                y=[
                                    (
                                        df[df['state'] == i]['deaths_per_100k_inhabitants'].tail(1).tolist()[0]
                                    ) for i in statesClean
                                ],
                                #y=df[df['state'] == i]['deaths_per_100k_inhabitants'].tail(1),
                                # text=df[df['state'] == i]['state'],
                                # mode='markers',
                                # opacity=0.7,
                                # marker={
                                #    'size': 15,
                                #    'line': {'width': 0.5, 'color': 'white'}
                                # },
                                #name=i,
                                type='bar',
                                #orientation='h'
                            ) #for i in statesClean
                        ],
                        'layout': dict(
                            xaxis={
                                'type': 'line',
                                'title': 'data',
                                'range': [umMesAtras, today]
                            },
                            yaxis={'title': 'Mortes por 100k habitantes'},
                            margin={'l': 40, 'b': 80, 't': 40, 'r': 40},
                            #title='Mortes por 100k habitantes',
                            # legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    }
                )
            ])
        ])
    ]),
    html.Div(children=[
        html.P(children=[
            'Produzido por ',
            html.A(children='Galdir Reges', href='https://galdir.github.io/')
        ]),

        html.P(children=[
            'Dados de ',
            html.A(children='Wesley Cota', href="https://covid19br.wcota.me/"),
            ' e ',
            html.A(children='Secretaria de Saúde da Bahia',
                   href="http://www.saude.ba.gov.br/"),

        ]),
    ]),


])
# deaths_per_100k_inhabitants
if __name__ == '__main__':
    app.run_server(debug=True)
