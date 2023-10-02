# Import required libraries
import pickle
import plotly.express as px
import pathlib
import base64
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

cwd = os.getcwd()
# cwd = '/var/www/multi_apps/multi_apps'
cwd = cwd + r'/ewb_dash'

app = dash.Dash( __name__,requests_pathname_prefix='/ewb_dash/')
app.title = 'IndiaPulse@ISB'

button_style = {
  "border-radius": "0px",
  "margin": "1px",
  "padding": "1px",
  "width":"15%",
  "position": "relative",
  'border': '1px solid #e0e4cc',
  "box-shadow": "1px 1px 1px #F2F4F7",
  "backgroundColor": '#F2F4F7'
}
button_style_selected = {
  "border-radius": "2px",
  "margin": "1px",
  "padding": "1px",
  "width":"15%",
  "position": "relative",
  'borderTop': '1px solid #d6d6d6',
  'borderBottom': '1px solid #d6d6d6',
  "box-shadow": "1px 1px 1px #F2F4F7",
  "backgroundColor": '#00567A',
  "color":"white"
}
button_style2 = {
  "border-radius": "0px",
  "margin": "1px",
  "padding": "1px",
  "width":"30%",
  "position": "relative",
  'border': '1px solid #e0e4cc',
  "box-shadow": "1px 1px 1px #F2F4F7",
  "backgroundColor": '#F2F4F7'
}
button_style_selected2 = {
  "border-radius": "2px",
  "margin": "1px",
  "padding": "1px",
  "width":"30%",
  "position": "relative",
  'borderTop': '1px solid #d6d6d6',
  'borderBottom': '1px solid #d6d6d6',
  "box-shadow": "1px 1px 1px #F2F4F7",
  "backgroundColor": '#00567A',
  "color":"white"
}

# Create controls
timeline = ['Jan_20', 'Feb_20', 'Mar_20', 'Apr_20', 'May_20', 'Jun_20', 'Jul_20', 'Aug_20', 'Sep_20', 'Oct_20',
            'Nov_20', 'Dec_20']
timedict = {'Jan_20': "January-2020", 'Feb_20': "February-2020", 'Mar_20': "March-2020", 'Apr_20': 'April-2020',
            'May_20': 'May-2020',
            'Jun_20': 'June-2020', 'Jul_20': 'July-2020', 'Aug_20': 'August-2020', 'Sep_20': 'September-2020',
            'Oct_20': 'October-2020',
            'Nov_20': 'November-2020', 'Dec_20': 'December-2020'}
name_dict = {"intra_eway":"INTRA-STATE","intra_asset":"Value within State","inter_out_eway":"INTER-STATE (OUT)",
             "inter_out_asset":"Value Shipped out","inter_in_eway":"INTER-STATE (IN)","inter_in_asset":"Value Shipped in",
             "eway_tot":"Combined Value",'asset_tot':'Combined Value'}
button_dict = {
               'but-0':"intra_asset",'but-1':'inter_out_asset','but-2':'inter_in_asset','but-3':"asset_tot",'but-4':"2019",
               'but-5':'2020','but-6':"2021"
              }

label_dict = { "intra_eway":"Inter-State E-Way Bills(Lakhs)","intra_asset":"Inter-State Assets(Crores)","inter_out_eway":"Intra-State E-Way Out Bills(Lakhs)",
             "inter_out_asset":"Intra-State Out Assets(Crores)","inter_in_eway":"Intra-State In E-Way Bills(Lakhs)","inter_in_asset":"Intra-State In Assets(Crores)"}

# epfodt = pd.read_excel(cwd + r"State_epfo_data.xlsx")
dfdt = pd.read_excel(cwd + r'/' + r"data/ewb-data-2019-20_per_capita_rounded_new.xlsx")
dfdt['year'] = dfdt['year'].astype(int)
dfdt['month'] = dfdt['month'].astype(int)
# dfdt2 = dfdt[dfdt['year']==2020].reset_index(drop=True)
# dfdt2 = dfdt[dfdt['year']==2020].reset_index(drop=True)
# ectdt = pd.read_excel(cwd + r"data/electricity_monthly_2020.xls")
with open(cwd + r'/' + r'data/State_LGD_preLadakh_processed.geojson', 'r') as f:
    statesgeo = json.load(f)
