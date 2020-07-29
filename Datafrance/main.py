import dash
import dash_core_components as dcc 
import dash_html_components as html 
import plotly
import plotly.graph_objs as go 
from dash.dependencies import Input, Output
import dash_table
import pandas as pd 
import numpy as np 
import folium
import os
from operator import itemgetter
import base64

# Importer tous nos datasets
df = pd.read_csv("dataset\\liensVilles.csv", dtype='unicode')
df_auto = pd.read_csv("dataset\\auto.csv")
df_chomage = pd.read_csv("dataset\\chomage.csv")
df_csp = pd.read_csv("dataset\\csp.csv")
df_del = pd.read_csv("dataset\\delinquance.csv")
df_demo = pd.read_csv("dataset\\demographie.csv", dtype='unicode')
df_elections = pd.read_csv("dataset\\elections.csv", dtype='unicode')
df_emploi = pd.read_csv("dataset\\emploi.csv")
df_entreprises = pd.read_csv("dataset\\entreprises.csv")
df_immo = pd.read_csv("dataset\\immobilier.csv")
df_infos = pd.read_csv("dataset\\infos.csv", dtype='unicode')
df_salaires = pd.read_csv("dataset\\salaires.csv")
df_sante = pd.read_csv("dataset\\santeSocial.csv", dtype='unicode')
df_candidats = pd.read_csv("dataset\\candidats_2019.csv")

