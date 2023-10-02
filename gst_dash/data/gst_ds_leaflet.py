# Import required libraries
import pickle
import plotly.express as px
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
import plotly.graph_objects as go
import dash_table as dtb
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
from dash.dash import no_update
import dash_core_components as dcc
import dash_html_components as html
# from core_functions import *
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import numpy as np
import io, os, json, time
from math import asin, cos, sqrt, pi, atan2, radians


# Multi-dropdown options
# from controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS

# get relative data folder
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("data2").resolve()


# if '_init_' in __file__:
#     cwd = __file__.replace(r'industry_dash.py','')
# else:
#     cwd = __file__.replace(r'gst_ds_leaflet.py','')
#
# print(__file__, cwd)



cwd = os.getcwd()
cwd = '/var/www/multi_apps/multi_apps'
cwd = cwd + r'/gst_dash'




# , routes_pathname_prefix='/app2/', requests_pathname_prefix='/app2/'
# app = dash.Dash(
#     __name__, url_base_pathname='/app2/', meta_tags=[{"name": "viewport", "content": "width=device-width"}]
# )
app = dash.Dash(__name__)
server = app.server

app = dash.Dash( __name__,requests_pathname_prefix='/gst_dash/')
app.title = 'IndiaPulse@ISB'

# Create controls
timeline = ['Jan_20', 'Feb_20', 'Mar_20','Apr_20','May_20','Jun_20','Jul_20','Aug_20','Sep_20','Oct_20','Nov_20','Dec_20']
timedict = {'Jan_20':"January-2020", 'Feb_20':"February-2020", 'Mar_20':"March-2020",'Apr_20':'April-2020','May_20':'May-2020',
            'Jun_20':'June-2020','Jul_20':'July-2020','Aug_20':'August-2020','Sep_20':'September-2020','Oct_20':'October-2020',
            'Nov_20':'November-2020','Dec_20':'December-2020'}
# epfodt = pd.read_excel(cwd + r"State_epfo_data.xlsx")
# gstdt = pd.read_excel(cwd +  r"data/GST_monthly_growth_2020.xls")
# ectdt = pd.read_excel(cwd +  r"data/electricity_monthly_2020.xls")
epfodt = pd.read_excel(cwd + r"/State_epfo_data.xlsx")
gstdt = pd.read_excel(cwd +  r"/data/GST_monthly_growth_2020.xls")
ectdt = pd.read_excel(cwd +  r"/data/electricity_monthly_2020.xls")
with open(cwd + r'/'+ r'data/State_LGD_preLadakh.geojson', 'r') as f:
    statesgeo = json.load(f)
# with open(r"E:/gis-dashboard/testdsh/GEOJSON/Bank_Branch.geojson") as bk:
#     bankpos = json.load(bk)
for i in range(len(statesgeo['features'])):
    state = statesgeo['features'][i]['properties']['STNAME']
    df = gstdt[gstdt['state_name']==state]
    df2 = ectdt[ectdt['state_name']==state]
    # statesgeo['features'][i]['properties']['TOT_P'] = list(df['TOT_WORK_P'])[0] if len(df)>0 else None
    for time in timeline:
        # print(time)
        gst = list(df[time])[0]
        statesgeo['features'][i]['properties'][time] = round(float(gst), 2) # if len(df)>0 else None
        # statesgeo['features'][i][time] = round(float(gst), 2)
        try:
            ect = list(df2[time])[0]
            # statesgeo['features'][i]['ect_'+time] = round(float(ect), 2)
            statesgeo['features'][i]['properties']['ect_' + time] = round(float(ect), 2)
        except:
            # print(time,state)
            # statesgeo['features'][i]['ect_' + time] = None
            statesgeo['features'][i]['properties']['ect_' + time] = None



def checkpoint(ltref,ltlong,d=5):
    # approximate radius of earth in km
    if ltref is None:
        return True
    lon2, lat2 = ltlong
    lat1, lon1 = ltref
    p = pi / 180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    dist = 12742 * asin(sqrt(a))

    if dist <= d:
        # print(ltlong[0], ltlong[1], dist, d)
        return True

    else:
        return False