# with open(r"E:/gis-dashboard/testdsh/GEOJSON/Bank_Branch.geojson") as bk:
#     bankpos = json.load(bk)
timeline2 = timeline.copy()

print("Done")

"""***********************************Leaflet Module Data-Script********************************"""
res=1500

def get_info2(feature=None,ftype= None, type=None, time='Apr_20'):
    header = [html.H6("E-Way Bills Generated (in Lakhs)", style={'font-size': '{}rem'.format(1.5*(res/1500)), "margin-bottom": "0px"})]
    if not feature:
        return header + [html.P("Hover over a region",style={'font-size': '{}rem'.format(1.1*(res/1500))})]

    ftp0 = 'India' if ftype == 'State' else feature['STATE'] if ftype == 'District' else feature[
        'DISTRICT'] if ftype == 'Tehsil' else feature['TAHSIL']
    header = [html.H6("E-Way Bills Generated (in Lakhs)", style={'font-size': '{}rem'.format(1.5*(res/1500)), "margin-bottom": "0px"})]
    ftp = {'State': "STNAME", 'District': 'NAME', 'Tehsil': 'TAHSIL', 'Village': 'VILLAGE'}
    if type == None:
        return header + [
            html.B(feature['properties'][ftp[ftype]], style={'font-size': '{}rem'.format(1.1 * (res / 1500))}),
            html.Br()] + [html.B(feature['properties'][ftp[ftype]],style={'font-size': '{}rem'.format(1.1*(res/1500))}),html.Br()] + ["Make a Selection"]
    return header + [html.B(feature['properties'][ftp[ftype]], style={'font-size': '{}rem'.format(1.1 * (res / 1500))}), html.Br(),
                     html.Plaintext("Month: {}".format(timedict[time]),
                                    style={'font-size': '{}rem'.format(1.1 * (res / 1500)), "margin-top": "0px",
                                           "margin-bottom": "0px"}),
                     html.Plaintext("{}: {}".format(name_dict[type], feature['properties'][type + '_' + time]),
                                    style={'font-size': '{}rem'.format(1.1 * (res / 1500)), "margin-top": "0px",
                                           "margin-bottom": "0px"})]


def get_info(feature=None,ftype= None, type='', time='Apr',year=2021):
    timef = time+'_'+str(year)[2:]
    header = [html.H6("Value of Traded Goods per Person (INR)", style={'font-size': '{}rem'.format(1.5*(res/1500)), "margin-bottom": "0px"})]
    if not feature:
        return header + [html.P("Hover over a region",style={'font-size': '{}rem'.format(1.1*(res/1500))})]
    ftp0 = 'India' if ftype=='State' else feature['STATE'] if ftype=='District' else feature['DISTRICT'] if ftype=='Tehsil' else feature['TAHSIL']
    header = [html.H6("Value of Traded Goods per Person (INR)", style={'font-size': '{}rem'.format(1.5*(res/1500)), "margin-bottom": "0px"})]
    ftp = {'State':"STNAME",'District':'NAME','Tehsil':'TAHSIL','Village':'VILLAGE'}
    if type == None:
        return header + [html.B(feature['properties'][ftp[ftype]],style={'font-size': '{}rem'.format(1.1*(res/1500))}),html.Br()] + \
                        ["Make a Selection"]
    return header + [html.B(feature['properties'][ftp[ftype]],style={'font-size': '{}rem'.format(1.1*(res/1500))}), html.Br(),
                     html.Plaintext("Month, year: {} {}".format(time,year),style={'font-size': '{}rem'.format(1.1*(res/1500)), "margin-top": "0px", "margin-bottom": "0px"}),
                     html.Plaintext("{}: {}".format(name_dict[type],feature['properties'][type+'_'+timef]),style={'font-size': '{}rem'.format(1.1*(res/1500)), "margin-top": "0px", "margin-bottom": "0px"})]