#dropdown ou liste deroulante
villes = [{"label": ville, "value": ville} for ville in df["ville"].unique()]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H4(" Choisisser une ville: "),
        dcc.Dropdown(
            id= "ville-picker",
            options= villes,
            value="Paris (75000)"
        )
    ], style={
        "width":"25%",
        "border":"1px solid #eee",
        "padding":"30px 30px 30px 120px",
        "box-shadow":"0 2px 2px #ccc",
        "display":"inline-block",
        "verticalAlign":"top"
    }),
    html.Div([
        dcc.Tabs(id = "tabs", value="tab-1", children=[
            #onglet infos generales
            dcc.Tab(label="Infos Générales", children= [
                html.Div([
                    html.H3("Infos Générales")
                ], style= {"background":"blue", "color":"white", "textAlign":"center", "padding":"10px 0px 10px 0px"}),
                html.Div([
                    dash_table.DataTable(
                        id = "table_infos",
                        style_cell = {"font-family" : "Montserrat"},
                        style_data_conditional = [
                            {
                                'if' : {'column_id' : 'intitule'},
                                'textAlign' : 'left'
                            }] + [
                            {
                                'if': {'row_index' : 'odd'},
                                'backgroundColor' : 'rgb(248, 248, 248)'
                            }
                        ],
                        style_header = {
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight' : 'bold'
                        }
                    )
                ], style= {'width':'40%','border':'1px solid #eee','box-shadow':'0 2px 2px #ccc', 'display':'inline-block', 
                            'verticalAlign' : 'top', 'padding' : '60px 30px 60px 30px'}),
                html.Div(id = "map", style= {'display':'inline-block','verticalAlign':'top','width':'50%', 
                                            'padding':'15px 0px 15px 10px'}),
            ]),
            #onglet Démographie
            dcc.Tab(label="Démographie", children= [
                html.H3("Population Française", style = {"background" : "blue", "color" : "white", "textAlign" : "center", 
                                                            "pading" : "10px 0px 10px 0px"}),
                html.Div([
                    dcc.Graph(id= "population")
                ], style= {"border" : "1px solid #eee", "box-shadow" : "0 2px 2px #ccc", "display" : "inline-block",
                            "verticalAlign" : "top", "width" : "45%", "pading" : "50px 0px 0px 50px"}),
                html.Div([
                    dcc.Graph(id= "naissance_deces")
                ], style= {"border" : "1px solid #eee", "box-shadow" : "0 2px 2px #ccc", "display" : "inline-block",
                            "verticalAlign" : "top", "width" : "45%", "pading" : "50px 0px 0px 50px"}),
                
                html.Div([
                    dcc.Graph(id= "hommes_femmes")
                ], style= {"display" : "inline-block", "verticalAlign":"top", "width":"35%"}),     
                html.Div([
                    dcc.Graph(id= "ages")
                ], style= {"display" : "inline-block", "verticalAlign":"top", "width":"35%"}),       
                html.Div([
                    dash_table.DataTable(
                        id= "repartitions",
                        style_cell = {"font-family" : "Montserrat"},
                        style_data_conditional = [
                            {
                                'if' : {'column_id' : 'intitule'},
                                'textAlign' : 'left'
                            }] + [
                            {
                                'if': {'row_index' : 'odd'},
                                'backgroundColor' : 'rgb(248, 248, 248)'
                            }
                        ],
                        style_header = {
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight' : 'bold'
                        }
                    )
                ], style= {"display" : "inline-block", "verticalAlign":"top", "width":"25%", "paddingTop":"50px"}), 
                html.Div([
                    dcc.Graph(id= "familles")
                ], style= {"display" : "inline-block", "verticalAlign":"top", "width":"35%"}),     
                html.Div([
                    dcc.Graph(id= "statut_marital")
                ], style= {"display" : "inline-block", "verticalAlign":"top", "width":"35%"}),       
                html.Div([
                    dash_table.DataTable(
                        id= "repartitions_2",
                        style_cell = {"font-family" : "Montserrat"},
                        style_data_conditional = [
                            {
                                'if' : {'column_id' : 'intitule'},
                                'textAlign' : 'left'
                            }] + [
                            {
                                'if': {'row_index' : 'odd'},
                                'backgroundColor' : 'rgb(248, 248, 248)'
                            }
                        ],
                        style_header = {
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight' : 'bold'
                        }
                    )
                ], style= {"display" : "inline-block", "verticalAlign":"top", "width":"25%", "paddingTop":"50px"}),        
                html.H3("Population étrangère", style = {"background":"blue", "color":"white", "textAlign":"center", 
                                                            "padding":"10px 0px 10p 0px"}),
                html.Div([
                    dcc.Graph(id= "evolution_etrangers")
                ], style= {"padding":"0px 240px 0px 240px"}),
                html.Div([
                    dcc.Graph(id= "repartition_etrangers_HF")
                ], style= {"display" : "inline-block", "verticalAlign":"top", "width":"35%"}),
                html.Div([
                    dcc.Graph(id= "repartition_etrangers_ages")
                ], style= {"display" : "inline-block", "verticalAlign":"top", "width":"35%"}),
                html.Div([
                    dash_table.DataTable(
                        id= "tableau_etrangers",
                        style_cell = {"font-family" : "Montserrat"},
                        style_data_conditional = [
                            {
                                'if' : {'column_id' : 'intitule'},
                                'textAlign' : 'left'
                            }] + [
                            {
                                'if': {'row_index' : 'odd'},
                                'backgroundColor' : 'rgb(248, 248, 248)'
                            }
                        ],
                        style_header = {
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight' : 'bold'
                        }
                    )
                ], style= {"display" : "inline-block", "verticalAlign":"top", "width":"25%", "paddingTop":"100px"}),
                html.H3("Population Immigrée", style = {"background":"blue", "color":"white", "textAlign":"center", 
                                                            "padding":"10px 0px 10p 0px"}),
                html.Div([
                    dcc.Graph(id= "evolution_immigres")
                ], style= {"padding":"0px 240px 0px 240px"}),        
                html.Div([
                    dcc.Graph(id= "repartition_immigres_HF")
                ], style= {"display" : "inline-block", "verticalAlign":"top", "width":"35%"}),
                html.Div([
                    dcc.Graph(id= "repartition_immigres_ages")
                ], style= {"display" : "inline-block", "verticalAlign":"top", "width":"35%"}),
                html.Div([
                    dash_table.DataTable(
                        id= "tableau_immigres",
                        style_cell = {"font-family" : "Montserrat"},
                        style_data_conditional = [
                            {
                                'if' : {'column_id' : 'intitule'},
                                'textAlign' : 'left'
                            }] + [
                            {
                                'if': {'row_index' : 'odd'},
                                'backgroundColor' : 'rgb(248, 248, 248)'
                            }
                        ],
                        style_header = {
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight' : 'bold'
                        }
                    )
                ], style= {"display" : "inline-block", "verticalAlign":"top", "width":"25%", "paddingTop":"100px"}),        
            ]),
            #onglet Sante et social
            dcc.Tab(label="Santé et social", children= [
                html.Div([
                    html.H1("Santé", style= {"background":"blue", "color":"white", "textAlign":"center", "padding":"10px 0px"}),
                    html.Div([
                        dcc.Graph(id = "practitiens")
                    ], style= {}),
                    html.Div([
                        dash_table.DataTable(
                            id= "tableau_practitiens"
                        )
                    ]),
                    html.Div([
                        dcc.Graph(id= "etablissements")
                    ]),
                    html.Div([
                        dash_table.DataTable(
                            id= "tableau_etablissements"
                        )
                    ])
                ]),
                html.Div([
                    html.H1("Social", style= {"background":"blue", "color":"white", "textAlign":"center", "padding":"10px 0px"}),
                    html.Div([
                        dcc.Graph(id = "caf")
                    ], style= {"border": "1px solid #eee", "box-shadow":"0 2px 2px #cc", "display":"inline-block", "width": "48%" }),
                    html.Div([
                        dcc.Graph(id = "rsa ")
                    ], style= {"border": "1px solid #eee", "box-shadow":"0 2px 2px #cc", "display":"inline-block", "width": "48%" }),
                    html.Div([
                        dcc.Graph(id = "apl")
                    ], style= {"border": "1px solid #eee", "box-shadow":"0 2px 2px #cc", "display":"inline-block", "width": "48%" }),
                    html.Div([
                        dcc.Graph(id = "alloc")
                    ], style= {"border": "1px solid #eee", "box-shadow":"0 2px 2px #cc", "display":"inline-block", "width": "48%" }),
                ])
            ]),
            #onglet Immobilier
            dcc.Tab(label="Immobilier"),
            #onglet Entreprise
            dcc.Tab(label="Entreprise"),
            #onglet Emplois
            dcc.Tab(label="Emplois"),
            #onglet Salaire
            dcc.Tab(label="Salaires"),
            #onglet CSP
            dcc.Tab(label="CSP"),
            #onglet Automobile
            dcc.Tab(label="Automobiles"),
            #onglet Délinquance
            dcc.Tab(label="Délinquance"),
            #onglet Européennes 2019
            dcc.Tab(label="Européennes 2019")
        ])

    ])

])


