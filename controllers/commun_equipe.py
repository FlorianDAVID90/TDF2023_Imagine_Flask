#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash, session

from connexion_db import get_db

commun_equipe = Blueprint('commun_equipe', __name__,
                        template_folder='templates')

@commun_equipe.route('/equipe/<abrev>',methods=['GET'])
def show_equipe_details(abrev):
    mycursor = get_db().cursor()
    mycursor.execute("SELECT id_equipe FROM EQUIPE WHERE abrev_equipe = %s;", abrev)
    id_team = mycursor.fetchone()
    id = id_team['id_equipe']

    mycursor.execute("SELECT id_equipe, nom_equipe, abrev_equipe, img_equipe, img_maillot_equipe, nom_pays, drapeau_svg "
                     "FROM EQUIPE "
                     "INNER JOIN PAYS ON EQUIPE.id_pays = PAYS.id_pays "
                     "WHERE id_equipe = %s;", id)
    equipe = mycursor.fetchone()

    mycursor.execute("SELECT id_equipe, nom_equipe AS nom, abrev_equipe  FROM EQUIPE WHERE id_equipe = 1 ")
    first_equipe = mycursor.fetchone()

    mycursor.execute("SELECT nom_equipe AS nom, abrev_equipe FROM EQUIPE WHERE id_equipe = %s + 1", id)
    next_equipe = mycursor.fetchone()

    mycursor.execute("SELECT nom_equipe AS nom, abrev_equipe FROM EQUIPE WHERE id_equipe = %s - 1", id)
    prev_equipe = mycursor.fetchone()

    mycursor.execute("SELECT id_equipe, nom_equipe AS nom, abrev_equipe FROM EQUIPE WHERE id_equipe = (SELECT MAX(id_equipe) FROM EQUIPE);")
    last_equipe = mycursor.fetchone()

    mycursor.execute("SELECT id_coureur, CONCAT(prenom_coureur,' ',nom_coureur) AS coureur, date_naissance, nom_pays, img_coureur, drapeau_svg "
                     "FROM COUREUR "
                     "INNER JOIN EQUIPE ON COUREUR.id_equipe = EQUIPE.id_equipe "
                     "INNER JOIN PAYS on COUREUR.id_pays = PAYS.id_pays "
                     "WHERE EQUIPE.id_equipe = %s "
                     "GROUP BY id_coureur, coureur", id)
    coureurs = mycursor.fetchall()

    all_equipes = get_equipes_in_nav()
    all_etapes = get_etapes_in_nav()

    return render_template('commun/show_equipe.html', team=equipe, coureurs=coureurs, etapes=all_etapes, equipes=all_equipes,
                           first_equipe=first_equipe, prev_equipe=prev_equipe, next_equipe=next_equipe, last_equipe=last_equipe)

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