def get_graph(state,type,res=1500):
    yval = []
    xval = []
    zval = []
    col = {2019:'#6F359E',2020:'#F55475',2021:'#512A44'}
    typed = {'asset_tot_abs':'Asset Value','eway_tot':'E-Way Bills'}
    unit = {'asset_tot_abs':'in INR Crores','eway_tot':'in Lakhs'}
    if state is None:
        st = 'All India'
        dff = pd.DataFrame([])
        for yr in ['2019', '2020','2021']:
            df = dfdt[dfdt['year']==int(yr)].groupby(['month']).agg({type:sum})
            df = df.sort_index(ascending=True)
            df['month'] = [x.split('_')[0] for x in timeline[:len(df)]]
            df['year'] = col[int(yr)]
            dff = dff.append(df)
        df = dff.copy()
    else:
        st = state['properties']['STNAME']
        s = 1
    # df = pd.DataFrame([],columns=['month',type,'year'])
        for yr in ['2019','2020','2021']:
            for time in timeline:
                yval.append(time.split('_')[0])
                xval.append(state['properties'][type+'_'+time.split('_')[0]+'_'+yr[2:]])
                zval.append(col[int(yr)])

        df = pd.DataFrame({'month':yval,type:xval,'year':zval})

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[df['year']=='#6F359E']['month'],
            y=df[df['year']=='#6F359E'][type],
            mode='lines + markers',
            marker=dict(size=2),
            line=dict(color='#6F359E', width=2),
            name='2019',
            # config={'displayModeBar': False}
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df[df['year'] == '#F55475']['month'],
            y=df[df['year'] == '#F55475'][type],
            mode='lines + markers',
            marker=dict(size=2),
            line=dict(color='#F55475', width=2),
            name='2020'
            # orientation='h',
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df[df['year'] == col[2021]]['month'],
            y=df[df['year'] == col[2021]][type],
            mode='lines + markers',
            marker=dict(size=2),
            line=dict(color=col[2021], width=2),
            name='2021'
            # orientation='h',
        )
    )

    fig.update_layout(dict(
            title={'text':"<b>{}<br>Value of Goods Traded</b><br>(Total in INR per person)<br>  ".format(st),
                   'x':0,'y':0.9},
            # xaxis={'title': 'GST change (yoy,%)', 'automargin': True},
            hovermode='x unified',
            # config=dict(displayModeBar = False),
            height=250*(res/1500),
            width=350*(res/1500),
            font={'size':8*(res/1500)},
            margin=dict(l=20*(res/1500), r=10, t=65*(res/1500), b=30*(res/1500)),
            # autosize=True,
            # showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
    ))

    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)
    # graph = dcc.Graph(figure=figure)
    return fig

classes = [100000, 500000, 1000000, 5000000, 10000000, 50000000, 100000000, 200000000]
classes2 = [5000, 10000, 50000, 100000, 500000, 1000000, 5000000, 10000000]
classes3 = [5000, 10000, 20000, 50000, 100000, 200000, 400000, 1000000]
classes4 = [500, 1000, 2000, 4000, 6000, 8000, 10000, 15000]
cols = ["intra_eway", "intra_asset", "inter_out_eway", "inter_out_asset", "inter_in_eway", "inter_in_asset","asset_tot"]
classdict = {}
dfdt2 = dfdt[~dfdt.state_name.isin(["Dadra & Nagar Haveli","Daman & Diu"])].reset_index(drop=True)
for col in cols:
    classdict[col] = [int(x) for x in np.linspace(0,dfdt2[col].max(),8)]

classesf = [-280, -200, -120, -80, -40, -20, -10, -5, 0, 5, 10, 20, 40, 80, 120, 200, 280]
classesf2 = [-80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 40, 50, 60, 70,
             80]  # np.logspace(0,epfodt['Sep_20'].max(),8)