####### ONGLET INFOS GENERALE #########

# Afficher les infos générales
@app.callback([Output("table_infos","data"), Output("table_infos","columns")],
                [Input("ville-picker","value")])
def update_generales(ville_choisie):
    colonnes = df_infos.columns
    colonnes_off = ['Taux de chômage (2015)','Etablissement public de coopération intercommunale (EPCI)','lien',
                    'Unnamed: 0',"Pavillon bleu", "Ville d'art et d'histoire", 
                    "Ville fleurie", "Ville internet",'ville']
    listeInfos = [info for info in colonnes if info not in colonnes_off]
    infos = {
        "intitule": listeInfos,
        "donnee" : [df_infos[df_infos['ville'] == ville_choisie][col].iloc[0] for col in listeInfos]
    }

    table = pd.DataFrame(infos)
    data = table.to_dict("rows")

    entete = [{"id": "intitule", "name": "   "}, {"id": "donnee", "name": ville_choisie}]

    return data, entete

# Afficher la localisation sur une carte
@app.callback(Output("map", "children"), [Input("ville-picker", "value")])
def update_location(ville_choisie):
    longitude = df_infos[df_infos["ville"] == ville_choisie]["Longitude"].iloc[0]
    latitude = df_infos[df_infos["ville"] == ville_choisie]["Latitude"].iloc[0]

    carte= folium.Map(location= (latitude, longitude), zoom_start=7)
    marcker = folium.Marker(location = [latitude, longitude])
    marcker.add_to(carte)

    fichier = "locations\\localisation_" + ville_choisie + ".html"
    if not os.path.isfile(fichier):
        carte.save(fichier)

    return html.Iframe(srcDoc = open(fichier, "r").read(), width="100%", height= "600")



###### Onglet démographie ########
###### Population Française ######

# Afficher le graphe de la population
@app.callback(Output("population", "figure"), [Input("ville-picker", "value")])
def population_graph(ville_choisie):
    x_axis = np.array(range(2006,2016))
    y_axis = [
        df_demo[df_demo["ville"] == ville_choisie]["nbre habitants (" + str(annee) + ")"].iloc[0] for annee in range (2006,2016)
    ]

    ville_choisie = ville_choisie.split("(")[0].strip()

    traces = []
    traces.append(
        go.Scatter(
            x= x_axis,
            y= y_axis,
            mode= "lines+markers",
            line= {"shape" : "spline", "smoothing" : 1},            
        )
    )

    return {
        "data" : traces,
        "layout" : go.Layout(
            title = "Evolution de la population à " + ville_choisie,
            xaxis= {"title" : "<br>Années"},
            yaxis= dict(title ="Nombre d'habitants"),
            hovermode= "closest",
            legend_orientation= "h"


        )
    }

