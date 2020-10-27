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

def nettoye(chaine):
    chaine=chaine.replace("\t"," ").replace("\n"," ").replace("  "," ").strip().strip("\t").strip("\n")
    return chaine


if os.path.exists("recup_liste_a_vendre.lock")==False:
    try:
        lock=open("recup_liste_a_vendre.lock", "a")
        lock.close()
        k = 0

        #31 12 2018 python27
        trace = open("trace_recup_liste_a_vendre.txt", "w")
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
            trace = open("trace_recup_liste_a_vendre.txt", "a")
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
        scroll_debut = int(config.get('parametre', 'scroll_debut'))

        temps_affichage_page_suivante = int(config.get('parametre', 'temps_affichage_page_suivante'))
        temps_affichage_tel = int(config.get('parametre', 'temps_affichage_tel'))

        cle="a_vendre"

        lien = config.get(cle, 'lien')
        categorie = config.get(cle, 'categorie')

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

        #Recuperation
        driver.get(lien)

        driver.maximize_window()
        driver.switch_to.frame("IWEB_IFRAME_SEARCH")

        idCategorie=driver.find_element_by_id("idCategorie")
        # print(dir(idCategorie))
        liste_option=[]
        liste_option_libelle=[]
        options_element=idCategorie.find_elements_by_tag_name("option")
        for x in range(1, len(options_element)):
            # if x in [1,2]:
            liste_option.append(u""+options_element[x].get_attribute("id"))
            liste_option_libelle.append(u""+options_element[x].text)
        date_=datetime.datetime.now().strftime("%Y%m%d %H%M%S")
        y=0

        for element_option in liste_option:
            # if bfin:
            #     break
            y=y+1
            if y>1:
                driver.get(lien)

                driver.maximize_window()
                driver.switch_to.frame("IWEB_IFRAME_SEARCH")

            s_script= "document.getElementById('"+u""+element_option+"').setAttribute('selected', 'true')"
            driver.execute_script(s_script)
            bien=liste_option_libelle[y-1]
            trace = open("trace_recup_liste_a_vendre.txt", "a")
            trace.write("entree option {0}\n".format(u""+element_option))
            trace.close()
            driver.switch_to.default_content()
            driver.execute_script("window.scrollTo(0, "+str(scroll_debut)+");")
            driver.switch_to.frame("IWEB_IFRAME_SEARCH")

            element_rechercher=driver.find_element_by_xpath("//button[@class='sendsearch btn-blue']")
            element_rechercher.click()
            time.sleep(temps_affichage_resultat)
            driver.switch_to.default_content()

            page1="1"
            while True:
                inc=0

                try:
                    time.sleep(3)
                    s_script0="return $('.box-stroke-white').html()"
                    html0=driver.execute_script(s_script0)
                    soup0=BeautifulSoup(html0, "lxml")
                except:
                    break

                liste_lien=soup0.findAll("div", {"data-type":"resultgallery-resultitem"})
                x=0
                for enr_lien in liste_lien:
                    x=x+1
                    # print(enr_lien.a.attrs["href"])
                    href=enr_lien.a["href"]
                    print("******* href: {0}".format(href))
                    # element_lien_photo=enr_lien.find("div", {"class":"photo-bien xl-photo photo-centered"}).img
                    element_lien_photo=enr_lien.select("div.owl-item.active div.photo-bien.xl-photo.photo-centered")

                    lien_photo=""
                    try:
                        lien_photo=element_lien_photo[0].contents[1]["src"]
                        print("lien photo: {0}".format(lien_photo))
                    except:
                        pass

                    designation=""
                    try:
                        element_designation=enr_lien.select("div.result-xl-title-bar div.title-bar-left")
                        designation=nettoye(element_designation[0].text)
                    except:
                        pass

                    #-------maj entete 07/02/2019----
                    curlocal.execute("select lien_photo, categorie from table_recup_liste_a_vendre where categorie='"+categorie+"' and lien_photo='"+lien_photo+"'")
                    t_lien_photo=curlocal.fetchall()
                    if len(t_lien_photo)==0:
                        insertion("table_recup_liste_a_vendre",["categorie","bien","designation","href","lien_photo","page"], [categorie,bien,designation,href,lien_photo,page1],local)
                        print("insertion {0} '{1}' | '{2}'".format(categorie, bien, page1))
                    else:
                        print("existe deja {0} '{1}' | '{2}'".format(categorie, bien, page1))
                    # if page1=="1" or page1=="17":
                    #     if x==1:
                    #         break

                try:
                    driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(3)
                    element_page_suivantes=driver.find_elements_by_xpath("//div[@class='navig-arrow-right']/a")
                    element_page_suivante=element_page_suivantes[0]
                    element_href=element_page_suivante.get_attribute("href")
                    href=u""+element_href
                    parse1 = urlparse.parse_qs(urlparse.urlparse(href).query)
                    page1=str(u""+parse1["page"][0])

                    # if page1=="2":
                    #     current_url=href
                    #     url_suivant=current_url.replace("?page=2", "?page=17")
                    #     driver.get(url_suivant)
                    #     page1="17"
                    #     pass
                    # else:
                    try:
                        element_page_suivante.click()
                    except Exception as inst:
                        # log=open(date_jour.replace("/", "-")+".txt", "a")
                        # traceback.print_exc(file=log)
                        # log.close()
                        pass

                    time.sleep(temps_affichage_page_suivante)
                except Exception as inst:
                    # log=open(date_jour.replace("/", "-")+".txt", "a")
                    # traceback.print_exc(file=log)
                    # log.close()
                    # bfin=True
                    break

        try:
            driver.close()
        except:
            pass

        trace = open("trace_recup_liste_a_vendre.txt", "a")
        trace.write("FIN Recup liste a vendre "+categorie+" !"+"\n")
        trace.close()

        #Suppression du fichier .lock
        if os.path.exists('recup_liste_a_vendre.lock')==True:
            os.remove('recup_liste_a_vendre.lock')

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
        if os.path.exists('recup_liste_a_vendre.lock')==True:
            os.remove('recup_liste_a_vendre.lock')

        sys.exit(0)