scale = ["{}".format(x) for x in classesf]
scale2 = ["{}".format(x) for x in classesf2]
# color = ["#ffffff","#ffe6e6","#ffcccc","#ffb3b3","#ff9999","#ff8080","#ff6666","#ff3333",'#e60000',"#990000"]
# # color.reverse()
# color2 = ["#e6ffe6","#ccffcc","#b3ffb3","#99ff99","#4dff4d","#1aff1a","#00e600","#00b300","#008000"]

color3wp = ['#E1CBF2','#BB99D6','#9567BA','#6F359E','#56257F','#3E1460','#320C51','#250441']
color3wb = ['#ccd5dc','#afbec9','#758fa2','#58788f','#3b617c','#1e4a69','#0f2b3f','#001829']
color3wb1 = ['#ade8f4','#90e0ef','#48cae4','#00b4d8','#0096c7','#0077b6','#023e8a','#03045e']
# colorscale = color+color24
# color3ry.reverse()
colorscale1 = color3wp
colorscale2 = color3wb1
# colorscale = ['#F8CAB4','#F6AF8E', '#EB5F1E', '#CE4E12', '#BC4710', '#96380D', '#83310B', '#5E2308', '#381505', '#260E03']
style1 = dict(weight=1, opacity=1, color='white', dashArray='3', fillOpacity=0.9)
stylet = dict(weight=1, opacity=1, color='white', dashArray='3', fillOpacity=0.0)
style2 = dict(weight=1, opacity=1, color='white', dashArray='3', fillOpacity=0.2)
style3 = dict(weight=0.6, opacity=1, color='white', dashArray='3', fillOpacity=0.1)
style4 = dict(weight=0.6, opacity=1, color='white', dashArray='3', fillOpacity=0.1)
ctg = scale.copy()
ctg2 = scale2.copy()
color_domain1 = dict(min=min(classdict["asset_tot"]), max=20000, colorscale=colorscale1)
color_domain2 = dict(min=min(classdict["asset_tot"]), max=max(classdict["asset_tot"]), colorscale=colorscale2)
colorbar = dlx.categorical_colorbar(categories=[str(x) for x in classdict["intra_asset"]], colorscale=colorscale1, width=250, height=15, position="bottomleft")


info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "100px", "right": "5px", "z-index": "900"})

title2 = html.Div(children=[html.H5("E-Way Bills")], id="mptitle2", className="mtitle",
                style={'font-family': 'Gilroy',"position": "absolute", "top": "9vh", "right": "5px", "z-index": "900"})
title = html.Div(children=[html.H5("Value of Goods Traded per Person")], id="mptitle", className="mtitle",
                style={"position": "absolute", "top": "9vh", "right": "5px", "z-index": "900"})

colorbar2 = dlx.categorical_colorbar(categories=[str(x) for x in classdict["intra_eway"]], colorscale=colorscale2, width=250, height=15, position="bottomleft")

colorbar = dl.Colorbar(width=200, height=20, **color_domain1, position="bottomleft",tickText=['0','10000','20000<b> INR</b>'])
colorbar2 = dl.Colorbar(width=200, height=20, **color_domain2, position="bottomleft")
info2 = html.Div(children=get_info2(), id="info2", className="info",
                style={"position": "absolute", "bottom": "130px", "right": "5px", "z-index": "900"})
# info2 = html.Div(children=get_info2(), id="info2", className="info",
#                 style={"position": "absolute", "bottom": "10px", "right": "10px", "z-index": "2000"})
labelname1 = html.Div(children=[html.B("INR",style={'font-size': '{}rem'.format(1.25),"margin-bottom": "0px"})],
                id = 'label1',style={"position": "absolute", "bottom": 44, "left": 195, "z-index": "1000","font-size": "1.5em"})