# Afficher l'evolution des naissances et des deces
@app.callback(Output("naissance_deces", "figure"), [Input("ville-picker", "value")])
def naissance_deces_graph(ville_choisie):
    x_axis = np.array(range(1999,2017))
    y_axis_naissance = [
        df_demo[df_demo["ville"] == ville_choisie]["nbre naissances (" + str(a) + ")"].iloc[0] for a in range(1999,2017)
    ]
    y_axis_deces = [
        df_demo[df_demo["ville"] == ville_choisie]["nbre deces (" + str(a) + ")"].iloc[0] for a in range(1999,2017)
    ]

    ville_choisie = ville_choisie.split("(")[0].strip()

    traces = [
        go.Scatter(
            x= x_axis,
            y= y_axis_naissance,
            mode= "lines+markers",
            line= {"shape" : "spline", "smoothing" :1},
            name= "Naissance à " + ville_choisie
        ),
        go.Scatter(
            x= x_axis,
            y= y_axis_deces,
            mode= "lines+markers",
            line= {"shape" : "spline", "smoothing" :1},
            name= "Deces à " + ville_choisie
        )
    ]

    return {
        "data" : traces,
        "layout" : go.Layout(
            title = "evolution des naissances et déces à " + ville_choisie,
            xaxis = {"title" : "<br>Années"},
            yaxis= dict(title ="Nombre de personnes"),
            hovermode= "closest",
            legend_orientation= "h"
            
        )
      
    }

# Afficher le camenbert repartition hommes/femmes
@app.callback(Output("hommes_femmes","figure"),[Input("ville-picker","value")])
def repartition_HF(ville_choisie):
    nb_hommes = df_demo[df_demo["ville"] == ville_choisie]["Hommes"].iloc[0]
    nb_femmes = df_demo[df_demo["ville"] == ville_choisie]["Femmes"].iloc[0]

    labels = ["Hommes", "Femmes"]
    values = [float(nb_hommes), float(nb_femmes)]
    total = sum(values)

    traces = [
        go.Pie(labels= labels, values= values)
    ]

    return{
        "data" : traces,
        "layout" : go.Layout(
            title= "Repartition Hommes/Femmes<br> (Total: " + str(total) + ")",
            legend_orientation= "h"

        ) 
    }

# Repartition par tranche d'age
@app.callback(Output("ages","figure"),[Input("ville-picker","value")])
def repartition_ages(ville_choisie):
    colonnes = ["Moins de 15 ans","15 - 29 ans","30 - 44 ans","45 - 59 ans","60 - 74 ans","75 ans et plus"]

    labels = colonnes
    values = [float(df_demo[df_demo["ville"] == ville_choisie][colonnes].iloc[0]) for colonnes in colonnes]
    total = sum(values)

    traces = [
        go.Pie(labels= labels, values= values)
    ]

    return{
        "data" : traces,
        "layout" : go.Layout(
            title= "Repartition par tranche d'ages<br> (Total: " + str(total) + ")",
            legend_orientation= "h"

        ) 
    }

# Tableau repartition hommes/femmes et tranches d'ages
@app.callback([Output("repartitions","data"), Output("repartitions","columns")], [Input("ville-picker","value")])
def table_repartitions(ville_choisie):
    colonnes = ["Hommes","Femmes","Moins de 15 ans","15 - 29 ans","30 - 44 ans","45 - 59 ans","60 - 74 ans","75 ans et plus"]

    infos = {
        "intitule" : colonnes, 
        "donnee" : [df_demo[df_demo["ville"] == ville_choisie][colonnes].iloc[0] for colonnes in colonnes]
    }
    table = pd.DataFrame(infos)
    data = table.to_dict("rows")

    entete = [{"id":"intitule", "name":"intitulé"}, {"id":"donnee", "name": ville_choisie.split("(")[0].strip()}]

    return data, entete

# Composition des familles
@app.callback (Output("familles", "figure"), [Input("ville-picker","value")])
def repartition_familles(ville_choisie):
    colonnes = ["Familles monoparentales","Couples sans enfant","Couples avec enfant",
                "Familles sans enfant","Familles avec un enfant","Familles avec deux enfants","Familles avec trois enfants",
                "Familles avec quatre enfants ou plus"]
    labels = colonnes
    values = [float(df_demo[df_demo["ville"] == ville_choisie][colonne].iloc[0]) for colonne in colonnes]
    total = sum(values)

    traces = [
        go.Pie(labels= labels, values= values)
    ]

    return {
        "data" : traces,
        "layout" : go.Layout(
            title= "Composition des familles<br> (Total " + str(total) + ")",
            legend_orientation = "h"
        )
    }

