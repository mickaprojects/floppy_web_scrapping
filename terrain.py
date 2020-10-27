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
from bs4 import BeautifulSoup

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

def isnumerique(chaine):
    """Fonction de test qui renvoie True si une chaine est entierement numerique"""
    i=0
    result = True
    while (i<len(chaine)):
        if chaine[i] not in "0123456789":
            result = False
            return result
        i= i+1
    return result

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

def nettoye3(chaine):
    chaine=chaine.replace("\t"," ").replace("\n"," ").replace("  "," ").strip().strip("\t").strip("\n")
    if str(chaine).find(" m")!=-1:
        chaine=str(chaine).replace(" m","")
    return chaine

def nettoye(chaine):
    chaine=chaine.replace("\t"," ").replace("\n"," ").replace("  "," ").strip().strip("\t").strip("\n")
    if str(chaine).find(" m²".encode("cp1252"))!=-1:
        chaine=str(chaine).replace(" m²".encode("cp1252"),"")
    if str(chaine).find(" m2".encode("cp1252"))!=-1:
        chaine=str(chaine).replace(" m2".encode("cp1252"),"")
    if str(chaine).find(" kWh/m2")!=-1:
        chaine=str(chaine).replace(" kWh/m2","")
    if str(chaine).find(" kg CO2/m2")!=-1:
        chaine=str(chaine).replace(" kg CO2/m2","")
    if str(chaine).find(" kWh/an")!=-1:
        chaine=str(chaine).replace(" kWh/an","")
    if str(chaine).find(" €/mois".encode("cp1252"))!=-1:
        chaine=str(chaine).replace(" €/mois".encode("cp1252"),"")
    if str(chaine).find(" €".encode("cp1252"))!=-1:
        chaine=str(chaine).replace(" €".encode("cp1252"),"")

    return chaine

def nettoye2(chaine):
    chaine=chaine.replace("\t"," ").replace("\n"," ").replace("  "," ").strip().strip("\t").strip("\n")
    if str(chaine).find(" m²".encode("cp1252"))!=-1:
        chaine=str(chaine).replace(" m²".encode("cp1252"),"")
    if str(chaine).find(" m2".encode("cp1252"))!=-1:
        chaine=str(chaine).replace(" m2".encode("cp1252"),"")
    if str(chaine).find(" €".encode("cp1252"))!=-1:
        chaine=str(chaine).replace(" €".encode("cp1252"),"")
    if str(chaine).find(" kWh/m2")!=-1:
        chaine=str(chaine).replace(" kWh/m2","")
    if str(chaine).find(" kg CO2/m2")!=-1:
        chaine=str(chaine).replace(" kg CO2/m2","")
    if str(chaine).find("n°".encode("cp1252"))!=-1:
        chaine=str(chaine).replace("n°".encode("cp1252"),"")
    return chaine

def nettoye4(chaine):
    chaine=chaine.replace("\t"," ").replace("\n"," ").replace("  "," ").strip().strip("\t").strip("\n")
    if str(chaine).find("m²".encode("cp1252"))!=-1:
        chaine=str(chaine).replace("m²".encode("cp1252"),"")
    return chaine

def nettoye_m(chaine):
    chaine=chaine.replace("\t"," ").replace("\n"," ").replace("  "," ").strip().strip("\t").strip("\n")
    if str(chaine).find(" m")!=-1:
        chaine=str(chaine).replace(" m","")
    return chaine

def ReplaceAllDoubleEspace(chaine):
    newchaine = chaine
    while newchaine.find('  ') >= 0:
        newchaine = newchaine.replace('  ', ' ')
    return newchaine.lstrip().rstrip().lstrip()

def ReplaceAllTab(chaine):
    newchaine = chaine
    while newchaine.find('\t') >= 0:
        newchaine = newchaine.replace('\t', ' ')
    return newchaine.lstrip().rstrip().lstrip()

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



