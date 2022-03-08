"""
This file is used to code the we page on dash showing the interactive choropleth map and bar chart. The charts have been
developed using the plotly express library. The web page has been designed using dash (dcc and html). The interactivity
is instead created using app callbacks with dash dependencies (input, output).

The code should return a web page divided in two columns. A side column having two parameters (region, income) dropdown
menus and a barchart (with another dropdown menu for the year). The main column instead has a dropdown menu to select
the indicator and the choropleth map with the year animation.

Used PEP 8 - style guide for python
"""

# ------------------------------------------------Imports------------------------------------------------------------- #

from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Disabling SettingCopyWarning from pandas as it was flagging a (falsely) potentially confusing "chained" assignment
pd.options.mode.chained_assignment = None

# ------------------------------------------------Data&Lists---------------------------------------------------------- #
# Import data from the correct directory and add lists for dropdown menus

df_path = Path(__file__).parent.joinpath("DBresorted_cm.csv")
# df_path = Path('Data Set')
df_cm_bc = pd.read_csv(str(df_path))
# df_cm_bc = pd.read_csv('./DBresorted_cm.csv')

indicator_dropdown_list = ['Starting a business - Score',
                           'Starting a business: Cost - Average (% of income per capita) - Score',
                           'Starting a business: Procedures required - Average (number) - Score',
                           'Starting a business: Time - Average (days) - Score',
                           'Starting a business: Paid-in Minimum capital (% of income per capita) - Score']

region_dropdown_list = ['World', 'South Asia', 'Middle East & North Africa', 'Europe & Central Asia',
                        'Sub-Saharan Africa', 'Latin America & Caribbean', 'East Asia & Pacific', 'North America']

income_dropdown_list = ['All', 'Low income', 'Upper middle income', 'Lower middle income', 'High income']

# -------------------------------------------Web Page Style----------------------------------------------------------- #
# Creating the container as two columns of different widths to incorporate the dropdown menus and both the choropleth
# map (main column) and bar chart (side column). Enabled the multi selection function for dropdowns and disabled the
# clearable.
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/", external_link=True)),
        dbc.NavItem(dbc.NavLink("Profiles", href="/", external_link=True)),
        dbc.NavItem(dbc.NavLink("Bubble Chart", href="/bubble_chart", external_link=True)),
        dbc.NavItem(dbc.NavLink("Choropleth Map", href="/choropleth_map", external_link=True)),
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
layout = html.Div([
    navbar,
    dbc.Container(fluid=True, children=[
        dbc.Row(
            dbc.Col(children=[html.Br()])),

        dbc.Row([
            dbc.Col(width=4, children=[

                html.H5("Select Region"),
                dcc.Dropdown(
                    id='region',
                    options=[{'value': x, 'label': x} for x in region_dropdown_list],
                    value=[],  # region_dropdown_list[0]
                    clearable=False,
                    multi=True),
                html.Br(),

                html.H5("Select Income Group"),
                dcc.Dropdown(
                    id='income',
                    options=[{'value': x, 'label': x} for x in income_dropdown_list],
                    value=[],  # income_dropdown_list[0]
                    clearable=False,
                    multi=True),
                html.Br(),

                html.H4("Top 10 charts"),
                dcc.Graph(id='barchart'),

                html.H5("Select Bar Chart Year"),
                dcc.Dropdown(
                    id='year',
                    options=[{'value': x, 'label': x} for x in list(range(2006, 2021, 1))],
                    value=2006,
                    clearable=False,
                    multi=False),
                html.Br()
            ]),

            dbc.Col(width=8, children=[
                html.H5("Select Indicator"),
                dcc.Dropdown(
                    id='indicator',
                    options=[{'value': x, 'label': x} for x in indicator_dropdown_list],
                    value=indicator_dropdown_list[0],
                    clearable=False),
                html.Br(),
                dcc.Graph(id='choropleth'),
            ]),
        ]),
    ])])


# -----------------------------------------------Layout--------------------------------------------------------------- #
# Generating app layout based on container


def init_dashboard(flask_app):
    dash_app = dash.Dash(server=flask_app, routes_pathname_prefix='/choropleth_map/',
                         external_stylesheets=[dbc.themes.SANDSTONE])
    dash_app.layout = layout
    init_callbacks(dash_app)
    return dash_app.server


# -------------------------------------------Interactivity and Charts------------------------------------------------- #
# Generating and updating the choropleth map (fig_cm) and bar chart (fig_bc) capturing the user inputs generated by
# selecting values in the different dropdown menus. The different charts have an associated pandas dataframe.