# Repartition du statut marital
@app.callback(Output("statut_marital","figure"), [Input("ville-picker","value")])
def repartition_statut_marital(ville_choisie):
    colonnes = ["Personnes célibataires","Personnes mariées","Personnes divorcées","Personnes veuves"]
    labels = colonnes
    values = [
        float(df_demo[df_demo["ville"] == ville_choisie][colonne].iloc[0]) for colonne in colonnes
    ]
    total = sum(values)
    traces= [
        go.Pie(labels= labels, values= values)
    ]
    
    return {
        "data": traces,
        "layout": go.Layout(
            title="Statuts Marital<br> (Total: " + str(total) + ")",
            legend_orientation= "h"

        )
    }
    
# Tableau 2 des répartitions
@app.callback([Output("repartitions_2","data"), Output("repartitions_2","columns")], [Input("ville-picker","value")])
def table_repartition_2(ville_choisie):
    colonnes = ["Familles monoparentales","Couples sans enfant","Couples avec enfant",
                "Familles sans enfant","Familles avec un enfant","Familles avec deux enfants","Familles avec trois enfants",
                "Familles avec quatre enfants ou plus","Personnes célibataires","Personnes mariées","Personnes divorcées",
                "Personnes veuves"]

    infos = {
        "intitule" : colonnes, 
        "donnee" : [df_demo[df_demo["ville"] == ville_choisie][colonnes].iloc[0] for colonnes in colonnes]
    }
    table = pd.DataFrame(infos)
    data = table.to_dict("rows")

    entete = [{"id":"intitule", "name":"intitulé"}, {"id":"donnee", "name": ville_choisie.split("(")[0].strip()}]

    return data, entete


####### Population étrangères ########

# Evolution Etranger et immigres 
@app.callback([Output("evolution_etrangers","figure"), Output("evolution_immigres", "figure")], [Input("ville-picker","value")])
def evolution_etrangers_immigres(ville_choisie):
    x_axis= np.array(range (2006,2016))
    y_axis_etranger= [df_demo[df_demo["ville"] == ville_choisie]["nbre étrangers (" + str(a) + ")"].iloc[0] for a in range(2006,2016)]
    y_axis_immigres= [df_demo[df_demo["ville"] == ville_choisie]["nbre immigrés (" + str(a) + ")"].iloc[0] for a in range(2006,2016)]

    ville_choisie = ville_choisie.split("(")[0].strip()

    traceEtrangers = [
        go.Scatter(
            x=x_axis,
            y=y_axis_etranger,
            mode="lines+markers",
            line= {"shape": "spline", "smoothing":1}
        )
    ]
    traceImmigres = [
        go.Scatter(
            x=x_axis,
            y=y_axis_immigres,
            mode="lines+markers",
            line= {"shape": "spline", "smoothing":1}
        )
    ]

    figureEtranger = {
        "data": traceEtrangers,
        "layout": go.Layout(
            title="Evolution de la population étrangère<br> à " + ville_choisie,
            xaxis= {"title": "Années"},
            yaxis= dict(title= "Nombre d'étrangers"),
            hovermode= "closest"
        )
    }

    figureImmigres = {
        "data": traceImmigres,
        "layout": go.Layout(
            title="Evolution de la population immigrés<br> à " + ville_choisie,
            xaxis= {"title": "Années"},
            yaxis= dict(title= "Nombre d'immigrés"),
            hovermode= "closest"
        )
    }

    return figureEtranger, figureImmigres
    
# Camenbert population HF etrangers
@app.callback(Output("repartition_etrangers_HF","figure"),[Input("ville-picker","value")])
def repartition_HF_Etrangers(ville_choisie):
    nb_hommes = df_demo[df_demo["ville"] == ville_choisie]["Hommes étrangers"].iloc[0]
    nb_femmes = df_demo[df_demo["ville"] == ville_choisie]["Femmes étrangères"].iloc[0]

    labels = ["Hommes étrangers", "Femmes étrangères"]
    values = [float(nb_hommes), float(nb_femmes)]
    total = sum(values)

    traces = [
        go.Pie(labels= labels, values= values)
    ]

    return{
        "data" : traces,
        "layout" : go.Layout(
            title= "Population étrangère | Hommes/Femmes<br> (Total: " + str(total) + ")",
            legend_orientation= "h"

        ) 
    }