"""***********************************Leaflet Module Data-Script********************************"""
def get_info2(feature=None,ftype= None, time='Apr_20'):
    header = [html.H6("Power Consumption (Year-on-Year)")]
    if not feature:
        return header + ["Hover over a region"]
    ftp0 = 'India' if ftype == 'State' else feature['STATE'] if ftype == 'District' else feature[
        'DISTRICT'] if ftype == 'Tehsil' else feature['TAHSIL']
    header = [html.H6("Power Consumption (Year-on-Year)")]
    ftp = {'State': "STNAME", 'District': 'NAME', 'Tehsil': 'TAHSIL', 'Village': 'VILLAGE'}
    return header + [html.B(feature['properties'][ftp[ftype]]), html.Br(),
                     "Month: {}".format(timedict[time]), html.Sup(""), html.Br(),
                     "Power Consumption Change: {}".format(str(feature['properties']['ect_'+time])+'%'  if time != 'Dec_20' else 'NA')]

def get_info(feature=None,ftype= None, time='Apr_20'):
    header = [html.H6("GST Change (Year-on-Year)")]
    if not feature:
        return header + ["Hover over a region"]
    ftp0 = 'India' if ftype=='State' else feature['STATE'] if ftype=='District' else feature['DISTRICT'] if ftype=='Tehsil' else feature['TAHSIL']
    header = [html.H6("GST Change (Year-on-Year)")]
    ftp = {'State':"STNAME",'District':'NAME','Tehsil':'TAHSIL','Village':'VILLAGE'}
    return header + [html.B(feature['properties'][ftp[ftype]]), html.Br(),
                     "Month: {}".format(timedict[time]), html.Sup(""),html.Br(),
                     "GST Change: {}%".format(feature['properties'][time])]

classes = [100000,500000,1000000,5000000,10000000,50000000,100000000,200000000]
classes2 = [5000,10000,50000,100000,500000,1000000,5000000,10000000]
classes3 = [5000,10000,20000,50000,100000,200000,400000,1000000]
classes4 = [500,1000,2000,4000,6000,8000,10000,15000]

classesf = [-280,-200,-120,-80,-40,-20,-10,-5,0,5,10,20,40,80,120,200,280]
classesf2 = [-80,-70,-60,-50,-40,-30,-20,-10,0,10,20,40,50,60,70,80]#np.logspace(0,epfodt['Sep_20'].max(),8)
scale = ["{}".format(x) for x in classesf]
scale2 = ["{}".format(x) for x in classesf2]
# color = ["#ffffff","#ffe6e6","#ffcccc","#ffb3b3","#ff9999","#ff8080","#ff6666","#ff3333",'#e60000',"#990000"]
# # color.reverse()
# color2 = ["#e6ffe6","#ccffcc","#b3ffb3","#99ff99","#4dff4d","#1aff1a","#00e600","#00b300","#008000"]

color3ry = ['#990000','#e60000','#ff3333','#ff6666','#ff8080','#ff9999','#ffb3b3','#ffcccc','#ffffd6']
color3yg = ['#e6ffb8','#b3ffa4','#99ff99','#4dff4d','#1aff1a','#00e600','#00b300','#008000']
# colorscale = color+color2
colorscale = color3ry + color3yg
#colorscale = ['#F8CAB4','#F6AF8E', '#EB5F1E', '#CE4E12', '#BC4710', '#96380D', '#83310B', '#5E2308', '#381505', '#260E03']
style1 = dict(weight=2, opacity=1, color='grey', dashArray='3', fillOpacity=0.9)
style2 = dict(weight=1, opacity=1, color='white', dashArray='3', fillOpacity=0.2)
style3 = dict(weight=0.6, opacity=1, color='white', dashArray='3', fillOpacity=0.1)
style4 = dict(weight=0.6, opacity=1, color='white', dashArray='3', fillOpacity=0.1)
ctg = scale.copy()
ctg2 = scale2.copy()
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=500, height=30, position="bottomleft")

info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "bottom": "150px", "right": "10px", "z-index": "900"})

