# -*- coding: utf-8 -*-

# FUNÇÃO PARA TIRAR O SINAL DE IGUAL NOS GRÁFICOS                         -----> fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
# FUNÇÃO QUE TIRA A SINCRONIA DOS EIXOS, PERMITINDO UM ZOOM EM CADA FRAME -----> fig.update_yaxes(matches=None) OU fig.update_xaxes(matches=None)
# FUNÇÃO PARA TIRAR AS LINHAS DO GRID DA GRÁFICO                          -----> fig.update_xaxes(showgrid=False) OU fig.update_yaxes(showgrid=False)
# FUNÇÃO PARA AUMENTAR A BORDA DAS BARRAS DO GRÁFICO                      -----> fig.data[0].marker.line.width = 4 E DEPOIS, fig.data[0].marker.line.color = "black"



from dash import Dash, dcc, html, Input, Output
import plotly.express as px
app = Dash(__name__)

app.layout = html.Div([
    html.H4('Analysis of Iris data using scatter matrix'),
    dcc.Dropdown(
        id="dropdown",
        options=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
        value=['sepal_length', 'sepal_width'],
        multi=True
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
def update_bar_chart(dims):
    df = px.data.iris() # replace with your own data source
    fig = px.scatter_matrix(
        df, dimensions=dims, color="species")
    return fig


app.run_server(debug=False)
# __________________________________________________________________________________________________________________________________________________________________
# # Podem ser Scatter, Line, Area e Bar Charts
# # import plotly.express as px
# # df = px.data.iris()
# # fig = px.area(df, x="sepal_width", y="sepal_length", color="species")
# # fig.show()

# # # Abaixo São Criados PLOTS de Trending Lines, Templates e Distribuição Marginal
# # import plotly.express as px
# # df = px.data.iris()
# # fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", marginal_y="violin",
# #            marginal_x="box", trendline="ols", template="simple_white")
# # fig.show()

# # Barras de Erros, Utilizadas Para Machine Learning Futuramente, type='data', # value of error bar given in data coordinates
#                                     # type='percent', # value of error bar given as percentage of y value
# __________________________________________________________________________________________________________________________________________________________________


# # import plotly.graph_objects as go
# # import numpy as np

# # x_theo = np.linspace(-4, 4, 100)
# # sincx = np.sinc(x_theo)
# # x = [-3.8, -3.03, -1.91, -1.46, -0.89, -0.24, -0.0, 0.41, 0.89, 1.01, 1.91, 2.28, 2.79, 3.56]
# # y = [-0.02, 0.04, -0.01, -0.27, 0.36, 0.75, 1.03, 0.65, 0.28, 0.02, -0.11, 0.16, 0.04, -0.15]

# # fig = go.Figure()
# # fig.add_trace(go.Scatter(
# #     x=x_theo, y=sincx,
# #     name='sinc(x)'
# # ))
# # fig.add_trace(go.Scatter(
# #     x=x, y=y,
# #     mode='markers',
# #     name='measured',
# #     error_y=dict(
# #         type='constant',
# #         value=0.1,
# #         color='purple',
# #         thickness=1.5,
# #         width=3,
# #     ),
# #     error_x=dict(
# #         type='constant',
# #         value=0.2,
# #         color='purple',
# #         thickness=1.5,
# #         width=3,
# #     ),
# #     marker=dict(color='purple', size=8)
# # ))
# # fig.show()
# __________________________________________________________________________________________________________________________________________________________________

# # É Possível Customizar O Interior Dos Gráficos De Barra com ---> barmode="group"
# # import plotly.express as px
# # df = px.data.medals_long()

# # fig = px.bar(df, x="medal", y="count", color="nation",
# #              pattern_shape="nation", pattern_shape_sequence=[".", "x", "+"])
# # fig.show()

# # Controla A Ordem Dos Frames -----> category_orders
# # import plotly.express as px
# # df = px.data.tips()
# # fig = px.bar(df, x="sex", y="total_bill", color="smoker", barmode="group", facet_row="time", facet_col="day",
# #        category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]})
# # fig.show()
# __________________________________________________________________________________________________________________________________________________________________


# # Synchronizing axes in subplots with matches
# # Using facet_col from plotly.express let zoom and pan each facet to the same range implicitly. 
# # However, if the subplots are created with make_subplots, the axis needs to be updated with matches parameter to update all the subplots accordingly.
# # Zoom in one trace below, to see the other subplots zoomed to the same x-axis range. To pan all the subplots, click and drag from the
# # center of x-axis to the side ( Vai Sempre Dar Zoom Em Todos Os Gráficos Juntos, Facilitando Comparações)

# # import plotly.graph_objects as go
# # from plotly.subplots import make_subplots
# # import numpy as np

# # N = 20
# # x = np.linspace(0, 1, N)

# # fig = make_subplots(1, 3)
# # for i in range(1, 4):
# #     fig.add_trace(go.Scatter(x=x, y=np.random.random(N)), 1, i)
# # fig.update_xaxes(matches='x')
# # fig.show()
# __________________________________________________________________________________________________________________________________________________________________


# # Adding the Same Trace to All Facets
# # The .add_trace() method can be used to add a copy of the same trace to each facet, for example an overall linear regression line as below. 
# # The legendgroup/showlegend pattern below is recommended to avoid having a separate legend item for each copy of the trace. Note that as of v5.2.1, 
# # there is a built-in option to add an overall trendline to all facets that uses this technique under the hood. (Utilizar a Mesma Reta Linear Para Todos Os Frames)

# # import plotly.express as px
# # df = px.data.tips()
# # fig = px.scatter(df, x="total_bill", y="tip", color='sex',
# #                  facet_col="day", facet_row="time")

# # import statsmodels.api as sm
# # import plotly.graph_objects as go
# # df = df.sort_values(by="total_bill")
# # model = sm.OLS(df["tip"], sm.add_constant(df["total_bill"])).fit()

# # #create the trace to be added to all facets
# # trace = go.Scatter(x=df["total_bill"], y=model.predict(),
# #                    line_color="black", name="overall OLS")

# # # give it a legend group and hide it from the legend
# # trace.update(legendgroup="trendline", showlegend=False)

# # # add it to all rows/cols, but not to empty subplots
# # fig.add_trace(trace, row="all", col="all", exclude_empty_subplots=True)

# # # set only the last trace added to appear in the legend
# # # `selector=-1` introduced in plotly v4.13
# # fig.update_traces(selector=-1, showlegend=True)
# # fig.show()
# __________________________________________________________________________________________________________________________________________________________________

# # Adding Lines and Rectangles to Facet Plots
# # introduced in plotly 4.12

# # It is possible to add labelled horizontal and vertical lines and rectangles to facet plots using .add_hline(), .add_vline(), .add_hrect() or .add_vrect().
# # The default row and col values are "all" but this can be overridden, as with the rectangle below, which only appears in the first column.

# import plotly.express as px

# df = px.data.stocks(indexed=True)
# fig = px.line(df, facet_col="company", facet_col_wrap=2)
# fig.add_hline(y=1, line_dash="dot",
#               annotation_text="Jan 1, 2018 baseline",
#               annotation_position="bottom right")

# fig.add_vrect(x0="2018-09-24", x1="2018-12-18", col=1,
#               annotation_text="decline", annotation_position="top left",
#               fillcolor="green", opacity=0.25, line_width=0)
# fig.show()
# __________________________________________________________________________________________________________________________________________________________________

# # Wrapping Column Facets
# # When the facet dimension has a large number of unique values, it is possible to wrap columns using the facet_col_wrap argument.
# # Utilizando FACET_COL Para Escolher Quantos Quadros Serão Divididos As Informações!!

# import plotly.express as px
# df = px.data.gapminder()
# fig = px.scatter(df, x='gdpPercap', y='lifeExp', color='continent', size='pop',
#                 facet_col='year', facet_col_wrap=4)
# fig.show()
# __________________________________________________________________________________________________________________________________________________________________

# # # Historigrama Simples, Utilizando Category_Ordders Para Escolher A Ordem Dos Frames!!!
# # Histogram Facet Grids
# import plotly.express as px
# df = px.data.tips()
# fig = px.histogram(df, x="total_bill", y="tip", color="sex", facet_row="time", facet_col="day",
#        category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]})
# fig.show()
# __________________________________________________________________________________________________________________________________________________________________

# # Choropleth Column Facets
# # new in version 4.13
# # Utilizando GeoLocalização Para Ver Quantidade De Votos Por Distrito!!!!
# import plotly.express as px

# df = px.data.election()
# df = df.melt(id_vars="district", value_vars=["Coderre", "Bergeron", "Joly"],
#             var_name="candidate", value_name="votes")
# geojson = px.data.election_geojson()

# fig = px.choropleth(df, geojson=geojson, color="votes", facet_col="candidate",
#                     locations="district", featureidkey="properties.district",
#                     projection="mercator"
#                    )
# fig.update_geos(fitbounds="locations", visible=False)
# fig.show()
# __________________________________________________________________________________________________________________________________________________________________