if os.path.exists("terrain.lock")==False:
    try:
        lock=open("terrain.lock", "a")
        lock.close()
        k = 0

        #31 12 2018 python27
        trace = open("trace_terrain.txt", "w")
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

        nom_parametre = r"" + "parametres.ini"
        if (os.access(nom_parametre, os.F_OK) == False):
            trace = open("trace_terrain.txt", "a")
            trace.write("Le fichier parametres.ini est introuvable !\n")
            trace.close()
            # print("Le fichier parametres.ini est introuvable !")
            sys.exit(0)

        config = ConfigParser()
        config.read(nom_parametre)
        traitement = config.get('parametre', 'traitement')
        temps_recherche = int(config.get('parametre', 'temps_recherche'))

        temps_affichage_resultat = int(config.get('parametre', 'temps_affichage_resultat'))
        scroll = int(config.get('parametre', 'scroll'))
        scroll_element = int(config.get('parametre', 'scroll_element'))
        scroll_debut = int(config.get('parametre', 'scroll_debut'))

        temps_affichage_page_suivante = int(config.get('parametre', 'temps_affichage_page_suivante'))
        temps_affichage_tel = int(config.get('parametre', 'temps_affichage_tel'))
        temps_affichage_element = int(config.get('parametre', 'temps_affichage_element'))

        cle="a_vendre"

        lien = config.get(cle, 'lien')
        # categorie = config.get(cle, 'categorie')
        categorie=""
        rep="resultats"
        if(os.access(rep,os.F_OK)==False):
            os.makedirs(rep,777)

        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--start-maximized")

        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": "", # IMPORTANT - ENDING SLASH V IMPORTANT
                 "directory_upgrade": True, "extensions_to_open": "", "plugins.plugins_disabled": ["Chrome PDF Viewer"], "plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}]}

        chromeOptions.add_experimental_option("prefs",prefs)
        chromeOptions.add_argument("--disable-print-preview")
        chromedriver = r"chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

        driver.implicitly_wait(temps_recherche)

        wait = ui.WebDriverWait(driver,temps_recherche)


        date_=datetime.datetime.now().strftime("%Y%m%d %H%M%S")
        date2_=datetime.datetime.now().strftime("%Y%m%d")
        y=0

        curlocal.execute("select * from table_recup_liste_a_vendre where (bien='Terrains' or bien='Garages' or categorie = 'construire' or categorie='vacance' or (categorie='agence' and (position('emplacement' in lower(designation))>0 or position('terrain' in lower(designation))>0 or position('garage' in lower(designation))>0 or position('construire' in lower(designation))>0 or position('vacance' in lower(designation))>0))) and traite='n'")
        t=curlocal.fetchall()
        z=0
        for enr in t:
            z=z+1

            driver.get(enr["href"])

            driver.maximize_window()

            driver.execute_script("window.scrollTo(0, "+str(scroll_element)+");")
            #adresse
            adresse=""
            cp=""
            ville=""
            num_voie=""
            prix=""
            bien=enr["bien"]
            categorie=enr["categorie"]
            designation=enr["designation"]
            page1=enr["page"]
            lien_photo=enr["lien_photo"]
            lien_url=enr["href"]

            s_script0="return $('#column-central').html()"
            html0=driver.execute_script(s_script0)
            soup0=BeautifulSoup(html0, "lxml")

            adresse=""
            surface=""
            try:
                e2=soup0.find(lambda tag:tag.name=="h1" and "Terrain à bâtir" in tag.text)
                # e2=soup0.find("h1", string="Terrain à bâtir")
                element_terrain_liste=e2.contents
                for l in element_terrain_liste:
                    if l.find("superficie de ")!=-1:
                        pos1=l.find("superficie de ")
                        if pos1!=None:
                            surface=nettoye4(l[pos1+len("superficie de "):])
                    # elif l.find(u"à vendre ")!=-1:
                    #     l1=l.split("\n\t")
                    #     for l2 in l1:
                    #         if l2.find(u"à vendre - ")!=-1:
                    #             adresse=l2.replace(u"à vendre - ","").strip()
                    #             break
                    #         elif l2.find(u"à vendre ")!=-1:
                    #             adresse=l2.replace(u"à vendre ","").strip()
                    #             break

            except:
                pass

            prix=""
            try:
                element_prix=soup0.select("li.pricefont span.price")
                if categorie=="vacance":
                    prix=element_prix[0].text.strip()
                    prix=prix.replace("€".encode("cp1252"), "€ ".encode("cp1252"))
                    prix=prix.replace("\t"," ")
                else:
                    prix=nettoye(element_prix[0].text)
            except:
                pass
            if prix=="":
                try:
                    element_prix=soup0.select("li.pricefont")
                    if categorie=="vacance":
                        prix=element_prix[0].text.strip()
                        prix=prix.replace("€".encode("cp1252"), "€ ".encode("cp1252"))
                        prix=prix.replace("\t"," ")
                    else:
                        prix=nettoye(element_prix[0].text)
                except:
                    pass

            profondeur_terrain=""
            for c in ["Profondeur:","Profondeur ="]:
                try:
                    if profondeur_terrain!="":
                        break
                    e2=soup0.find(lambda tag:tag.name=="div" and c in tag.text)
                    s2=e2.text
                    pos4=s2.find(c)
                    pos5=0
                    if pos4!=-1:
                        pos5=pos4+len(c)
                        s3=s2[pos5:]
                        if s3.find("m")!=-1:
                            pos6=s3.find("m")
                            profondeur_terrain=nettoye_m(s3[0:pos6])
                except:
                    pass

            #ajout 12 02 2019
            hauteur_entree=""
            for c in ["Hauteur entrée:","Hauteur entrée ="]:
                try:
                    if hauteur_entree!="":
                        break
                    e2=soup0.find(lambda tag:tag.name=="div" and c in tag.text)
                    s2=e2.text
                    pos4=s2.find(c)
                    pos5=0
                    if pos4!=-1:
                        pos5=pos4+len(c)
                        s3=s2[pos5:]
                        if s3.find("m")!=-1:
                            pos6=s3.find("m")
                            hauteur_entree=nettoye_m(s3[0:pos6])
                except:
                    pass

            largeur_porte=""
            for c in ["Largeur porte:","Largeur porte ="]:
                try:
                    if largeur_porte!="":
                        break
                    e2=soup0.find(lambda tag:tag.name=="div" and c in tag.text)
                    s2=e2.text
                    pos4=s2.find(c)
                    pos5=0
                    if pos4!=-1:
                        pos5=pos4+len(c)
                        s3=s2[pos5:]
                        if s3.find("m")!=-1:
                            pos6=s3.find("m")
                            largeur_porte=nettoye_m(s3[0:pos6])
                except:
                    pass

            largeur_interieur=""
            for c in ["Largeur intérieur:","Largeur intérieur ="]:
                try:
                    if largeur_interieur!="":
                        break
                    e2=soup0.find(lambda tag:tag.name=="div" and c in tag.text)
                    s2=e2.text
                    pos4=s2.find(c)
                    pos5=0
                    if pos4!=-1:
                        pos5=pos4+len(c)
                        s3=s2[pos5:]
                        if s3.find("m")!=-1:
                            pos6=s3.find("m")
                            largeur_interieur=nettoye_m(s3[0:pos6])
                except:
                    pass

            largeur=""
            for c in ["Largeur:","Largeur ="]:
                try:
                    if largeur!="":
                        break
                    e2=soup0.find(lambda tag:tag.name=="div" and c in tag.text)
                    s2=e2.text
                    pos4=s2.find(c)
                    pos5=0
                    if pos4!=-1:
                        pos5=pos4+len(c)
                        s3=s2[pos5:]
                        if s3.find("m")!=-1:
                            pos6=s3.find("m")
                            largeur=nettoye_m(s3[0:pos6])
                except:
                    pass

            hauteur=""
            for c in ["Hauteur:","Hauteur ="]:
                try:
                    if hauteur!="":
                        break
                    e2=soup0.find(lambda tag:tag.name=="div" and c in tag.text)
                    s2=e2.text
                    pos4=s2.find(c)
                    pos5=0
                    if pos4!=-1:
                        pos5=pos4+len(c)
                        s3=s2[pos5:]
                        if s3.find("m")!=-1:
                            pos6=s3.find("m")
                            hauteur=nettoye_m(s3[0:pos6])
                except:
                    pass

            #--------------------------------

            s_script2="return $('.locationdescription').html()"
            html2=driver.execute_script(s_script2)
            soup2=BeautifulSoup(html2, "lxml")
            chambre=""
            try:
                e2=soup2.find(lambda tag:tag.name=="li" and "chambres" in tag.text)
                l3=e2.text.replace("chambres","")
                chambre=nettoye(l3)
            except:
                pass

            #ajout 15 02 2019 12:50
            nombre_personnes=""
            try:
                e2=soup2.find(lambda tag:tag.name=="li" and " personne" in tag.text)
                l3=e2.text.replace(" personnes","").replace(" personne","").replace("De ","")
                nombre_personnes=nettoye(l3)
            except:
                pass
            #----------------------

            nom_immeuble=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Nom de la résidence / de l'immeuble " in tag.text)
                l3=e2.text.split(" : ")
                nom_immeuble=nettoye(l3[1])
            except:
                pass

            surface_habitable=""
            try:
                e2=soup0.find(lambda tag:tag.name=="li" and "surface habitable de " in tag.text)
                l3=e2.text.replace("surface habitable de ","")
                surface_habitable=nettoye(l3)
            except:
                pass

            #ajout 15 02 2019
            architecture_contemporain=""
            try:
                e2=soup0.find(lambda tag:tag.name=="li" and "Architecture contemporain" in tag.text)
                if nz(e2.text)!="":
                    architecture_contemporain="oui"
            except:
                pass

            maconnerie_traditionnelle=""
            try:
                e2=soup0.find(lambda tag:tag.name=="li" and "Maçonnerie traditionnelle" in tag.text)
                if nz(e2.text)!="":
                    maconnerie_traditionnelle="oui"
            except:
                pass
            #---------------

            #ajout 10 02 2019
            prix_au_m2=""
            try:
                e2=soup0.find(lambda tag:tag.name=="li" and "Prix au m² " in tag.text)
                l3=e2.text.split(" : ")
                prix_au_m2=nettoye(l3[1])
            except:
                pass

            if surface=="":
                try:
                    e2=soup0.find(lambda tag:tag.name=="li" and "Terrain de " in tag.text)
                    surface=nettoye(e2.text.replace("Terrain de ",""))
                except:
                    pass

            if surface=="":
                try:
                    e2=soup0.find(lambda tag:tag.name=="p" and "Terrain  :" in tag.text)
                    surface=nettoye(e2.text.replace("Terrain  :",""))
                except:
                    pass

            surface_constructible=""
            try:
                e2=soup0.find(lambda tag:tag.name=="li" and "surface constructible de " in tag.text)
                surface_constructible=nettoye(e2.text.replace("surface constructible de ",""))
            except:
                pass
            #------------
            try:
                element_adresse=soup0.select("ul.locationinfo span li")
                element_adresse2=element_adresse[0].contents
                adr=""
                for a in element_adresse2:
                    try:
                        tag_name=a.name
                        if tag_name==None:
                            adr=adr+" "+a
                    except:
                        pass
                adresse_avant=nettoye(adr)
                num_voie1=adresse_avant.split(" ")[0].strip()
                num_voie11=adresse_avant.split(" ")[0].strip().replace(",","")
                v2=adresse_avant.split(" ")
                num_voie2=v2[len(v2)-1].strip()
                num_voie22=v2[len(v2)-1].strip().replace(",","")
                if isnumerique(num_voie11):
                    num_voie=num_voie11
                    adresse=adresse_avant.replace(num_voie1+" ","")
                elif isnumerique(num_voie22):
                    num_voie=num_voie22
                    adresse=adresse_avant.replace(" "+num_voie2,"")
                else:
                    adresse=adresse_avant

                num_voie=num_voie.replace("\t"," ")
                adresse=adresse.replace("\t"," ")
                element_adresse3=element_adresse[1].contents
                adr=""
                for a in element_adresse3:
                    try:
                        tag_name=a.name
                        if tag_name==None:
                            adr=adr+" "+a
                    except:
                        pass
                adresse_apres=nettoye(adr)
                cp=adresse_apres.split(" - ")[0].strip()
                ville=adresse_apres.split(" - ")[1].strip()

            except:
                pass

            #ajout 10 02 2019
            libre_le=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Libre le " in tag.text)
                l3=e2.text.split(" : ")
                libre_le=nettoye_m(l3[1])
            except:
                pass
            #---------------

            largeur_facade_rue=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Largeur façade à rue " in tag.text)
                l3=e2.text.split(" : ")
                largeur_facade_rue=nettoye(l3[1])
                largeur_facade_rue=largeur_facade_rue.replace(" m","")
            except:
                pass

            #ajout 15 02 2019
            delai_de_construction=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Délai de construction " in tag.text)
                l3=e2.text.split(" : ")
                delai_de_construction=nettoye(l3[1])
            except:
                pass
            #---------------

            nombre_facade=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Nombre de façades " in tag.text)
                l3=e2.text.split(" : ")
                nombre_facade=nettoye(l3[1])
            except:
                pass

            nombre_etage=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Nombre d'étages " in tag.text)
                l3=e2.text.split(" : ")
                nombre_etage=nettoye(l3[1])
            except:
                pass

            teledistribution=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Télédistribution" in tag.text)
                if nz(e2.text)!="":
                    teledistribution="oui"
            except:
                pass

            parking_exterieur=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Parkings extérieurs " in tag.text)
                l3=e2.text.split(" : ")
                parking_exterieur=nettoye(l3[1])
            except:
                pass

            #ajout 15 02 2019
            bord_de_mer_lac=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Bord de mer/lac" in tag.text)
                if nz(e2.text)!="":
                    bord_de_mer_lac="oui"
            except:
                pass

            dans_la_verdure=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Dans la verdure" in tag.text)
                if nz(e2.text)!="":
                    dans_la_verdure="oui"
            except:
                pass

            piscine=""
            try:
                texte2="Piscine:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                piscine=e2.text.replace(texte2,"").strip()
                piscine=piscine.replace("\t"," ")
            except:
                pass

            if piscine=="":
                try:
                    e2=soup0.find(lambda tag:tag.name=="p" and "Piscine" in tag.text)
                    if nz(e2.text)!="":
                        piscine="oui"
                except:
                    pass

            barbecue=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Barbecue" in tag.text)
                if nz(e2.text)!="":
                    barbecue="oui"
            except:
                pass

            jacuzzi=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Jacuzzi" in tag.text)
                if nz(e2.text)!="":
                    jacuzzi="oui"
            except:
                pass

            sauna=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Sauna" in tag.text)
                if nz(e2.text)!="":
                    sauna="oui"
            except:
                pass

            frigo=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Frigo" in tag.text)
                if nz(e2.text)!="":
                    frigo="oui"
            except:
                pass

            congelateur=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Congélateur" in tag.text)
                if nz(e2.text)!="":
                    congelateur="oui"
            except:
                pass

            micro_ondes=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Micro-ondes" in tag.text)
                if nz(e2.text)!="":
                    micro_ondes="oui"
            except:
                pass

            connexion_internet=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Connexion internet" in tag.text)
                if nz(e2.text)!="":
                    connexion_internet="oui"
            except:
                pass

            caution_garantie_locative=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Caution-garantie locative " in tag.text)
                l3=e2.text.split(" : ")
                caution_garantie_locative=nettoye(l3[1])
            except:
                pass

            acompte_en_pourcentage_du_loyer=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Acompte en % du 'loyer' " in tag.text)
                l3=e2.text.split(" : ")
                acompte_en_pourcentage_du_loyer=nettoye(l3[1])
            except:
                pass

            frais_de_dossier=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Frais de dossier " in tag.text)
                l3=e2.text.split(" : ")
                frais_de_dossier=nettoye(l3[1])
            except:
                pass

            golf=""
            try:
                texte2="Golf:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                golf=e2.text.replace(texte2,"").strip()
                golf=golf.replace("\t"," ")
            except:
                pass

            mer=""
            try:
                texte2="Mer:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                mer=e2.text.replace(texte2,"").strip()
                mer=mer.replace("\t"," ")
            except:
                pass

            gare=""
            try:
                texte2="Gare:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                gare=e2.text.replace(texte2,"").strip()
                gare=gare.replace("\t"," ")
            except:
                pass

            aeroport=""
            try:
                texte2="Aéroport:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                aeroport=e2.text.replace(texte2,"").strip()
                aeroport=aeroport.replace("\t"," ")
            except:
                pass

            office_du_tourisme=""
            try:
                texte2="Office du tourisme:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                office_du_tourisme=e2.text.replace(texte2,"").strip()
                office_du_tourisme=office_du_tourisme.replace("\t"," ")
            except:
                pass

            marches=""
            try:
                texte2="Marchés:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                marches=e2.text.replace(texte2,"").strip()
                marches=marches.replace("\t"," ")
            except:
                pass

            magasins=""
            try:
                texte2="Magasins:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                magasins=e2.text.replace(texte2,"").strip()
                magasins=magasins.replace("\t"," ")
            except:
                pass

            grandes_villes=""
            try:
                texte2="Grandes villes:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                grandes_villes=e2.text.replace(texte2,"").strip()
                grandes_villes=grandes_villes.replace("\t"," ")
            except:
                pass

            vtt=""
            try:
                texte2="VTT:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                vtt=e2.text.replace(texte2,"").strip()
                vtt=vtt.replace("\t"," ")
            except:
                pass

            bowling=""
            try:
                texte2="Bowling:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                bowling=e2.text.replace(texte2,"").strip()
                bowling=bowling.replace("\t"," ")
            except:
                pass

            casino=""
            try:
                texte2="Casino:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                casino=e2.text.replace(texte2,"").strip()
                casino=casino.replace("\t"," ")
            except:
                pass

            thalasso=""
            try:
                texte2="Thalasso:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                thalasso=e2.text.replace(texte2,"").strip()
                thalasso=thalasso.replace("\t"," ")
            except:
                pass

            ski_nautique=""
            try:
                texte2="Ski nautique:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                ski_nautique=e2.text.replace(texte2,"").strip()
                ski_nautique=ski_nautique.replace("\t"," ")
            except:
                pass

            voile=""
            try:
                texte2="Voile:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                voile=e2.text.replace(texte2,"").strip()
                voile=voile.replace("\t"," ")
            except:
                pass

            surf=""
            try:
                texte2="Surf:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                surf=e2.text.replace(texte2,"").strip()
                surf=surf.replace("\t"," ")
            except:
                pass

            equitation=""
            try:
                texte2="Equitation:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                equitation=e2.text.replace(texte2,"").strip()
                equitation=equitation.replace("\t"," ")
            except:
                pass

            randonnee=""
            try:
                texte2="Randonnée:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                randonnee=e2.text.replace(texte2,"").strip()
                randonnee=randonnee.replace("\t"," ")
            except:
                pass

            squash=""
            try:
                texte2="Squash:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                squash=e2.text.replace(texte2,"").strip()
                squash=squash.replace("\t"," ")
            except:
                pass

            restaurants=""
            try:
                texte2="Restaurants:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                restaurants=e2.text.replace(texte2,"").strip()
                restaurants=restaurants.replace("\t"," ")
            except:
                pass

            station_thermale=""
            try:
                texte2="Station thermale:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                station_thermale=e2.text.replace(texte2,"").strip()
                station_thermale=station_thermale.replace("\t"," ")
            except:
                pass

            tennis=""
            try:
                texte2="Tennis:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                tennis=e2.text.replace(texte2,"").strip()
                tennis=tennis.replace("\t"," ")
            except:
                pass

            distance_ville=""
            try:
                texte2="Ville:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                distance_ville=e2.text.replace(texte2,"").strip()
                distance_ville=distance_ville.replace("\t"," ")
            except:
                pass

            shopping=""
            try:
                texte2="Shopping:"
                e2=soup0.find(lambda tag:tag.name=="p" and texte2 in tag.text)
                shopping=e2.text.replace(texte2,"").strip()
                shopping=shopping.replace("\t"," ")
            except:
                pass

            #---------------

            #ajout 15 02 2019
            surface_au_sol=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Surface au sol de " in tag.text)
                l3=e2.text.replace("Surface au sol de ","")
                surface_au_sol=nettoye(l3)
            except:
                pass
            #---------------

            etat_batiment=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Bon état" in tag.text)
                etat_batiment=e2.text.strip()
                etat_batiment=etat_batiment.replace("\t"," ")
            except:
                pass

            parking_interieur=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Parkings intérieurs " in tag.text)
                l3=e2.text.split(" : ")
                parking_interieur=nettoye_m(l3[1])
            except:
                pass

            quartier_ou_lieu_dit=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Quartier ou lieu-dit " in tag.text)
                l3=e2.text.split(" : ")
                quartier_ou_lieu_dit=nettoye(l3[1])
            except:
                pass

            #ajout 15 02 2019
            jardin_prive=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Jardin privé " in tag.text)
                l3=e2.text.split(" : ")
                jardin_prive=nettoye(l3[1])
            except:
                pass

            orientation_du_jardin=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Orientation du jardin " in tag.text)
                l3=e2.text.split(" : ")
                orientation_du_jardin=nettoye(l3[1])
            except:
                pass

            living=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Living " in tag.text)
                l3=e2.text.split(" : ")
                living=nettoye(l3[1])
            except:
                pass

            #----------------

            salle_a_manger=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Salle a manger " in tag.text)
                l3=e2.text.split(" : ")
                salle_a_manger=nettoye(l3[1])
            except:
                pass

            cuisine=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Cuisine " in tag.text)
                l3=e2.text.split(" : ")
                cuisine=nettoye(l3[1])
            except:
                pass

            surface_chambre1=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Chambre  1 " in tag.text)
                l3=e2.text.split(" : ")
                surface_chambre1=nettoye(l3[1])
            except:
                pass

            surface_chambre2=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Chambre  2 " in tag.text)
                l3=e2.text.split(" : ")
                surface_chambre2=nettoye(l3[1])
            except:
                pass

            surface_chambre3=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Chambre  3 " in tag.text)
                l3=e2.text.split(" : ")
                surface_chambre3=nettoye(l3[1])
            except:
                pass

            surface_chambre4=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Chambre  4 " in tag.text)
                l3=e2.text.split(" : ")
                surface_chambre4=nettoye(l3[1])
            except:
                pass

            surface_chambre5=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Chambre  5 " in tag.text)
                l3=e2.text.split(" : ")
                surface_chambre5=nettoye(l3[1])
            except:
                pass

            surface_chambre6=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Chambre  6 " in tag.text)
                l3=e2.text.split(" : ")
                surface_chambre6=nettoye(l3[1])
            except:
                pass

            surface_chambre7=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Chambre  7 " in tag.text)
                l3=e2.text.split(" : ")
                surface_chambre7=nettoye(l3[1])
            except:
                pass

            surface_chambre8=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Chambre  8 " in tag.text)
                l3=e2.text.split(" : ")
                surface_chambre8=nettoye(l3[1])
            except:
                pass

            surface_chambre9=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Chambre  9 " in tag.text)
                l3=e2.text.split(" : ")
                surface_chambre9=nettoye(l3[1])
            except:
                pass

            surface_chambre10=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Chambre  10 " in tag.text)
                l3=e2.text.split(" : ")
                surface_chambre10=nettoye(l3[1])
            except:
                pass

            salle_douche=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Salles de douches " in tag.text)
                l3=e2.text.split(" : ")
                salle_douche=nettoye(l3[1])
            except:
                pass

            terrasse=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Terrasse " in tag.text)
                l3=e2.text.split(" : ")
                terrasse=nettoye(l3[1])
            except:
                pass

            #ajout 15 02 2019 12:50
            annee_construction=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Année de construction " in tag.text)
                l3=e2.text.split(" : ")
                annee_construction=nettoye(l3[1])
            except:
                pass
            #----------------------

            largeur_terrain_rue=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Largeur terrain à rue " in tag.text)
                l3=e2.text.split(" : ")
                largeur_terrain_rue=nettoye_m(l3[1])
            except:
                pass

            if profondeur_terrain=="":
                try:
                    e2=soup0.find(lambda tag:tag.name=="p" and "Profondeur du terrain " in tag.text)
                    l3=e2.text.split(" : ")
                    profondeur_terrain=nettoye_m(l3[1])
                except:
                    pass

            #ajout 11 02 2019
            terrain_a_front_de_rue=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Terrain à front de rue" in tag.text)
                if e2.text.find("Terrain à front de rue")!=-1:
                    terrain_a_front_de_rue="Oui"
            except:
                pass
            #--------------------
            #ajout 10 02 2019
            orientation_facade_rue=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Orientation de la façade rue " in tag.text)
                l3=e2.text.split(" : ")
                orientation_facade_rue=nettoye(l3[1])
            except:
                pass

            type_construction=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "type de construction " in tag.text)
                l3=e2.text.split(" : ")
                type_construction=nettoye(l3[1])
            except:
                pass
            # ----------------

            permis_batir_obtenu=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Permis d'urbanisme obtenu " in tag.text)
                l3=e2.text.split(" : ")
                permis_batir_obtenu=nettoye(l3[1])
            except:
                pass

            autorisation_lotissement=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Autorisation de lotissement " in tag.text)
                l3=e2.text.split(" : ")
                autorisation_lotissement=nettoye(l3[1])
            except:
                pass

            affectation_urban_recente_denomination_plan=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Affectation urbanistique la plus récente sur base des dénominations utilisées dans le registre des plans " in tag.text)
                l3=e2.text.split(" : ")
                affectation_urban_recente_denomination_plan=nettoye(l3[1])
            except:
                pass

            droit_preemption_plan_execution_spatial=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Droit de préemption plan d'exécution spatial " in tag.text)
                l3=e2.text.split(" : ")
                droit_preemption_plan_execution_spatial=nettoye(l3[1])
            except:
                pass

            citation_infraction_urbanistique=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Citation pour infraction urbanistique " in tag.text)
                l3=e2.text.split(" : ")
                citation_infraction_urbanistique=nettoye(l3[1])
            except:
                pass

            salle_bain=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Salles de bains " in tag.text)
                l3=e2.text.split(" : ")
                salle_bain=nettoye(l3[1])
            except:
                pass

            toilette=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Toilettes " in tag.text)
                l3=e2.text.split(" : ")
                toilette=nettoye(l3[1])
            except:
                pass

            #ajout 10 02 2019
            information_urbanistique_complementaire=""
            try:
                e2=soup0.find(lambda tag:tag.name=="p" and "Informations urbanistiques complémentaires " in tag.text)
                l3=e2.text.split(" : ")
                information_urbanistique_complementaire=nettoye(l3[1])
            except:
                pass
            #--------------

            information_zones_inondables=""
            raccordement_egout=""
            gaz_eau_electricite=""
            try:
                # e2=soup0.find(lambda tag:tag.name=="td" and "Information sur les zones inondables  :" in tag.text)
                element_inondable2=soup0.select("td.box-content")
                # element_inondable2=e2.contents
                valeur_inondable=""
                for inond in element_inondable2:
                    try:
                        td_value=inond.text
                        if td_value.find("Information sur les zones inondables  :")!=-1:
                            pos2=td_value.find("Information sur les zones inondables  :")
                            valeur_inondable=td_value[pos2+len("Information sur les zones inondables  :"):]
                        if td_value.find("Raccordement à l'égout")!=-1:
                            raccordement_egout="Oui"
                        if td_value.find("Gaz/Eau/Electricité")!=-1:
                            gaz_eau_electricite="Oui"
                    except:
                        pass
                information_zones_inondables=nettoye(valeur_inondable)
            except:
                pass

            agence_nom=""
            try:
                e2=soup0.find("li", {"class":"nom"})
                agence_nom=nettoye(e2.text)
            except:
                pass

            agence_adresse=""
            agence_cp=""
            agence_ville=""
            agence_num_voie=""
            try:
                e2=soup0.find("li", {"class":"adress"})
                agence_element_adresse=e2.contents
                agence_adresse_avant=agence_element_adresse[0].strip()
                agence_adresse_apres=agence_element_adresse[2].strip()
                agence_cp=agence_adresse_apres.split(" - ")[0].strip()
                agence_ville=agence_adresse_apres.split(" - ")[1].strip()
                agence_num_voie1=agence_adresse_avant.split(" ")[0].strip()
                agence_v2=agence_adresse_avant.split(" ")
                agence_num_voie2=agence_v2[len(agence_v2)-1].strip()
                if isnumerique(agence_num_voie1):
                    agence_num_voie=agence_num_voie1
                    agence_adresse=agence_adresse_avant.replace(agence_num_voie+" ","")
                elif isnumerique(agence_num_voie2):
                    agence_num_voie=agence_num_voie2
                    agence_adresse=agence_adresse_avant.replace(" "+agence_num_voie,"")
                else:
                    agence_adresse=agence_adresse_avant

            except:
                pass
            agence_num_voie=agence_num_voie.replace("\t"," ")
            agence_cp=agence_cp.replace("\t"," ")
            agence_ville=agence_ville.replace("\t"," ")
            agence_adresse=agence_adresse.replace("\t"," ")
            agence_agree_ipi=""
            try:
                e2=soup0.find("li", {"class":"adress"})
                agence_element_adresse=e2.contents
                agence_agree_ipi_text=agence_element_adresse[4].strip()
                if agence_agree_ipi_text.find(u"Agréé IPI n° ")!=-1:
                    agence_agree_ipi=nettoye(agence_agree_ipi_text.replace(u"Agréé IPI n° ",""))
            except:
                pass

            immoweb_code=""
            ref_agence=""
            try:
                e2=soup0.find(lambda tag:tag.name=="b" and "Immoweb code  :" in tag.text)
                liste2=e2.contents
                for l2 in liste2:
                    try:
                        if l2.find("Immoweb code  :")!=-1:
                            immoweb_code=nettoye(l2.replace("Immoweb code  :",""))
                        if l2.find("Agence  :")!=-1:
                            pos3=l2.find("Agence  :")+len("Agence  :")
                            ref_agence=ReplaceAllTab(ReplaceAllDoubleEspace(nettoye(l2[pos3:])))
                        elif l2.find("Ref.")!=-1:
                            pos3=l2.find("Ref.")+len("Ref.")
                            ref_agence=ReplaceAllTab(ReplaceAllDoubleEspace(nettoye(l2[pos3:])))
                            ref_agence=ref_agence.replace(":","").strip()
                    except:
                        pass
            except:
                pass

            ref_agence=ref_agence.replace("\t"," ")
            concat_cle=num_voie+adresse+cp+ville
            cle=retour_chaine_nettoyee(concat_cle)

            curlocal.execute("select * from table_scrapping_immo where cle='"+cle+"'")
            t_cle=curlocal.fetchall()
            if len(t_cle)>0:
                curlocal.execute("update table_recup_liste_a_vendre set traite='o' where idenr="+str(enr["idenr"]))
                local.commit()
                continue

            chauffage=""
            double_vitrage=""
            cpeb_consommation_energetique=""
            numero_rapport_cpeb=""
            lien_calendrier=""

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
            #clic sur informations detaillees
            try:
                # try:
                #     driver.find_element_by_xpath("//p/a[@rel='nofollow']").click()
                #     time.sleep(3)
                # except:
                #     pass
                try:
                    driver.find_element_by_xpath("//span[@id='nuggCloseButtonspan']").click()
                    time.sleep(1)
                except:
                    pass
                try:
                    driver.switch_to.default_content()
                    driver.switch_to.frame("IWEB_IFRAME")
                    s_script3="return $('#main').html()"
                    html3=driver.execute_script(s_script3)
                    soup3=BeautifulSoup(html3, "lxml")
                except:
                    pass

                try:
                    e2=soup3.find(lambda tag:tag.name=="p" and "Chauffage " in tag.text)
                    l3=e2.text.split(" : ")
                    chauffage=nettoye(l3[1])
                except:
                    pass

                try:
                    e2=soup3.find(lambda tag:tag.name=="p" and "Double vitrage" in tag.text)
                    if nz(e2.text)!="":
                        double_vitrage="oui"
                except:
                    pass

                try:
                    e2=soup3.find(lambda tag:tag.name=="h3" and "Certificat de performance énergétique (CPEB)" in tag.text)
                    if nz(e2.text)!="":
                        e3=e2.parent.select("table tbody tr td a img")
                        cpeb_consommation_energetique=e3[0]["src"]
                except:
                    pass

                try:
                    e2=soup3.find(lambda tag:tag.name=="p" and "Numéro du rapport CPEB " in tag.text)
                    l3=e2.text.split(" : ")
                    numero_rapport_cpeb=nettoye(l3[1])
                except:
                    pass

                try:
                    driver.switch_to.default_content()
                    driver.switch_to.frame("IWEB_ONGLET")
                    driver.find_element_by_xpath("//td[@class='tab-actif']/span/a/b[text()='Calendrier & Prix']").click()
                    time.sleep(3)
                    lien_calendrier=driver.current_url
                except:
                    pass

            except:
                pass

            prix_demande_hors_droits_enregistrement_hors_frais_notaire=""
            prix_inclut_poste_architecte=""
            prix_inclut_poste_ingenieur_en_stabilite=""
            prix_inclut_poste_coordinateur_de_securite=""
            prix_inclut_poste_etude_du_sol=""
            prix_inclut_poste_amenagement_de_la_cuisine=""
            prix_inclut_poste_amenagement_des_abords=""
            prix_inclut_poste_test_blower_door=""

            try:
                driver.switch_to.default_content()
                driver.switch_to.frame("IWEB_ONGLET")
                driver.find_element_by_xpath("//td[@class='tab-actif']/span/a/b[text()='Financier']").click()
                time.sleep(2)
                driver.switch_to.default_content()
                driver.switch_to.frame("IWEB_IFRAME")

                try:
                    s_script1="return $('.box-content').html()"
                    html1=driver.execute_script(s_script1)
                    soup1=BeautifulSoup(html1, "lxml")
                    e2=soup1.find(lambda tag:tag.name=="p" and "Prix demandé hors droits d'enregistrement" in tag.text)
                    if "et hors frais de notaire" in e2.text:
                        prix_demande_hors_droits_enregistrement_hors_frais_notaire="Oui"
                except:
                    pass

                s_script1="return $('.box-content').html()"
                html1=driver.execute_script(s_script1)
                soup1=BeautifulSoup(html1, "lxml")

                #ajout 15 02 2019
                try:
                    e2=soup1.find(lambda tag:tag.name=="p" and "Architecte  :" in tag.text)
                    l3=e2.text.split(" : ")
                    prix_inclut_poste_architecte=nettoye(l3[1])
                except:
                    pass

                try:
                    e2=soup1.find(lambda tag:tag.name=="p" and "Ingénieur en stabilité  :" in tag.text)
                    l3=e2.text.split(" : ")
                    prix_inclut_poste_ingenieur_en_stabilite=nettoye(l3[1])
                except:
                    pass

                try:
                    e2=soup1.find(lambda tag:tag.name=="p" and "Coordinateur de sécurité  :" in tag.text)
                    l3=e2.text.split(" : ")
                    prix_inclut_poste_coordinateur_de_securite=nettoye(l3[1])
                except:
                    pass

                try:
                    e2=soup1.find(lambda tag:tag.name=="p" and "Etude du sol  :" in tag.text)
                    l3=e2.text.split(" : ")
                    prix_inclut_poste_etude_du_sol=nettoye(l3[1])
                except:
                    pass

                try:
                    e2=soup1.find(lambda tag:tag.name=="p" and "Aménagement de la cuisine  :" in tag.text)
                    l3=e2.text.split(" : ")
                    prix_inclut_poste_amenagement_de_la_cuisine=nettoye(l3[1])
                except:
                    pass

                try:
                    e2=soup1.find(lambda tag:tag.name=="p" and "Aménagement des abords  :" in tag.text)
                    l3=e2.text.split(" : ")
                    prix_inclut_poste_amenagement_des_abords=nettoye(l3[1])
                except:
                    pass

                try:
                    e2=soup1.find(lambda tag:tag.name=="p" and "Test Blower Door  :" in tag.text)
                    l3=e2.text.split(" : ")
                    prix_inclut_poste_test_blower_door=nettoye(l3[1])
                except:
                    pass
                #---------------
            except:
                pass

            driver.switch_to.default_content()
            try:
                driver.switch_to.frame("IWEB_ONGLET")
            except:
                pass

            try:
                driver.find_element_by_xpath("//td[@class='tab-actif']/span/a/b[text()='Description']").click()
                time.sleep(3)
            except:
                pass
            driver.switch_to.default_content()

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            tel=""
            disponibilite_tel=""
            mobile=""
            disponibilite_mobile = ""
            try:
                driver.find_element_by_xpath("//a[@class='lightboxTriggerTel buttonTel']").click()
                time.sleep(2)
                try:
                    element_tel2=driver.find_element_by_xpath("//div[@class='boxoverlayer-tel']/div[@class='tel01 infoElement']")
                    tel=u""+element_tel2.text
                    tel=tel.replace("\t"," ")
                except:
                    pass
                try:
                    element_mobile=driver.find_element_by_xpath("//div[@class='boxoverlayer-tel']/div[@class='mobile01 infoElement']")
                    mobile=u""+element_mobile.text
                    mobile=mobile.replace("\t"," ")
                except:
                    pass
                try:
                    element_dispo=driver.find_element_by_xpath("//div[@class='dispo infoElement']")
                    disponibilite_tel=u""+element_dispo.text
                    disponibilite_tel=disponibilite_tel.replace("\t"," ")
                except:
                    pass
            except:
                pass

            #------------------------
            #-------maj 07/02/2019----
            if z==1:
                rep=rep+"\\"+date2_
                if(os.access(rep,os.F_OK)==False):
                    os.makedirs(rep,777)

                export = open(rep + "\\" +categorie+"_terrain_"+ str(date_)+".txt", "w")
                export.write("lien_url"+"\t"+"categorie"+"\t"+"bien"+"\t"+"designation"+"\t"+"num_voie"+"\t"+"adresse"+"\t"+"cp"+"\t"+"ville"+"\t"+"prix"+"\t"+"prix_au_m2"+"\t"+"surface_constructible"+"\t"+"libre_le"+"\t"+"largeur_facade_rue"+"\t"+"delai_de_construction"+"\t"+"nombre_facade"+"\t"+"nombre_etage"+"\t"+"surface_au_sol"+"\t"+"etat_batiment"+"\t"+"parking_interieur"+"\t"+"surface"+"\t"+"largeur_terrain_rue"+"\t"+"profondeur_terrain"+"\t"+"hauteur_entree"+"\t"+"largeur_porte"+"\t"+"largeur_interieur"+"\t"+"largeur"+"\t"+"hauteur"+"\t"+"chambre"+"\t"+"surface_habitable"+"\t"+"architecture_contemporain"+"\t"+"maconnerie_traditionnelle"+"\t"+"terrain_a_front_de_rue"+"\t"+"orientation_facade_rue"+"\t"+"type_construction"+"\t"+"permis_batir_obtenu"+"\t"+"raccordement_egout"+"\t"+"autorisation_lotissement"+"\t"+"affectation_urban_recente_denomination_plan"+"\t"+"droit_preemption_plan_execution_spatial"+"\t"+"citation_infraction_urbanistique"+"\t"+"salle_bain"+"\t"+"toilette"+"\t"+"information_urbanistique_complementaire"+"\t"+"information_zones_inondables"+"\t"+"agence_nom"+"\t"+"agence_num_voie"+"\t"+"agence_adresse"+"\t"+"agence_cp"+"\t"+"agence_ville"+"\t"+"agence_agree_ipi"+"\t"+"immoweb_code"+"\t"+"ref_agence"+"\t"+"prix_demande_hors_droits_enregistrement_hors_frais_notaire"+"\t"+"prix_inclut_poste_architecte"+"\t"+"prix_inclut_poste_ingenieur_en_stabilite"+"\t"+"prix_inclut_poste_coordinateur_de_securite"+"\t"+"prix_inclut_poste_etude_du_sol"+"\t"+"prix_inclut_poste_amenagement_de_la_cuisine"+"\t"+"prix_inclut_poste_amenagement_des_abords"+"\t"+"prix_inclut_poste_test_blower_door"+"\t"+"tel"+"\t"+"disponibilite_tel"+"\t"+"mobile"+"\t"+"disponibilite_mobile"+"\t""nombre_personnes"+"\t"+"nom_immeuble"+"\t"+"annee_construction"+"\t"+"teledistribution"+"\t"+"parking_exterieur"+"\t"+"bord_de_mer_lac"+"\t"+"dans_la_verdure"+"\t"+"jardin_prive"+"\t"+"orientation_du_jardin"+"\t"+"terrasse"+"\t"+"piscine"+"\t"+"barbecue"+"\t"+"living"+"\t"+"salle_a_manger"+"\t"+"cuisine"+"\t"+"surface_chambre1"+"\t"+"surface_chambre2"+"\t"+"surface_chambre3"+"\t"+"surface_chambre4"+"\t"+"surface_chambre5"+"\t"+"surface_chambre6"+"\t"+"surface_chambre7"+"\t"+"surface_chambre8"+"\t"+"surface_chambre9"+"\t"+"surface_chambre10"+"\t"+"salle_douche"+"\t"+"jacuzzi"+"\t"+"sauna"+"\t"+"frigo"+"\t"+"congelateur"+"\t"+"micro_ondes"+"\t"+"connexion_internet"+"\t"+"caution_garantie_locative"+"\t"+"acompte_en_pourcentage_du_loyer"+"\t"+"frais_de_dossier"+"\t"+"golf"+"\t"+"mer"+"\t"+"gare"+"\t"+"aeroport"+"\t"+"office_du_tourisme"+"\t"+"marches"+"\t"+"magasins"+"\t"+"grandes_villes"+"\t"+"vtt"+"\t"+"bowling"+"\t"+"casino"+"\t"+"thalasso"+"\t"+"ski_nautique"+"\t"+"voile"+"\t"+"surf"+"\t"+"equitation"+"\t"+"randonnee"+"\t"+"squash"+"\t"+"restaurants"+"\t"+"station_thermale"+"\t"+"tennis"+"\t"+"distance_ville"+"\t"+"shopping"+"\t"+"chauffage"+"\t"+"double_vitrage"+"\t"+"cpeb_consommation_energetique"+"\t"+"numero_rapport_cpeb"+"\t"+"lien_calendrier"+"\t"+"lien_photo"+"\t"+"page"+"\n")
                export.close()

            insertion("table_scrapping_immo",["lien_url","categorie","bien","designation","num_voie","adresse","cp","ville","prix","prix_au_m2","surface_constructible","libre_le","largeur_facade_rue","delai_de_construction","nombre_facade","nombre_etage","surface_au_sol","etat_batiment","parking_interieur","surface","largeur_terrain_rue","profondeur_terrain","hauteur_entree","largeur_porte","largeur_interieur","largeur","hauteur","chambre","surface_habitable","architecture_contemporain","maconnerie_traditionnelle","terrain_a_front_de_rue","orientation_facade_rue","type_construction","permis_batir_obtenu","raccordement_egout","autorisation_lotissement","affectation_urban_recente_denomination_plan","droit_preemption_plan_execution_spatial","citation_infraction_urbanistique","salle_bain","toilette","information_urbanistique_complementaire","information_zones_inondables","agence_nom","agence_num_voie","agence_adresse","agence_cp","agence_ville","agence_agree_ipi","immoweb_code","ref_agence","prix_demande_hors_droits_enregistrement_hors_frais_notaire","prix_inclut_poste_architecte","prix_inclut_poste_ingenieur_en_stabilite","prix_inclut_poste_coordinateur_de_securite","prix_inclut_poste_etude_du_sol","prix_inclut_poste_amenagement_de_la_cuisine","prix_inclut_poste_amenagement_des_abords","prix_inclut_poste_test_blower_door","tel","disponibilite_tel","mobile","disponibilite_mobile","nombre_personnes","nom_immeuble","annee_construction","teledistribution","parking_exterieur","bord_de_mer_lac","dans_la_verdure","jardin_prive","orientation_du_jardin","terrasse","piscine","barbecue","living","salle_a_manger","cuisine","surface_chambre1","surface_chambre2","surface_chambre3","surface_chambre4","surface_chambre5","surface_chambre6","surface_chambre7","surface_chambre8","surface_chambre9","surface_chambre10","salle_douche","jacuzzi","sauna","frigo","congelateur","micro_ondes","connexion_internet","caution_garantie_locative","acompte_en_pourcentage_du_loyer","frais_de_dossier","golf","mer","gare","aeroport","office_du_tourisme","marches","magasins","grandes_villes","vtt","bowling","casino","thalasso","ski_nautique","voile","surf","equitation","randonnee","squash","restaurants","station_thermale","tennis","distance_ville","shopping","chauffage","double_vitrage","cpeb_consommation_energetique","numero_rapport_cpeb","lien_calendrier","lien_photo","page","cle"], [lien_url,categorie,bien,designation,num_voie,adresse,cp,ville,prix,prix_au_m2,surface_constructible,libre_le,largeur_facade_rue,delai_de_construction,nombre_facade,nombre_etage,surface_au_sol,etat_batiment,parking_interieur,surface,largeur_terrain_rue,profondeur_terrain,hauteur_entree,largeur_porte,largeur_interieur,largeur,hauteur,chambre,surface_habitable,architecture_contemporain,maconnerie_traditionnelle,terrain_a_front_de_rue,orientation_facade_rue,type_construction,permis_batir_obtenu,raccordement_egout,autorisation_lotissement,affectation_urban_recente_denomination_plan,droit_preemption_plan_execution_spatial,citation_infraction_urbanistique,salle_bain,toilette,information_urbanistique_complementaire,information_zones_inondables,agence_nom,agence_num_voie,agence_adresse,agence_cp,agence_ville,agence_agree_ipi,immoweb_code,ref_agence,prix_demande_hors_droits_enregistrement_hors_frais_notaire,prix_inclut_poste_architecte,prix_inclut_poste_ingenieur_en_stabilite,prix_inclut_poste_coordinateur_de_securite,prix_inclut_poste_etude_du_sol,prix_inclut_poste_amenagement_de_la_cuisine,prix_inclut_poste_amenagement_des_abords,prix_inclut_poste_test_blower_door,tel,disponibilite_tel,mobile,disponibilite_mobile,nombre_personnes,nom_immeuble,annee_construction,teledistribution,parking_exterieur,bord_de_mer_lac,dans_la_verdure,jardin_prive,orientation_du_jardin,terrasse,piscine,barbecue,living,salle_a_manger,cuisine,surface_chambre1,surface_chambre2,surface_chambre3,surface_chambre4,surface_chambre5,surface_chambre6,surface_chambre7,surface_chambre8,surface_chambre9,surface_chambre10,salle_douche,jacuzzi,sauna,frigo,congelateur,micro_ondes,connexion_internet,caution_garantie_locative,acompte_en_pourcentage_du_loyer,frais_de_dossier,golf,mer,gare,aeroport,office_du_tourisme,marches,magasins,grandes_villes,vtt,bowling,casino,thalasso,ski_nautique,voile,surf,equitation,randonnee,squash,restaurants,station_thermale,tennis,distance_ville,shopping,chauffage,double_vitrage,cpeb_consommation_energetique,numero_rapport_cpeb,lien_calendrier,lien_photo,page1,cle],local)
            print("insertion {0} '{1}' | '{2}'".format(categorie, bien, page1))
            export = open(rep + "\\" +categorie+"_terrain_"+ str(date_)+".txt", "a")
            export.write(lien_url+"\t"+categorie+"\t"+bien+"\t"+designation+"\t"+num_voie+"\t"+adresse+"\t"+cp+"\t"+ville+"\t"+prix+"\t"+prix_au_m2+"\t"+surface_constructible+"\t"+libre_le+"\t"+largeur_facade_rue+"\t"+delai_de_construction+"\t"+nombre_facade+"\t"+nombre_etage+"\t"+surface_au_sol+"\t"+etat_batiment+"\t"+parking_interieur+"\t"+surface+"\t"+largeur_terrain_rue+"\t"+profondeur_terrain+"\t"+hauteur_entree+"\t"+largeur_porte+"\t"+largeur_interieur+"\t"+largeur+"\t"+hauteur+"\t"+chambre+"\t"+surface_habitable+"\t"+architecture_contemporain+"\t"+maconnerie_traditionnelle+"\t"+terrain_a_front_de_rue+"\t"+orientation_facade_rue+"\t"+type_construction+"\t"+permis_batir_obtenu+"\t"+raccordement_egout+"\t"+autorisation_lotissement+"\t"+affectation_urban_recente_denomination_plan+"\t"+droit_preemption_plan_execution_spatial+"\t"+citation_infraction_urbanistique+"\t"+salle_bain+"\t"+toilette+"\t"+information_urbanistique_complementaire+"\t"+information_zones_inondables+"\t"+agence_nom+"\t"+agence_num_voie+"\t"+agence_adresse+"\t"+agence_cp+"\t"+agence_ville+"\t"+agence_agree_ipi+"\t"+immoweb_code+"\t"+ref_agence+"\t"+prix_demande_hors_droits_enregistrement_hors_frais_notaire+"\t"+prix_inclut_poste_architecte+"\t"+prix_inclut_poste_ingenieur_en_stabilite+"\t"+prix_inclut_poste_coordinateur_de_securite+"\t"+prix_inclut_poste_etude_du_sol+"\t"+prix_inclut_poste_amenagement_de_la_cuisine+"\t"+prix_inclut_poste_amenagement_des_abords+"\t"+prix_inclut_poste_test_blower_door+"\t"+tel+"\t"+disponibilite_tel+"\t"+mobile+"\t"+disponibilite_mobile+"\t"+nombre_personnes+"\t"+nom_immeuble+"\t"+annee_construction+"\t"+teledistribution+"\t"+parking_exterieur+"\t"+bord_de_mer_lac+"\t"+dans_la_verdure+"\t"+jardin_prive+"\t"+orientation_du_jardin+"\t"+terrasse+"\t"+piscine+"\t"+barbecue+"\t"+living+"\t"+salle_a_manger+"\t"+cuisine+"\t"+surface_chambre1+"\t"+surface_chambre2+"\t"+surface_chambre3+"\t"+surface_chambre4+"\t"+surface_chambre5+"\t"+surface_chambre6+"\t"+surface_chambre7+"\t"+surface_chambre8+"\t"+surface_chambre9+"\t"+surface_chambre10+"\t"+salle_douche+"\t"+jacuzzi+"\t"+sauna+"\t"+frigo+"\t"+congelateur +"\t"+micro_ondes+"\t"+connexion_internet+"\t"+caution_garantie_locative+"\t"+acompte_en_pourcentage_du_loyer+"\t"+frais_de_dossier+"\t"+golf+"\t"+mer+"\t"+gare+"\t"+aeroport+"\t"+office_du_tourisme+"\t"+marches+"\t"+magasins+"\t"+grandes_villes+"\t"+vtt+"\t"+bowling+"\t"+casino+"\t"+thalasso+"\t"+ski_nautique+"\t"+voile+"\t"+surf+"\t"+equitation+"\t"+randonnee+"\t"+squash+"\t"+restaurants+"\t"+station_thermale+"\t"+tennis+"\t"+distance_ville+"\t"+shopping+"\t"+chauffage+"\t"+double_vitrage+"\t"+cpeb_consommation_energetique+"\t"+numero_rapport_cpeb+"\t"+lien_calendrier+"\t"+lien_photo+"\t"+page1+"\n")
            export.close()
            curlocal.execute("update table_recup_liste_a_vendre set traite='o' where idenr="+str(enr["idenr"]))
            local.commit()

        try:
            driver.close()
        except:
            pass

        trace = open("trace_terrain.txt", "a")
        trace.write("FIN Scrapping terrain "+categorie+" !"+"\n")
        trace.close()

        #Suppression du fichier .lock
        if os.path.exists('terrain.lock')==True:
            os.remove('terrain.lock')

        sys.exit(0)
        # print("FIN Traitement recuperation donnees !")

    except Exception as inst:
        log=open(date_jour.replace("/", "-")+".txt", "a")
        traceback.print_exc(file=log)
        log.close()
        try:
            driver.close()
        except:
            pass
        if os.path.exists('terrain.lock')==True:
            os.remove('terrain.lock')

        sys.exit(0)