colorbar2 = dlx.categorical_colorbar(categories=ctg2, colorscale=colorscale, width=500, height=30, position="bottomleft")

info2 = html.Div(children=get_info2(), id="info2", className="info",
                style={"position": "absolute", "bottom": "150px", "right": "10px", "z-index": "900"})
# info2 = html.Div(children=get_info2(), id="info2", className="info",
#                 style={"position": "absolute", "bottom": "10px", "right": "10px", "z-index": "2000"})

"""**********************************************************************************************************************"""
# Load data
# df = pd.read_csv(DATA_PATH.joinpath("wellspublic.csv"), low_memory=False)
# df["Date_Well_Completed"] = pd.to_datetime(df["Date_Well_Completed"])
# df = df[df["Date_Well_Completed"] > dt.datetime(1960, 1, 1)]
#
# trim = df[["API_WellNo", "Well_Type", "Well_Name"]]
# trim.index = trim["API_WellNo"]
# dataset = trim.to_dict(orient="index")



#points = pickle.load(open(DATA_PATH.joinpath("points.pkl"), "rb"))


# Create global chart template
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

# Create app layout
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# df_atm = pd.read_excel(r"assets/Ambala_po_AllVillages.xlsx")
# dicts = df_atm.to_dict('rows')
# for item in dicts:
#     item["tooltip"] = "{:.1f}".format(item['PO_Code'])  # bind tooltip
#     item["popup"] = item["PO_Name"]  # bind popup
# geojson = dlx.dicts_to_geojson(dicts, lon="Longitude",lat="Latitude")  # convert to geojson
# geo_atmbuf = dlx.geojson_to_geobuf(geojson)

###### Layout
polygon = dl.Polygon(positions=[[57, 10], [57, 11], [56, 11], [57, 10]])