labelname2 = html.Div(children=[html.B('',style={'font-size': '{}rem'.format(1.25),"margin-bottom": "0px"})],
                id = 'label2',style={"position": "absolute", "bottom": "60px", "left": "900px", "z-index": "1000","font-size": "1.5em"})

image_filename = cwd + r'/' + r"assets/Final_Logo-01-2.png"
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

image_filename2 = cwd + r'/' + r"assets/isb_logo_transparent.png"
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())

"""**********************************************************************************************************************"""
# Load data
# df = pd.read_csv(DATA_PATH.joinpath("wellspublic.csv"), low_memory=False)
# df["Date_Well_Completed"] = pd.to_datetime(df["Date_Well_Completed"])
# df = df[df["Date_Well_Completed"] > dt.datetime(1960, 1, 1)]
#
# trim = df[["API_WellNo", "Well_Type", "Well_Name"]]
# trim.index = trim["API_WellNo"]
# dataset = trim.to_dict(orient="index")


# points = pickle.load(open(DATA_PATH.joinpath("points.pkl"), "rb"))

res=1500
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
    html.Div(id="output-clientside", style={'display': 'none'}),
    html.Div([
        html.Div([
                    html.Div(
                        [
                            html.Div([
                                    html.Div([
                                            html.H4("IndiaPulse@ISB",style={"margin-bottom": "0px"}),
                                            html.Hr(style={"margin-bottom": '2px', "margin-top": '2px'}),
                                            html.H5("V-shaped Recovery in Manufacturing", style={"margin-top": "0px"}),
                                        ])
                                    ],id="title"),

                        ],
                        className="pretty_container_head",
                        id="cross-filter-options",
                    ),

                    html.Div([
                        html.Hr(style={"margin-bottom": '2px', "margin-top": '2px'}),
                        html.Plaintext("Click on any state on the map to view",
                                       style={"color":"rgb(0,0,0,0)","margin-bottom": '0px',"margin-left":'10px','font-size': '{}rem'.format(1.3*(res/1500))}),
                        html.Div([
                            dcc.Graph(
                                id='linechart1',
                                figure={
                                'data': [],
                                'layout': dict(hovermode='closest',
                                               height='33vh',
                                               # handles multiple points landing on the same vertical,
                                               # automargin = True,
                                               margin=dict(l=10, r=10, t=10, b=10),
                                               # autosize=True,
                                               # showlegend = True,
                                               paper_bgcolor='transparent',
                                               plot_bgcolor='transparent',
                                               showgrid=False,
                                               xaxis={
                                                   'showgrid': False,  # thin lines in the background
                                                   'zeroline': False,  # thick line at x=0
                                                   'visible': False,  # numbers below
                                               },
                                               yaxis={
                                                   'showgrid': False,  # thin lines in the background
                                                   'zeroline': False,  # thick line at x=0
                                                   'visible': False,  # numbers below
                                               }
                                               )

                            },
                                # style={'height':'25vh'},
                            ),
                        ],
                        id='linechart1d',
                        style={'height':'33vh','display':'block'},
                        className="pretty_container_bar"
                        ),
                        html.Div([
                            dcc.Graph(
                                id='linechart2',
                                figure={
                                    'data': [],
                                    'layout': dict(hovermode='closest',
                                                   # height='40vh',
                                                   # handles multiple points landing on the same vertical,
                                                   # automargin = True,
                                                   margin=dict(l=10, r=10, t=10, b=10),
                                                   # autosize=True,
                                                   # showlegend = True,
                                                   paper_bgcolor='transparent',
                                                   plot_bgcolor='transparent',
                                                   showgrid=False,
                                                    xaxis= {
                                                        'showgrid': False, # thin lines in the background
                                                        'zeroline': False, # thick line at x=0
                                                        'visible': False,  # numbers below
                                                    },
                                                    yaxis= {
                                                        'showgrid': False, # thin lines in the background
                                                        'zeroline': False, # thick line at x=0
                                                        'visible': False,  # numbers below
                                                    }
                                                   ),


                                },

                            ),

                        ],
                        id='linechart2d',
                        style={'height':'20vh','display':'none'},
                        className="pretty_container_bar",
                        ),
                    ],
                    # id='linechart1d',
                    # style={'height':'25%'},
                    className="pretty_container_bar",

                    ),
                    html.Hr(style={"margin-bottom": '8px','margin-top':'20px'}),
                    html.Div(
                        [
                            html.Div(
                                html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                                         style={'height':'35px', 'width':'105px','align-items': 'left'}),
                                className="pretty_container_bar six columns",
                            ),
                            html.Div(
                                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                         style={'height':'35px', 'width':'140px','align-items': 'right'}),
                                className="pretty_container_bar six columns",
                            )

                        ],
                        className='row flex-display'
                    ),
                ],
            style={'height': '99vh'},
            className="pretty_container2 three columns",
        ),

        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        dl.Map(zoom=2, zoomSnap=0.25, zoomControl= False,
                               children=[
                                   dl.TileLayer(
                                       url='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}.png',
                                       minZoom=2),


                                   dl.GeoJSON(data=statesgeo, id="states", zoomToBounds=True,
                                              zoomToBoundsOnClick=False,
                                              options=dict(style=dlx.choropleth.style),
                                              hoverStyle=dict(weight=5, color='#666', dashArray=''),
                                              hideout=dict(colorscale=colorscale1, classes=classdict["intra_asset"], style=stylet,
                                                           color_prop='TOT_P')),
                                   dl.GeoJSON(data=[], id='districts', zoomToBounds=True, zoomToBoundsOnClick=False,
                                              options=dict(style=dlx.choropleth.style),
                                              hoverStyle=dict(weight=3, color='#555', dashArray=''),
                                              hideout=dict(colorscale=colorscale1, classes=classes2, style=style2,
                                                           color_prop='TOT_P')
                                              ),
                                   dl.GeoJSON(data=[], id='tehsils', zoomToBounds=True, zoomToBoundsOnClick=False,
                                              options=dict(style=dlx.choropleth.style),
                                              hoverStyle=dict(weight=1.5, color='#555', dashArray=''),
                                              hideout=dict(colorscale=colorscale1, classes=classes3, style=style3,
                                                           color_prop='TOT_P')
                                              ),
                                   dl.GeoJSON(data=[], id='villages', zoomToBounds=False, zoomToBoundsOnClick=True,
                                              options=dict(style=dlx.choropleth.style),
                                              hoverStyle=dict(weight=0.5, color='#555', dashArray=''),
                                              hideout=dict(colorscale=colorscale1, classes=classes4, style=style4,
                                                           color_prop='TOT_P')
                                              ),
                                   colorbar,
                                   info,
                                   # title,
                                   # labelname1
                                   # geobuf resource (fastest option)
                               ],
                               style={'height': '78vh',
                                      "display": "block"},
                               id="map-graph"),
                    ]),
                    html.Div([
                        html.Button(children=['Combined Value'], id='but-3', style=button_style_selected),
                        html.Button(children=['Value within State'], id='but-0', style=button_style),
                        html.Button(children=['Value Shipped out'], id='but-1', style=button_style),
                        html.Button(children=['Value Shipped in'], id='but-2', style=button_style),

                    ],
                        className="row flex-display"
                    )
                ],
                    className="pretty_container"),
            ],
            className="pretty_container",
            ),
            html.Div([
                        html.Div([
                            html.P(
                                "Use the time-slider to visualize the value of goods transacted per person in the year 2019,2020 & 2021",
                                className="control_label nine columns",
                            ),
                            html.Div([
                                html.Button(children=['2019'], id='but-4', style=button_style2),
                                html.Button(children=['2020'], id='but-5', style=button_style2),
                                html.Button(children=['2021'], id='but-6', style=button_style_selected2),
                            ],
                            className="row flex-display three columns",
                                style={'margin-left':'8vh'}
                            ),

                        ],
                        className="row flex-display"
                        ),
                        # html.P(
                        #     "Use the time-slider to visualize the value of goods transacted per person in the year 2020",
                        #     className="control_label",
                        # ),
                        dcc.Slider(
                            id="timeline",
                            min=0,
                            max=5,
                            step=None,
                            #'#0091CE'
                            marks={i: {'label': x.split('_')[0],'style': {'color': 'black'}} for i, x in enumerate(timeline) if i<11},
                            value=0,
                            updatemode='drag',
                        )
                    ],
                style={'height': '16vh', "display": "block"},
                className="pretty_container",
            ),
        ],
            style={'height': '99vh'},
            className="pretty_container2 nine columns",
        )
    ], id = "mainContainer",
       style={"display": "flex", "flex-direction": "row"},
    ),

    html.Div(id="hiddenState-div", style={'display': 'none'}),
    html.Div(id="hiddenDist-div", style={'display': 'none'}),
    html.Div(id="hiddenteh-div", style={'display': 'none'}),
    html.Div(id="StateDist-div", style={'display': 'none'}),
    html.Div(id="dataframe-div", style={'display': 'none'}),
    html.Div(id="reso-div", style={'display': 'none'}),
    html.Div(id="reso2-div", style={'display': 'none'}),
    html.Div(id="hid-button1", style={'display': 'none'}, children='but-3'),
    html.Div(id="hid-button2", style={'display': 'none'}, children='but-4'),
    html.Div(id="hid-year-button", style={'display': 'none'}, children='2021'),
    # html.Div(id="po_df-div", style={'display': 'none'}),
    # html.Div(id="select-level", style={'display': 'none'}),
    html.Div(id="click-event", style={'display': 'none'}),
    html.Div(id="select-event", style={'display': 'none'}),
],
    # id="mainContainer",
    # style={"display": "flex", "flex-direction": "column","overflow-y": "hidden"},
)