def init_callbacks(dash_app):
    @dash_app.callback(
        [Output("choropleth", "figure"), Output("barchart", "figure")],
        [Input("indicator", "value")], [Input("region", "value")], [Input("income", "value")], [Input("year", "value")])
    def update_output(indicator, region, income, year):
        """
        Function returns the figure for both the choropleth map and bar chart based on the inputs captured by using the
        callbacks and passed as inputs of the function

        :param [str] indicator: Indicator selected from the dropdown menu
        :param [list] region: List of regions selected from the dropdown menu (can be single or multiple values)
        :param [list] income: List of income groups selected from the dropdown menu (can be single or multiple values)
        :param [str] year: Value selected for the year to display in the bar chart
        :return: figures for choropleth map and bar chart
        """

        # When no values are selected from multi choice then use the standard values for region and income group
        if len(region) == 0:
            region = ['World']
        if len(income) == 0:
            income = ['All']

        # -------------------------------------------Choropleth Map--------------------------------------------------- #

        # Modifying the dataframe to generate choropleth map by taking data for only the selected regions. Setting fitbound
        # value variable to locations to automatically zoom in selected regions in the map
        if 'World' not in region:
            df_choropleth = df_cm_bc.loc[df_cm_bc['Region'].isin(region)]
            fitbound_value_cm = 'locations'
        else:
            df_choropleth = df_cm_bc
            fitbound_value_cm = False

        # Modifying the dataframe to generate choropleth map by taking data for only the selected income groups
        if 'All' not in income:
            df_choropleth = df_choropleth.loc[df_cm_bc['Income Group'].isin(income)]
        else:
            df_choropleth = df_choropleth

        # Generate choropleth map using specific values for range_color to have constant color scale
        fig_cm = px.choropleth(df_choropleth,
                               locations="Country Code",
                               color=indicator,
                               hover_name="Country Name",
                               projection='natural earth',
                               title=str(indicator),
                               animation_frame='Year',
                               hover_data={'Country Code': False},
                               color_continuous_scale=px.colors.sequential.Plasma,
                               fitbounds=fitbound_value_cm,
                               range_color=[0, 100])

        # Update the layout (title, margin and color bar title) for choropleth map figure
        fig_cm.update_layout(title=dict(font=dict(size=20)),
                             margin=dict(l=15, r=15, t=35, b=5),
                             coloraxis_colorbar=dict(title="Score"))
        fig_cm.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })

        # ------------------------------------------Bar Chart--------------------------------------------------------- #

        # Modify the same database used for choropleth to display same data but only showing the top 10 countries in a
        # ranking order
        df_barchart = df_choropleth.loc[df_choropleth['Year'] == year]
        df_barchart.sort_values(by=[str(indicator)], inplace=True, ascending=False)
        df_barchart = df_barchart.head(10)
        df_barchart = df_barchart[df_barchart[str(indicator)].notna()]
        df_barchart.sort_values(by=[str(indicator)], inplace=True, ascending=True)

        # Creating a list in order to change color of bar chart based on the position. List can take different dimensions
        # due to number of countries available for selected parameters. Thus creating a list for the top n positions with
        # n between 0 and 10
        if df_barchart[str(indicator)].count() in range(3, 11):
            list_pos_color = ['Runners up' for i in range(1, df_barchart[str(indicator)].count() - 2)]
            list_pos_color.extend(('Third', 'Second', 'First'))
        elif df_barchart[str(indicator)].count() == 3:
            list_pos_color = ['Third', 'Second', 'First']
        elif df_barchart[str(indicator)].count() == 2:
            list_pos_color = ['Second', 'First']
        elif df_barchart[str(indicator)].count() == 1:
            list_pos_color = ['First']
        else:
            list_pos_color = []

        # Generating bar chart figure specifying colours for first, second, third and runners up positions and adding name
        # of country over the bar
        fig_bc = px.bar(df_barchart,
                        x=indicator,
                        y='Country Name',
                        orientation='h',
                        labels={str(indicator): 'Score'},
                        hover_data={'Country Name': False},
                        color=list_pos_color,
                        text='Country Name',
                        color_discrete_map={'First': 'rgb(255,215,0)',  # Gold
                                            'Second': 'rgb(192,192,192)',  # Silver
                                            'Third': 'rgb(205, 127, 50)',  # Bronze
                                            'Runners up': 'rgb(204, 229, 255)'})  # Light blue

        # Disabling the y-axes labels and title
        fig_bc.update_yaxes(visible=False, showticklabels=False)
        fig_bc.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })

        return fig_cm, fig_bc