app.layout = html.Div([
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside",style={'display':'none'}),
        dbc.Row([
            dbc.Col(
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.H3(
                                                        "IndiaPulse@ISB",
                                                        style={"margin-bottom": "0px"},
                                                    ),
                                                    html.Hr(style={"margin-bottom": '2px',"margin-top": '2px'}),
                                                    html.H5(
                                                        "GST Collection", style={"margin-top": "0px"}
                                                    ),
                                                ]
                                            )
                                        ],
                                        #className="one-third column",
                                        id="title",
                                    ),

                                ],
                                className="pretty_container",
                                id="cross-filter-options",
                            ),

                            # html.Div(
                            #     [
                            #         dbc.Card(
                            #                 dbc.CardBody("""
                            #                 Year-on-year change in monthly GST Collection for each state is visualized on this time slider map
                            #                 for the year 2020, as compared to the year 2019."""),
                            #                 className="mb-3",
                            #                 ),
                            #     ],
                            #     className="pretty_container",
                            # ),
                            html.Div([
                            dcc.Graph(
                                id='barchart2',
                                figure={
                                    'data':[],
                                    'layout' : dict(hovermode='closest',
                                            height=500,
                                            # handles multiple points landing on the same vertical,
                                            # automargin = True,
                                            margin=dict(l=10, r=10, t=40, b=10),
                                            autosize = True,
                                            # showlegend = True,
                                            paper_bgcolor='transparent',
                                            plot_bgcolor='transparent')

                                }
                            ),

                        ],      id='bardiv',
                                # style={'display':'none'},
                                className="pretty_container_bar",
                            ),
                        ],
                        style = {'height':'100%'},
                        className = "pretty_container2  three columns",
                    )),

            dbc.Col([
                dbc.Row(
                    html.Div([
                        html.Div([
                            dl.Map(zoom=2, zoomSnap=0.25,
                                   children=[
                                       dl.TileLayer(url='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}.png',minZoom=4.75),
                                       # dl.Overlay(dl.LayerGroup(id="layer"), name="Custom Location",checked=False)]),

                                       # dl.TileLayer(url="https://online.transerve.com/preview-wms/5f802c037f660116b85e02ff?access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiNWRmMWY3OWVmOGUxNTM5Y2ZjZWRlM2ZkIiwic2Vzc2lvbiI6IjVmODAyYjZkN2Y2NjAxNzBjYjVlMDI4NiIsImlhdCI6MTYwMjIzNTM5NX0.xgoAoRQpfx-LNqww-Erc4d_MvFdhMtH3NOunaMX_E1E"),
                                       # dl.GeoJSON(data=bermuda),  # in-memory geojson (slowest option)
                                       # dl.GeoJSON(data=biosfera, format="geobuf"),  # in-memory geobuf (smaller payload than geojson)
                                       # dl.LayerGroup(id="layer"),

                                       dl.GeoJSON(data=statesgeo, id="states", zoomToBounds=True,
                                                  zoomToBoundsOnClick=False,
                                                  options=dict(style=dlx.choropleth.style),
                                                  hoverStyle=dict(weight=5, color='#666', dashArray=''),
                                                  hideout=dict(colorscale=colorscale, classes=classesf, style=style1,
                                                               color_prop='TOT_P')),
                                       dl.GeoJSON(data=[], id='districts', zoomToBounds=True, zoomToBoundsOnClick=False,
                                                  options=dict(style=dlx.choropleth.style),
                                                  hoverStyle=dict(weight=3, color='#555', dashArray=''),
                                                  hideout=dict(colorscale=colorscale, classes=classes2, style=style2,
                                                               color_prop='TOT_P')
                                                  ),
                                       dl.GeoJSON(data=[], id='tehsils', zoomToBounds=True, zoomToBoundsOnClick=False,
                                                  options=dict(style=dlx.choropleth.style),
                                                  hoverStyle=dict(weight=1.5, color='#555', dashArray=''),
                                                  hideout=dict(colorscale=colorscale, classes=classes3, style=style3,
                                                               color_prop='TOT_P')
                                                  ),
                                       dl.GeoJSON(data=[], id='villages', zoomToBounds=False, zoomToBoundsOnClick=True,
                                                  options=dict(style=dlx.choropleth.style),
                                                  hoverStyle=dict(weight=0.5, color='#555', dashArray=''),
                                                  hideout=dict(colorscale=colorscale, classes=classes4, style=style4,
                                                               color_prop='TOT_P')
                                                  ),
                                       colorbar,
                                       info,
                                       # geobuf resource (fastest option)
                                   ],
                                   style={'position': 'absolute','left': '396px', 'width': '38%', 'height': '88vh',
                                          "display": "block"},
                                   id="map-graph"),

                        ]),

                        # html.Div([
                        #     dcc.Graph(
                        #         id='barchart',
                        #         figure={
                        #             'data':[],
                        #             'layout' : dict(hovermode='closest',
                        #                     height=720,
                        #                     # handles multiple points landing on the same vertical,
                        #                     # automargin = True,
                        #                     margin=dict(l=10, r=10, t=40, b=10),
                        #                     autosize = True,
                        #                     # showlegend = True,
                        #                     paper_bgcolor='#e0e4cc',
                        #                     plot_bgcolor='#e0e4cc')
                        #
                        #         }
                        #     ),
                        #
                        # ],
                        #     style={'position': 'absolute', 'right': '5px', 'width': '25%', 'height': '87vh',
                        #                   },
                        #     className="pretty_container"
                        # )
                        html.Div([
                            dl.Map(zoom=2, zoomSnap=0.25,
                                   children=[
                                       dl.TileLayer(url='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}.png',minZoom=4.75),
                                       # dl.Overlay(dl.LayerGroup(id="layer"), name="Custom Location",checked=False)]),

                                       # dl.TileLayer(url="https://online.transerve.com/preview-wms/5f802c037f660116b85e02ff?access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiNWRmMWY3OWVmOGUxNTM5Y2ZjZWRlM2ZkIiwic2Vzc2lvbiI6IjVmODAyYjZkN2Y2NjAxNzBjYjVlMDI4NiIsImlhdCI6MTYwMjIzNTM5NX0.xgoAoRQpfx-LNqww-Erc4d_MvFdhMtH3NOunaMX_E1E"),
                                       # dl.GeoJSON(data=bermuda),  # in-memory geojson (slowest option)
                                       # dl.GeoJSON(data=biosfera, format="geobuf"),  # in-memory geobuf (smaller payload than geojson)
                                       # dl.LayerGroup(id="layer"),

                                       dl.GeoJSON(data=statesgeo, id="states2", zoomToBounds=True,
                                                  zoomToBoundsOnClick=False,
                                                  options=dict(style=dlx.choropleth.style),
                                                  hoverStyle=dict(weight=5, color='#666', dashArray=''),
                                                  hideout=dict(colorscale=colorscale, classes=classesf2, style=style1,
                                                               color_prop='ect_Jan_20')),
                                       dl.GeoJSON(data=[], id='districts2', zoomToBounds=True, zoomToBoundsOnClick=False,
                                                  options=dict(style=dlx.choropleth.style),
                                                  hoverStyle=dict(weight=3, color='#555', dashArray=''),
                                                  hideout=dict(colorscale=colorscale, classes=classes2, style=style2,
                                                               color_prop='TOT_P')
                                                  ),
                                       dl.GeoJSON(data=[], id='tehsils2', zoomToBounds=True, zoomToBoundsOnClick=False,
                                                  options=dict(style=dlx.choropleth.style),
                                                  hoverStyle=dict(weight=1.5, color='#555', dashArray=''),
                                                  hideout=dict(colorscale=colorscale, classes=classes3, style=style3,
                                                               color_prop='TOT_P')
                                                  ),
                                       dl.GeoJSON(data=[], id='villages2', zoomToBounds=False, zoomToBoundsOnClick=True,
                                                  options=dict(style=dlx.choropleth.style),
                                                  hoverStyle=dict(weight=0.5, color='#555', dashArray=''),
                                                  hideout=dict(colorscale=colorscale, classes=classes4, style=style4,
                                                               color_prop='TOT_P')
                                                  ),
                                       colorbar2,
                                       info2,
                                       # geobuf resource (fastest option)
                                   ],
                                   style={'position': 'absolute','right': '10px', 'width': '38%', 'height': '88vh',
                                          "display": "block"},
                                   id="map-graph2"),

                        ]),
                    ]
                    ),

                ),

                dbc.Row([
                    html.Div([
                        html.Div(
                            [
                                html.P(
                                    "Use the time-slider to visualize year-on-year change in monthly GST collections and power consumption of the states",
                                    className="control_label",
                                ),
                                dcc.Slider(
                                    id="timeline",
                                    min=0,
                                    max=11,
                                    step=None,

                                    marks = {i:{'label':x.split('_')[0]} for i,x in enumerate(timeline)},
                                    value=0,
                                    updatemode='drag',
                                )
                            ],
                            className="pretty_container",
                        ),
                    ]),
                ],
                    id='tab',
                    style={'position': 'absolute', 'right': '5px', 'top': '90vh', 'width': '76.5%'},
                )

            ])
        ]),
        html.Div(id="hiddenState-div", style={'display': 'none'}),
        html.Div(id="hiddenDist-div", style={'display': 'none'}),
        html.Div(id="hiddenteh-div", style={'display': 'none'}),
        html.Div(id="StateDist-div", style={'display': 'none'}),
        html.Div(id="dataframe-div", style={'display': 'none'}),
        html.Div(id="atm_df-div", style={'display': 'none'}),
        html.Div(id="bc_df-div", style={'display': 'none'}),
        html.Div(id="bnk_df-div", style={'display': 'none'}),
        html.Div(id="po_df-div", style={'display': 'none'}),
        html.Div(id="select-level", style={'display': 'none'}),
        html.Div(id="click-event", style={'display': 'none'}),
        html.Div(id="select-event", style={'display': 'none'}),
    ],
    #id="mainContainer",
    #style={"display": "flex", "flex-direction": "column","overflow-y": "hidden"},
)