"""***********************************leaflet- CALLBACKS****************************"""

@app.callback(
    Output('timeline','marks'),
    [Input('timeline','value')])
def update_timelineStyle(time):
    # '#0091CE'
    color = ['black' if x!=time else '#0091CE' for x in range(12)]
    font = ['normal' if x!=time else 'bold' for x in range(12)]
    marks = {i: {'label': x.split('_')[0], 'style': {'color': color[i],'font-weight':font[i]}} for i, x in enumerate(timeline) if i < 12}
    return marks


@app.callback(
    [Output(f"but-{i}", "style") for i in range(4, 7)]+
    [Output('hid-year-button','children'),
     Output('timeline','max')
     # Output('label1', 'children')
     ],
    [Input(f"but-{i}", "n_clicks") for i in range(4, 7)]+
    [Input('timeline','value')],
)
def set_active(but1,but2,but3,time):
    user_call = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if user_call not in ['but-4','but-5','but-6']:
        raise PreventUpdate

    # get id of triggering button
    if user_call == 'but-6':
        maxm = 5
    else:
        maxm=11
    button_id = user_call
    year = button_dict[button_id]
    cblabel = [html.B('INR', style={'font-size': '{}rem'.format(1.25), "margin-bottom": "0px"})]
    print(button_id)
    return [button_style_selected2 if (button_id == f"but-{i}") else button_style2 for i in range(4,7)]+[year] + [maxm]


