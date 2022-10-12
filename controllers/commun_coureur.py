#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connexion_db import get_db

commun_coureur = Blueprint('commun_coureur', __name__,
                        template_folder='templates')

@commun_coureur.route('/coureur/<int:id>',methods=['GET'])
def show_coureur_details(id):
    mycursor = get_db().cursor()

    mycursor.execute("SELECT * FROM COUREUR WHERE id_coureur = %s;", id)
    coureur = mycursor.fetchone()
    return render_template('commun/show_coureur.html', coureur=coureur)