# Camenbert Ages etrangers
@app.callback(Output("repartition_etrangers_ages","figure"),[Input("ville-picker","value")])
def repartition_etranger_ages(ville_choisie):
    colonnes = ["Moins de 15 ans étrangers","15-24 ans étrangers","25-54 ans étrangers","55 ans et plus étrangers"]

    labels = colonnes
    values = [float(df_demo[df_demo["ville"] == ville_choisie][colonnes].iloc[0]) for colonnes in colonnes]
    total = sum(values)

    traces = [
        go.Pie(labels= labels, values= values)
    ]

    return{
        "data" : traces,
        "layout" : go.Layout(
            title= "Repartition des étrangers par tranche d'ages<br> (Total: " + str(total) + ")",
            legend_orientation= "h"

        ) 
    }

# Tableau repartition etrangers
@app.callback([Output("tableau_etrangers","data"), Output("tableau_etrangers","columns")], [Input("ville-picker","value")])
def table_repartitions_etrangers(ville_choisie):
    colonnes = ["Hommes étrangers","Femmes étrangères","Moins de 15 ans étrangers",
                "15-24 ans étrangers","25-54 ans étrangers","55 ans et plus étrangers"]

    infos = {
        "intitule" : colonnes, 
        "donnee" : [df_demo[df_demo["ville"] == ville_choisie][colonnes].iloc[0] for colonnes in colonnes]
    }
    table = pd.DataFrame(infos)
    data = table.to_dict("rows")

    entete = [{"id":"intitule", "name":"intitulé"}, {"id":"donnee", "name": ville_choisie.split("(")[0].strip()}]

    return data, entete

####### Population immigrés ########

# Camenbert population HF immigres
@app.callback(Output("repartition_immigres_HF","figure"),[Input("ville-picker","value")])
def repartition_HF_Immigres(ville_choisie):
    nb_hommes = df_demo[df_demo["ville"] == ville_choisie]["Hommes immigrés"].iloc[0]
    nb_femmes = df_demo[df_demo["ville"] == ville_choisie]["Femmes immigrées"].iloc[0]

    labels = ["Hommes immigrés", "Femmes immigrées"]
    values = [float(nb_hommes), float(nb_femmes)]
    total = sum(values)

    traces = [
        go.Pie(labels= labels, values= values)
    ]

    return{
        "data" : traces,
        "layout" : go.Layout(
            title= "Population immigrée | Hommes/Femmes<br> (Total: " + str(total) + ")",
            legend_orientation= "h"

        ) 
    }

# Camenbert Ages immigres
@app.callback(Output("repartition_immigres_ages","figure"),[Input("ville-picker","value")])
def repartition_immigres_ages(ville_choisie):
    colonnes = ["Moins de 15 ans immigrés","15-24 ans immigrés","25-54 ans immigrés","55 ans et plus immigrés"]

    labels = colonnes
    values = [float(df_demo[df_demo["ville"] == ville_choisie][colonnes].iloc[0]) for colonnes in colonnes]
    total = sum(values)

    traces = [
        go.Pie(labels= labels, values= values)
    ]

    return{
        "data" : traces,
        "layout" : go.Layout(
            title= "Repartition des immigrés par tranche d'ages<br> (Total: " + str(total) + ")",
            legend_orientation= "h"

        ) 
    }

# Tableau repartition immigres
@app.callback([Output("tableau_immigres","data"), Output("tableau_immigres","columns")], [Input("ville-picker","value")])
def table_repartitions_immigress(ville_choisie):
    colonnes = ["Population immigrée","Hommes immigrés","Femmes immigrées","Moins de 15 ans immigrés",
                "15-24 ans immigrés","25-54 ans immigrés","55 ans et plus immigrés"]

    infos = {
        "intitule" : colonnes, 
        "donnee" : [df_demo[df_demo["ville"] == ville_choisie][colonnes].iloc[0] for colonnes in colonnes]
    }
    table = pd.DataFrame(infos)
    data = table.to_dict("rows")

    entete = [{"id":"intitule", "name":"intitulé"}, {"id":"donnee", "name": ville_choisie.split("(")[0].strip()}]

    return data, entete


############# SANTE ET SOCIAL ############







server = app.server

if __name__ == "__main__":
    app.run_server(debug = True)
