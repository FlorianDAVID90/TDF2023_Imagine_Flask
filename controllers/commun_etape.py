#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash, session

from connexion_db import get_db

commun_etape = Blueprint('commun_etape', __name__,
                        template_folder='templates')

@commun_etape.route('/etape/<int:id>',methods=['GET'])
def show_etape_details(id):
    etapes = get_etapes_in_nav()
    equipes = get_equipes_in_nav()

    mycursor = get_db().cursor()

    mycursor.execute("SELECT MIN(id_col) AS id FROM COL WHERE id_etape = %s;",id)
    min_col_id = mycursor.fetchone()

    mycursor.execute(
        "SELECT id_etape, libelle_etape, date_etape, longueur, libelle_type_etape,"
        "UPPER(CONCAT(nom_ville_depart,' > ',nom_ville_arrivee)) AS villes, descriptif1, descriptif2, descriptif3 "
        "FROM ETAPE "
        "INNER JOIN TYPE_ETAPE ON ETAPE.id_type_etape = TYPE_ETAPE.id_type_etape "
        "INNER JOIN VILLE_DEPART ON ETAPE.id_ville_depart = VILLE_DEPART.id_ville_depart "
        "INNER JOIN VILLE_ARRIVEE ON ETAPE.id_ville_arrivee = VILLE_ARRIVEE.id_ville_arrivee "
        "WHERE id_etape = %s;", id)

    etape = mycursor.fetchone()

    mycursor.execute("SELECT id_col, cat_col, nom_col, nb_km, poucentage_moyen, altitude, situation_km, img_profil_col "
                     "FROM COL "
                     "WHERE id_etape = %s;", id)

    cols = mycursor.fetchall()
    return render_template('commun/show_etape.html', etape=etape, cols=cols, etapes=etapes, equipes=equipes, min_col_id=min_col_id)

def get_equipes_in_nav():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT id_equipe, nom_equipe, abrev_equipe, img_maillot_equipe FROM EQUIPE ORDER BY id_equipe")
    equipes = mycursor.fetchall()

    return equipes


def get_etapes_in_nav():
    mycursor = get_db().cursor()
    mycursor.execute(
        "SELECT id_etape, libelle_etape, date_etape, longueur, libelle_type_etape, UPPER(CONCAT(nom_ville_depart,' > ',nom_ville_arrivee)) AS villes "
        "FROM ETAPE "
        "INNER JOIN TYPE_ETAPE ON ETAPE.id_type_etape = TYPE_ETAPE.id_type_etape "
        "INNER JOIN VILLE_DEPART ON ETAPE.id_ville_depart = VILLE_DEPART.id_ville_depart "
        "INNER JOIN VILLE_ARRIVEE ON ETAPE.id_ville_arrivee = VILLE_ARRIVEE.id_ville_arrivee "
        "ORDER BY id_etape;")
    etapes = mycursor.fetchall()

    return etapes