"""***********************************leaflet- CALLBACKS****************************"""


@app.callback([
               Output("info", "children"),
               Output("info2", "children")],
              [Input("states", "hover_feature"),
               Input("states2", "hover_feature"),
               # Input("tehsils", "hover_feature"),
               # Input("villages", "hover_feature")
               ],
               [State('timeline','value')])
def info_hover(feature_st,feature_st2,tval):
    # print('Hi!!')
    user_call = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    time = timeline[tval]
    if user_call == 'states':
        # print(feature_st['properties'])
        return get_info(feature_st,'State',time), no_update
    elif user_call == 'states2':
        # if time == 'Dec_20':
        #     print("yes")
        return no_update, get_info2(feature_st2,'State',time)
    else:
        return no_update, no_update
    # if user_call == 'tehsils':
    #     return get_info(feature_teh,'Tehsil')
    # if user_call == 'villages':
    #     return get_info(feature_vil,'Village')


@app.callback(Output('states','hideout'),
              [Input('timeline','value')])
def update_gstinfo(time):
    if time is None:
        raise PreventUpdate
    else:
        time = timeline[time]
        hideout = dict(colorscale=colorscale, classes=classesf, style=style1,
                       color_prop=time)
        return hideout

@app.callback(Output('states2', 'hideout'),
              [Input('timeline','value')])
