#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from flask import Blueprint


from controllers.auth_security import *

from controllers.commun_equipe import *
from controllers.commun_etape import *


app = Flask(__name__)
app.secret_key = 'une cle(token)'


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


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

@app.route('/')
def show_accueil():
    equipes = get_equipes_in_nav()
    etapes = get_etapes_in_nav()

    return render_template('_layout.html', equipes=equipes, etapes=etapes)

@app.route('/carte-TDF-2023')
def show_carte_and_details_tdf():
    mycursor = get_db().cursor()

    mycursor.execute("SELECT SUM(longueur) AS nbKm FROM ETAPE;")
    total_km = mycursor.fetchone()

    mycursor.execute("SELECT id_etape, libelle_etape, date_etape, longueur, libelle_type_etape, CONCAT(nom_ville_depart,' > ',nom_ville_arrivee) AS villes "
                     "FROM ETAPE "
                     "INNER JOIN TYPE_ETAPE ON ETAPE.id_type_etape = TYPE_ETAPE.id_type_etape "
                     "INNER JOIN VILLE_DEPART ON ETAPE.id_ville_depart = VILLE_DEPART.id_ville_depart "
                     "INNER JOIN VILLE_ARRIVEE ON ETAPE.id_ville_arrivee = VILLE_ARRIVEE.id_ville_arrivee "
                     "ORDER BY id_etape;")

    all_etapes = mycursor.fetchall()

    mycursor.execute("SELECT id_repos, lieu_repos, date_repos FROM REPOS")
    repos = mycursor.fetchall()

    equipes = get_equipes_in_nav()
    etapes = get_etapes_in_nav()

    return render_template('show_carte.html', etapes=etapes, equipes=equipes, all_etapes=all_etapes, total_km=total_km, repos=repos)


##################
# Authentification
##################

# Middleware de sécurité

@app.before_request
def before_request():
     if request.path.startswith('/admin') or request.path.startswith('/commun'):
        if 'role' not in session:
            return redirect('/login')
        else:
            if (request.path.startswith('/commun') and session['role'] != 'ROLE_commun') or (request.path.startswith('/admin') and session['role'] != 'ROLE_admin'):
                print('pb de route : ', session['role'], request.path.title(), ' => deconnexion')
                session.pop('username', None)
                session.pop('role', None)
                return redirect('/login')
                #return redirect(url_for('auth_login'))


app.register_blueprint(auth_security)

# app.register_blueprint(commun_coureur)
# app.register_blueprint(commun_classement)
app.register_blueprint(commun_etape)
app.register_blueprint(commun_equipe)
#
# app.register_blueprint(admin_coureur)
# app.register_blueprint(admin_classement)
# app.register_blueprint(admin_etape)
# app.register_blueprint(admin_equipe)


if __name__ == '__main__':
    app.run(debug=True)

