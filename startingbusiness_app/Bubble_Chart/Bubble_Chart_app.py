"""
This file is a copy of the one in the multi page app, but is used to run the app singularly for testing purposes.

This file is used to code the page on dash showing the interactive bubblechart map and data table. The charts have been
developed using the plotly express library. The web page has been designed using dash (dcc and html). The interactivity
is instead created using app callbacks with dash dependencies (input, output).

The code should return a web page divided in four rows:
- a top row containing Gender and Region selectors
- a middle row with the bubble chart for the selected combination of gender and region and an option to animate by year
(NOTE: if both men and women are selected, this row will actually contain two columns, with one graph per column
representing each of the gender groups)
- a row containing a second title and a year selection for the data table
- a row containing the data [actual value, not score] for the chosen gender, region, and year.

Used PEP 8 - style guide for python
"""
# ------------------------------------------------Imports------------------------------------------------------------- #

from pathlib import Path
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash

df_path = Path(__file__).parent.joinpath("DBBubbleChart.csv")

df_general = pd.read_csv(df_path)
df_by_region = df_general.groupby(['Region', 'Year'], as_index=False).mean()

# -----------------------------------------------StyleSheet----------------------------------------------------------- #
external_stylesheets = [dbc.themes.COSMO]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

region_bubblechart_list = df_general['Region'].unique()
year_bubblechart_list = df_general['Year'].unique()

# -----------------------------------------------Navigation----------------------------------------------------------- #

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/", external_link=True)),
        dbc.NavItem(dbc.NavLink("Bubble Chart", href="/bubble_chart", external_link=True)),
        dbc.NavItem(dbc.NavLink("Choropleth Map", href="/choropleth_map", external_link=True)),
        dbc.NavItem(dbc.NavLink("Blog", href="/blog", external_link=True)),
        dbc.NavItem(dbc.NavLink("Profile", href="/profile", external_link=True)),
        dbc.NavItem(dbc.NavLink("Sign Up", href="/signup", external_link=True)),
        dbc.NavItem(dbc.NavLink("Log In", href="/login", external_link=True)),
    ],
    brand="Starting a Business",
    brand_href="/",
    brand_external_link=True,
    color="primary",
    dark=True,
    links_left=True,
    fluid=True,
    sticky="top",
)

# -------------------------------------------Web Page Style----------------------------------------------------------- #
# Creating the container as one row with the region and gender selectors, one with the bubble chart(s), one with the
# year selector and one with a table which will contain the actual values for the indicators being analysed
bubblechart_page = dbc.Container(fluid=True, children=[
    dbc.Row(dbc.Col(children=[html.Br()])),
    dbc.Row([html.Hr(),
             dbc.Col(width=2, children=[
                 html.H5("Select Gender"),
                 dbc.Checklist(
                     options=[
                         {"label": "Women", "value": 1},
                         {"label": "Men", "value": 2},
                     ],
                     value=[],
                     id="gender",
                     switch=True,
                     inline=True,
                     style={'margin': '20px'}
                 )
             ]),
             dbc.Col(children=[
                 html.H5("Select Region"),
                 dbc.Checklist(
                     options=[{"label": x, "value": x}
                              for x in region_bubblechart_list],
                     value=[],
                     inline=True,
                     id="region")]),
             html.Hr()]),
    dbc.Row([html.H2("Relationship between factors involved in starting a business", style={'text-align': 'center'}),
             html.Br(),
             html.H4("Calculated based on absolute score", style={'text-align': 'center'}),
             dbc.Col(id='bubble_chart_col', style={'left': '50%'}),
             ]),
    dbc.Row([html.Br(), html.Hr(), html.H2("Data for the chosen geographic area", style={'text-align': 'center'})]),
    dbc.Row([dbc.Col(children=[html.H5('Select Year', style={'text-align': 'center'}),
                               dcc.Dropdown(options=[{"label": x, "value": x}
                                                     for x in year_bubblechart_list],
                                            value='2006',
                                            id="year",
                                            multi=False,
                                            clearable=False)
                               ], width={"size": 4, "offset": 4})]),
    dbc.Row([
        dbc.Col(children=[
            dcc.Graph(id="values_table"),
        ], style={'left': '50%'}),
    ])
])

# -----------------------------------------------Layout--------------------------------------------------------------- #
# Generating app layout based on container

app.layout = html.Div([
    navbar, bubblechart_page])
layout2 = app.layout


