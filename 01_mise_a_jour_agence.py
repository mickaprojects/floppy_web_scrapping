#!/usr/bin/env python
# -*- coding: cp1252 -*-


from selenium.webdriver.common.keys import Keys
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, uuid
from selenium.webdriver.common.action_chains import ActionChains
from distutils.version import StrictVersion
from numbers import Number
from configparser import ConfigParser
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from openpyxl.workbook import Workbook
import ast

from datetime import date
import time
import datetime
import sys
import os
import random
import glob
import re
import shutil
import traceback
import urlparse
import psycopg2
import psycopg2.extras

reload(sys)
sys.setdefaultencoding("cp1252")



def retour_valeur(tchamp, tvaleur, lib_champ):
    for l in range(len(lib_champ)):
        chp=lib_champ[l]
        for c in range(len(tchamp)):
            if tchamp[c].strip()==chp:
                return u""+tvaleur[c].strip()
    return ""

def libelle_couleur(liste_code, liste_couleur, code):
    for c in range(len(liste_code)):
        if liste_code[c]==code:
            return liste_couleur[c]
    return ""

def nz(valeur_o,valeur_pardefaut=''):
    if valeur_o=='' or valeur_o==None or valeur_o=='None':
        return valeur_pardefaut
    else:
        return valeur_o

def date2fr(sdateEn,sep="-"):
    a1=sdateEn[0:4]
    m1=sdateEn[5:7]
    d1=sdateEn[8:10]
    return d1+sep+m1+sep+a1

def retour_lignes_fichier(sfichier):
    if os.path.exists(r""+sfichier)==False:
        return ""
    with open(r""+sfichier, "r") as f :
        fichier_entier = f.read()
        if fichier_entier!="":
            lignes = fichier_entier.split("\n")
            return lignes
        else:
            return ""

def retour_chaine_nettoyee(chaine):
    chaine=chaine.encode("cp1252")
    ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç'.-,"
    ReplaceListeAccents = "EEEEAAAUUUIIOOCeeeeaaauuuiiooc    "
    k=0
    bchiffreaccepter=True
    while(k<len(chaine)):
        chainenew=chaine
        bok=False
        if bchiffreaccepter==True:
            if (ord(chainenew[k].upper())>= 65 and ord(chainenew[k].upper()) <= 90) or (ord(chainenew[k].upper()) >= 48 and ord(chainenew[k].upper()) <= 57) or ord(chainenew[k].upper()) == 32:
                bok=True
        else:
            if (ord(chainenew[k].upper())>= 65 and ord(chainenew[k].upper()) <= 90) or ord(chainenew[k].upper()) == 32:
                bok=True

        if bok==False:
            j=0
            btrouve=False
            while(j<len(ListeAccents)):
                if(ListeAccents[j]==chaine[k]):
                    chaine  = chaine.replace(chaine[k],ReplaceListeAccents[j])
                    btrouve=True
                    break
                j=j+1
            if btrouve==False:
                chaine  = chaine.replace(chaine[k]," ")

        k=k+1
    chaine = chaine.upper()
    chaine=ReplaceAllDoubleEspace(chaine)
    chaine=chaine.replace(" ","").strip()
    return chaine

def ReplaceAllDoubleEspace(chaine):
    newchaine = chaine
    while newchaine.find('  ') >= 0:
        newchaine = newchaine.replace('  ', ' ')
    return newchaine.lstrip().rstrip().lstrip()

def insertion(table,tzChamp,tzValue,connexion):
    """  Insertion des donnees dans une table;
        parametres:
            table : la table où on veut inserer les données
            tzChamp : les champs concernées par l'insértion (sous forme dde tableau)
            tzValue : les valeurs pour chaque element du tableau champ
            connexion : connexion d'acces à la table

    """
    if(len(tzChamp)==len(tzValue)):
        try:

            i=0
            j=0
            curs = connexion.cursor()
            curs.execute("SET client_encoding = 'WIN1252';")
            connexion.commit()
            sql = ""
            sql += "INSERT INTO \"" + table + "\"("
            while(i<len(tzChamp)):
                if i == len(tzChamp) - 1:
                    sql+= "\""+tzChamp[i]+"\""
                    i = i+1
                else:
                    sql+="\""+tzChamp[i]+"\","
                    i = i+1
            sql+=") VALUES("
            while(j<len(tzValue)):
                if tzValue[j]==None:
                    if j == len(tzValue)-1:
                        sql+=" null "
                        j = j+1
                    else:
                        sql+="null,"
                        j = j+1

                else:

                    if j == len(tzValue)-1:
                        sql+="'%s'" %(str(tzValue[j]).replace("'","''"),)
                        j = j+1
                    else:
                        sql+="'%s'," %(str(tzValue[j]).replace("'","''"),)
                        j = j+1
            sql+= ")"
            # print sql
            curs.execute(sql.encode("cp1252"))
            connexion.commit()
            return True
        except Exception as inst:
            msgs =  'type ERREUR78:'+str(type(inst))+'\n'     # the exception instance
            msgs+=  'CONTENU:'+str(inst)+'\n'           # __str__ allows args to printed directly
            print(msgs.encode("utf8"))
            return False

    else:
        print("Nombres des colonnes non identiques")
        return False

if os.path.exists("mise_a_jour_agence.lock")==False:
    try:
        lock=open("mise_a_jour_agence.lock", "a")
        lock.close()
        k = 0

        #09 12 2018 python27
        trace = open("trace_mise_a_jour_agence.txt", "w")
        trace.close()
        date_jour1 = str(date.today())
        date_jour=date2fr(date_jour1,"/")

        dbname="saisie"
        try:
            local      = psycopg2.connect("dbname="+dbname+" user=postgres password=123456  host= localhost")
            local.set_client_encoding('WIN1252')
            local.set_isolation_level(0)
            curlocal  = local.cursor(cursor_factory=psycopg2.extras.DictCursor);

        except :
            print("serveur introuvable")
            sys.exit(0)

        curlocal.execute("SET client_encoding = 'WIN1252';")
        local.commit()

        curlocal.execute("select distinct agence_nom, adresse from table_scrapping_immo where agence_nom is not null and trim(agence_nom)<>'' and adresse is not null and trim(adresse)<>'' ")
        t_liste=curlocal.fetchall()

        for enr in t_liste:
            cle=retour_chaine_nettoyee(enr[0].encode("cp1252", "ignore")).strip()+retour_chaine_nettoyee(enr[1].encode("cp1252", "ignore")).strip()
            curlocal.execute("select * from table_agence_atraiter where cle='"+cle+"'")
            t_search=curlocal.fetchall()
            if len(t_search)==0:
                insertion("table_agence_atraiter",["title_agence","adresse","cle"], [enr[0].encode("cp1252", "ignore"),enr[1].encode("cp1252", "ignore"),cle],local)

        trace = open("trace_mise_a_jour_agence.txt", "a")
        trace.write("FIN mise a jour agence !"+"\n")
        trace.close()

        #Suppression du fichier .lock
        if os.path.exists('mise_a_jour_agence.lock')==True:
            os.remove('mise_a_jour_agence.lock')

        sys.exit(0)
        # print("FIN Traitement recuperation donnees !")

    except Exception as inst:
        log=open(date_jour.replace("/", "-")+".txt", "a")
        traceback.print_exc(file=log)
        log.close()

        if os.path.exists('mise_a_jour_agence.lock')==True:
            os.remove('mise_a_jour_agence.lock')

        sys.exit(0)