@app.callback(
    [Output(f"but-{i}", "style") for i in range(0, 4)]+
    [Output('hid-button1','children'),
     # Output('label1', 'children')
     ],
    [Input(f"but-{i}", "n_clicks") for i in range(0, 4)]+
    [Input('timeline','value')],
)
def set_active(but1,but2,but3,but4,time):
    user_call = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if user_call not in ['but-0','but-1','but-2','but-3']:
        raise PreventUpdate

    # get id of triggering button
    button_id = user_call
    cblabel = [html.B('INR', style={'font-size': '{}rem'.format(1.25), "margin-bottom": "0px"})]
    print(button_id)
    return [button_style_selected if (button_id == f"but-{i}") else button_style for i in range(0, 4)]+[button_id]



@app.callback(
    Output("info", "children"),
    # Output("info2", "children")],
    [Input("states", "hover_feature"),
     # Input("states2", "hover_feature"),
     # Input("tehsils", "hover_feature"),
     # Input("villages", "hover_feature")
     ],
    [State('timeline', 'value'),
     State('hid-button1', 'children'),
     State('hid-year-button', 'children')
     ])
def info_hover(feature_st, tval,button_id1,year):
    if button_id1 is None:
        print("None button")
        ctype1 = None
    else:
        print(button_id1)
        print(button_dict[button_id1])
        ctype1 = button_dict[button_id1]

    user_call = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    time = timeline[tval].split('_')[0]
    if user_call == 'states':
        # print(feature_st['properties'])
        return get_info(feature_st, 'State', ctype1, time,year)
    # elif user_call == 'states2':
    #     # if time == 'Dec_20':
    #     #     print("yes")
    #     return no_update, get_info2(feature_st2, 'State', ctype2, time)
    else:
        return no_update#, no_update
    # if user_call == 'tehsils':
    #     return get_info(feature_teh,'Tehsil')
    # if user_call == 'villages':
    #     return get_info(feature_vil,'Village')