def update_ectinfo(time):

    if time is None:
        raise PreventUpdate
    else:
        if timeline[time] == 'Dec_20':
            time = 'ect_'+ timeline[time]
            stylet = dict(weight=2, opacity=1, color='grey', dashArray='3', fillOpacity=0.0)
            hideout = dict(colorscale=colorscale, classes=classesf2, style=stylet,
                           color_prop=time)
            return hideout
        else:
            time = 'ect_'+ timeline[time]
            hideout = dict(colorscale=colorscale, classes=classesf2, style=style1,
                           color_prop=time)
            return hideout

# @app.callback(
#     [Output('barchart','figure'),
#     Output('bardiv','style')],
#     [Input('states','hover_feature')],
#     prevent_initial_call=True)
def update_state_bar(state):
    yval = []
    xval = []
    if state is None:
        return no_update,{'display':'block'}
    else:
        st = state['properties']['STNAME']
    for time in timeline:
        yval.append(time.split('_')[0])
        xval.append(state[time])
    df = pd.DataFrame([])
    df['Month'] = yval
    df['gst'] = xval
    df["color"] = np.where(df["gst"] < 0, 'red', 'green')

    figure = {
        'data': [
            go.Bar(
                y=df['Month'],
                x=df['gst'],
                orientation='h',
                marker_color=df['color']
            )
        ],
        'layout': go.Layout(
            title=go.layout.Title(text="{} Monthly GST <br> (Year-on-Year, %)".format(st)),
            # xaxis={'title': 'GST change (yoy,%)', 'automargin': True},
            hovermode='closest',
            height=460,
            # handles multiple points landing on the same vertical,
            # automargin = True,
            margin=dict(l=30, r=10, t=80, b=30),
            # autosize=True,
            # showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    }
    return figure,{'display':'block'}





@app.callback(
     Output('barchart2','figure'),
    [Input('timeline','value')])
def update_bar(time):
    if time is None:
        raise PreventUpdate
    else:
        time = timeline[time]
        yval = []
        xval = []
        df = pd.DataFrame([])
        for feature in statesgeo['features']:
            yval.append(feature['properties']['STNAME'])
            xval.append(feature['properties'][time])
        df['state'] = yval
        df['gst'] = xval
        df["color"] = np.where(df["gst"] < 0, 'red', 'green')
        df = df.sort_values(['gst'],ascending=True)


        figure= {
            'data': [
                go.Bar(
                    y=df['state'],
                    x=df['gst'],
                    orientation='h',
                    marker_color=df['color']
                )
            ],
            'layout': go.Layout(
                title=go.layout.Title(text="StateWise GST (Year-on-Year)"),
                xaxis={'title': 'GST change (Year-on-Year,%)', 'automargin': True},
                hovermode='closest',
                height=680,
                # handles multiple points landing on the same vertical,
                # automargin = True,
                margin=dict(l=120, r=10, t=80, b=4),
                # autosize=True,
                # showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        }
        return figure



"""**************************************************************************************"""




# Main
# if __name__ == "__main__":
#     app.run_server(debug=True)