# -------------------------------------------Interactivity and Charts------------------------------------------------- #
# Generating and updating the bubble chart and table (fig_bc) capturing the user inputs generated by selecting values
# in the different checklists. The different charts have an associated pandas dataframe.
def init_callbacks(dash_app):
    @dash_app.callback(
        [Output("values_table", "figure")],
        [Output("bubble_chart_col", "children")],
        [Input("gender", "value")], [Input("region", "value")],
        [Input("year", "value")])
    def update_chart(gender, region, year):
        """
            Function returns the figure for both the bubble chart and table based on the inputs captured by using the
            callbacks and passed as inputs of the function

            :param [int] gender: Gender selected from the checklist (1 = women, 2 = men)
            :param [list] region: List of region(s) selected from the checklist (can be single or multiple values)
            :param [list] year: Year selected from the dropdown menu (single value)
            :return:
                children for the bubble chart container (can be one graph or two)
                table with the true scores for the selected region
            """

        # Based on whether the selected gender is Men, Women, both, or neither, set the headers of the bubble chart and
        # of the table
        if gender == [1]:  # Gender is Women
            x_header_fig = 'Time - Women (days)- Score'
            y_header_fig = 'Procedures required - Women (number) - Score'
            size_header_fig = 'Cost - Women (% of income per capita) - Score'
            title_text_fig = 'Women'

            x_header_tab = 'Time - Women (days)'
            y_header_tab = 'Procedures required - Women (number)'
            z_header_tab = 'Cost - Women (% of income per capita)'
        elif gender == [2]:  # Gender is Men
            x_header_fig = 'Time - Men (days) - Score'
            y_header_fig = 'Procedures required - Men (number) - Score'
            size_header_fig = 'Cost - Men (% of income per capita) - Score'
            title_text_fig = 'Men'

            x_header_tab = 'Time - Men (days)'
            y_header_tab = 'Procedures required - Men (number)'
            z_header_tab = 'Cost - Men (% of income per capita)'
        elif not gender:  # Neither Men nor Women was selected
            x_header_fig = 'Time (Average) - Score'
            y_header_fig = 'Procedures required (Average) - Score'
            size_header_fig = 'Cost (Average) - Score'
            title_text_fig = 'Average of men and women'

            x_header_tab = 'Time (Average)'
            y_header_tab = 'Procedures required (Average)'
            z_header_tab = 'Cost (Average)'

        # Based on which region (or regions) has been selected in the checklist, select the relevant rows in the
        # dataframe (i.e. those whose 'region' value matches the one selected) and keep those rows. For all the
        # unselected regions, calculate scores as average of the scores for that region
        if not region:
            df = df_by_region
            df_tab = df
            hover_header = 'Region'
        else:
            df_averaged = df_general.loc[~(df_general['Region'].isin(region))].groupby(['Region', 'Year'],
                                                                                       as_index=False).mean()
            df = df_general.loc[df_general['Region'].isin(region)].append(df_averaged)
            hover_header = 'Country Name'
            # drop countries that cannot be represented in the chart because of a value = 0
            df_tab = df[~(df['Country Name'].isnull())]
            for r in range(
                    len(df['Country Name'])):  # update the country name to match the region name for the averaged rows
                if pd.isnull(df['Country Name'].iloc[r]):
                    df['Country Name'].iloc[[r]] = df['Region'].iloc[[r]]

        df = df.sort_values(by=['Region', 'Year'])  # to maintain the color constant (and to not change the year)

        df_tab = df_tab[df_tab['Year'] == int(year)]  # dataframe for the chosen year

        if len(gender) != 2:  # create graphs when only one selection is made for gender
            df = df.dropna(subset=[x_header_fig, y_header_fig, size_header_fig])
            df = df.loc[
                ~((df[x_header_fig] == 0) | (df[y_header_fig] == 0) | (df[size_header_fig] == 0))]
            # create bubble chart
            fig = px.scatter(df,
                             x=x_header_fig,
                             y=y_header_fig,
                             animation_frame='Year',
                             size=size_header_fig,
                             color='Region',
                             range_x=[-10, 110],
                             range_y=[-10, 110],
                             hover_name=hover_header,
                             labels={x_header_fig: 'Time [Score]',
                                     y_header_fig: 'Procedures required [Score]',
                                     size_header_fig: 'Cost [Score]'
                                     },
                             title=title_text_fig)
            if region:
                # if one specific region is selected to open up, slightly fade the markers at the back
                for year_i in df['Year'].unique():
                    fig.for_each_trace(
                        lambda trace: trace.update(marker={"opacity": 0.4}) if (trace.name not in region) else (),
                    )

            fig.layout.autosize = True
            fig.update_layout(title=dict(font=dict(size=20)),
                              margin=dict(l=15, r=15, t=35, b=5),
                              autosize=True)
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })
            children_bc = dcc.Graph(id="bubble_chart", figure=fig)

            # create the table
            tab = go.Figure(
                data=[go.Table(header=dict(values=list([hover_header, x_header_tab, y_header_tab, z_header_tab])),
                               cells=dict(
                                   values=[df_tab[hover_header], df_tab[x_header_tab], df_tab[y_header_tab],
                                           df_tab[z_header_tab]])
                               )])
        else:  # create graphs when both men and women have been selected
            df = df.dropna(subset=['Time - Women (days)',
                                   'Time - Men (days)',
                                   'Procedures required - Women (number)',
                                   'Procedures required - Men (number)',
                                   'Cost - Women (% of income per capita)',
                                   'Cost - Men (% of income per capita)'])

            # create women bubble chart
            fig_W = px.scatter(df,
                               x='Time - Women (days)- Score',
                               y='Procedures required - Women (number) - Score',
                               animation_frame='Year',
                               size='Cost - Women (% of income per capita) - Score',
                               color='Region',
                               range_x=[-10, 110],
                               range_y=[-10, 110],
                               hover_name=hover_header,
                               labels={'x': 'Time [Score]',
                                       'y': 'Procedures required [Score]',
                                       'size': 'Cost [Score]'
                                       },
                               title='Women')

            # create men bubble chart
            fig_M = px.scatter(df,
                               x='Time - Men (days) - Score',
                               y='Procedures required - Men (number) - Score',
                               animation_frame='Year',
                               size='Cost - Men (% of income per capita) - Score',
                               color='Region',
                               range_x=[-10, 110],
                               range_y=[-10, 110],
                               hover_name=hover_header,
                               labels={'x': 'Time [Score]',
                                       'y': 'Procedures required [Score]',
                                       'size': 'Cost [Score]'
                                       },
                               title='Men')

            if region:
                # if one specific region is selected to open up, slightly fade the markers at the back
                for year_i in df['Year'].unique():
                    fig_W.for_each_trace(
                        lambda trace: trace.update(marker={"opacity": 0.4}) if (trace.name not in region) else (),
                    )
                    fig_M.for_each_trace(
                        lambda trace: trace.update(marker={"opacity": 0.4}) if (trace.name not in region) else (),
                    )

            fig_W.layout.autosize = True
            fig_W.update_layout(title=dict(font=dict(size=20)),
                                margin=dict(l=15, r=15, t=35, b=5),
                                autosize=True)
            fig_W.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })
            fig_M.layout.autosize = True
            fig_M.update_layout(title=dict(font=dict(size=20)),
                                margin=dict(l=15, r=15, t=35, b=5),
                                autosize=True)
            fig_M.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })

            # create two subcolumns to display both charts
            children_bc = [
                dbc.Row(
                    children=[dbc.Col(children=[dcc.Graph(id="bubble_chart_W", figure=fig_W)], style={'left': '50%'}),
                              dbc.Col(children=[dcc.Graph(id="bubble_chart_M", figure=fig_M)], style={'left': '50%'})])]

            # create table
            tab = go.Figure(
                data=[go.Table(header=dict(values=list([hover_header, 'Time - Women (days)',
                                                        'Time - Men (days)',
                                                        'Procedures required - Women (number)',
                                                        'Procedures required - Men (number)',
                                                        'Cost - Women (% of income per capita)',
                                                        'Cost - Men (% of income per capita)'])),
                               cells=dict(
                                   values=[df_tab[hover_header], df_tab['Time - Women (days)'],
                                           df_tab['Time - Men (days)'], df_tab['Procedures required - Women (number)'],
                                           df_tab['Procedures required - Men (number)'],
                                           df_tab['Cost - Women (% of income per capita)'],
                                           df_tab['Cost - Men (% of income per capita)']])
                               )])
        tab.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })

        return tab, children_bc


def init_dashboard(flask_app):
    dash_app = dash.Dash(server=flask_app, routes_pathname_prefix='/bubble_chart/',
                         external_stylesheets=[dbc.themes.SANDSTONE])
    dash_app.layout = layout2
    dash_app.title = "Bubble Chart"
    init_callbacks(dash_app)
    return dash_app.server


if __name__ == '__main__':
    app.run_server(debug=True)