@app.callback(#[
               Output('states', 'hideout'),
              [Input('timeline', 'value'),
               Input('hid-button1','children'),
               Input('hid-year-button','children')])
def update_map1(time,button_id,year):
    if time is None or button_id is None:
        raise PreventUpdate
    else:
        # time = timeline[time]
        sel = button_dict[button_id]
        print(button_id,sel)
        time = f"{sel}_{timeline[time].split('_')[0]}_{str(year[2:])}"#sel + '_' + timeline[time].split('_')[0]
        hideout = dict(colorscale=colorscale1, classes=classdict['asset_tot'], style=style1,
                       color_prop=time)
        return hideout#, dl.Tooltip('Click to view monthly figures')


@app.callback(
    [
     # Output('linechart1','figure'),
     # Output('linechart1','style'),
     Output('linechart1', 'figure'),
     Output('linechart1d', 'style')
     ],
    [Input('states','click_feature'),
     # Input('states2','click_feature')
     ],)
#     prevent_initial_call=True)
def update_state_bar(state):
    user_call = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if user_call is None:
        # return get_graph(None,'eway_tot'), {'display': 'block'}, get_graph(None,'asset_tot'), {'display': 'block'}
        return get_graph(None, 'asset_tot'), {'display': 'block'}
    if user_call == 'states':
        # return get_graph(state,'eway_tot'),{'display': 'block'}, get_graph(state,'asset_tot_abs'), {'display': 'block'}
        return get_graph(state, 'asset_tot'), {'display': 'block'}
    # elif user_call == 'states2':
    #     return get_graph(state2,'eway_tot'),{'display': 'block'}, get_graph(state2,'asset_tot'), {'display': 'block'}
    else:
        # return get_graph(None,'eway_tot'), {'display': 'block'}, get_graph(None,'asset_tot_abs'), {'display': 'block'}
        return get_graph(None, 'asset_tot'), {'display': 'block'}



# @app.callback(
#     Output('barchart2', 'figure'),
#     [Input('timeline', 'value')])
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
        df = df.sort_values(['gst'], ascending=True)

        figure = {
            'data': [
                go.Bar(
                    y=df['state'],
                    x=df['gst'],
                    orientation='h',
                    marker_color=df['color']
                )
            ],
            'layout': go.Layout(
                title=go.layout.Title(text="Percent Change 2019-20"),
                xaxis={'title': 'Percent Change in GST <br> (2019 to 2020)', 'automargin': True},
                hovermode='closest',
                height=630,
                # handles multiple points landing on the same vertical,
                # automargin = True,
                margin=dict(l=120, r=10, t=40, b=4),
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
#     app.run_server(debug=True, port=8057)
