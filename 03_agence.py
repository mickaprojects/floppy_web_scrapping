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
    # if str(chaine).find(" €/mois".encode("cp1252"))!=-1:
    #     chaine=str(chaine).replace(" €/mois".encode("cp1252"),"")
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

def ReplaceAllDoubleEspace(chaine):
    newchaine = chaine
    while newchaine.find('  ') >= 0:
        newchaine = newchaine.replace('  ', ' ')
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



if os.path.exists("agence.lock")==False and os.path.exists("recup_liste_agence.lock")==False:
    try:
        lock=open("agence.lock", "a")
        lock.close()
        k = 0

        #31 12 2018 python27
        trace = open("trace_agence.txt", "w")
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
            trace = open("trace_agence.txt", "a")
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

        curlocal.execute("select * from table_recup_liste_a_vendre where categorie='agence' and position('emplacement' in lower(designation))=0 and position('terrain' in lower(designation))=0 and position('garage' in lower(designation))=0 and position('construire' in lower(designation))=0 and position('vacance' in lower(designation))=0 and traite='n'")
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
            ref_promoteur=""
            nom_immeuble=""
            emplacement=""
            try:
                time.sleep(2)
                element_adresse=driver.find_element_by_id("propertyPage-title-address-output")
                adresse=u""+element_adresse.text
                adresse=str(adresse).strip()
                adresse_=adresse.split("|")
                adresse_avant=adresse_[0].strip()
                adresse_apres=adresse_[1].strip()
                cp=adresse_apres.split(" - ")[0].strip()
                ville=adresse_apres.split(" - ")[1].strip()
                num_voie1=adresse_avant.split(" ")[0].strip()
                num_voie11=adresse_avant.split(" ")[0].strip().replace("-","").replace(",","")
                v2=adresse_avant.split(" ")
                num_voie2=v2[len(v2)-1].strip()
                num_voie22=v2[len(v2)-1].strip().replace("-","").replace(",","")
                if isnumerique(num_voie11):
                    num_voie=num_voie1
                    num_voie=num_voie.strip(",")
                    adresse=adresse_avant.replace(num_voie1+" ","")
                elif isnumerique(num_voie22):
                    num_voie=num_voie2
                    num_voie=num_voie.strip(",")
                    adresse=adresse_avant.replace(" "+num_voie2,"")
                else:
                    adresse=adresse_avant

            except:
                pass

            concat_cle=num_voie+adresse+cp+ville
            cle=retour_chaine_nettoyee(concat_cle)

            curlocal.execute("select * from table_scrapping_immo where cle='"+cle+"'")
            t_cle=curlocal.fetchall()
            if len(t_cle)>0:
                curlocal.execute("update table_recup_liste_a_vendre set traite='o' where idenr="+str(enr["idenr"]))
                local.commit()
                continue

            try:
                element_prix=driver.find_element_by_xpath("//div[@class='iw-propertypage-price-current-content']")
                prix=element_prix.text
                # if str(prix).find(" €/mois".encode("cp1252"))!=-1:
                #     prix=str(prix).replace(" €/mois".encode("cp1252"),"")
                # elif str(prix).find(" €".encode("cp1252"))!=-1:
                #     prix=str(prix).replace(" €".encode("cp1252"),"")
            except:
                pass

            surface=""
            chambre=""
            salle_bain=""
            habitable=""
            try:
                e2=driver.find_element_by_xpath("//div[@id='iw-propertypage-main-info']/ul/li/h3/span[@data-label='bedroom']/following-sibling::span")
                chambre=e2.text
            except:
                pass

            try:
                e2=driver.find_element_by_xpath("//div[@id='iw-propertypage-main-info']/ul/li/h3/span[@data-label='bathroom']/following-sibling::span")
                salle_bain=e2.text
            except:
                pass

            try:
                e2=driver.find_element_by_xpath("//div[@id='iw-propertypage-main-info']/ul/li/h3/span[@data-label='land']/following-sibling::span")
                surface=e2.text
            except:
                pass
            if str(surface).find("m²".encode("cp1252"))!=-1:
                surface=str(surface).replace(" m²".encode("cp1252"),"")
            if str(surface).find("m2".encode("cp1252"))!=-1:
                surface=str(surface).replace(" m2".encode("cp1252"),"")

            try:
                e2=driver.find_element_by_xpath("//div[@id='iw-propertypage-main-info']/ul/li/h3/span[@data-label='livingArea']/following-sibling::span")
                habitable=e2.text
            except:
                pass

            #ajout 12 02 2019
            bien_disponible=""
            try:
                e2=driver.find_element_by_xpath("//div[@id='iw-propertypage-main-info']/ul/li/h3/span[@data-label='unitCount']/following-sibling::span")
                bien_disponible=e2.text
            except:
                pass
            #--------------

            #ajout 13 02 2019
            date_de_livraison=""
            try:
                e2=driver.find_element_by_xpath("//div[@id='iw-propertypage-main-info']/ul/li/h3/span[@data-label='deliveryDate']/following-sibling::span")
                date_de_livraison=e2.text
            except:
                pass
            #---------------

            if str(habitable).find("m²".encode("cp1252"))!=-1:
                habitable=str(habitable).replace(" m²".encode("cp1252"),"")
            if str(habitable).find("m2".encode("cp1252"))!=-1:
                habitable=str(habitable).replace(" m2".encode("cp1252"),"")

            #structure en bas
            try:
                s_script0="return $('#iw-propertypage-verticals').html()"
                html0=driver.execute_script(s_script0)
                soup0=BeautifulSoup(html0, "lxml")
            except:
                pass
            disponible_le=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-availability"}).td
                # e2=soup0.find("td", {"class":"iw-propertypage-verticals-characteristic-value"})
                # e2=driver.find_element_by_xpath("//tr[@aria-label='general-availability']/td")
                disponible_le=nettoye(e2.text)
            except:
                pass

            quartier_ou_lieu_dit=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-buildingDescription-district"}).td
                # e2=soup0.find("td", {"class":"iw-propertypage-verticals-characteristic-value"})
                # e2=driver.find_element_by_xpath("//tr[@aria-label='general-buildingDescription-district']/td")
                quartier_ou_lieu_dit=nettoye(e2.text)
            except:
                pass

            annee_de_construction=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-buildingDescription-constructionYear"}).td
                annee_de_construction=nettoye(e2.text)
            except:
                pass

            nombre_etage=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-buildingDescription-floorCount"}).td
                nombre_etage=nettoye(e2.text)
            except:
                pass

            #ajout 09 02 2019
            etage_du_bien=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-buildingDescription-floorOfProperty"}).td
                etage_du_bien=nettoye(e2.text)
            except:
                pass
            #----------------

            #ajout 07 02 2019
            nombre_logement=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-buildingDescription-dwellingsNumber"}).td
                nombre_logement=nettoye(e2.text)
            except:
                pass
            #---------------

            etat_batiment=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-buildingDescription-renovationType"}).td
                etat_batiment=nettoye(e2.text)
            except:
                pass

            largeur_facade_rue=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-buildingDescription-streetFacadeWidth"}).td
                largeur_facade_rue=nettoye3(e2.text)
            except:
                pass

            nombre_facade=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-buildingDescription-facadeCount"}).td
                nombre_facade=nettoye(e2.text)
            except:
                pass

            surface_disponible=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-buildingDescription-availableArea"}).td
                surface_disponible=nettoye(e2.text)
            except:
                pass

            #ajout 09 02 2019
            meuble=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-newlyBuilt-furnished"}).td
                meuble=nettoye(e2.text)
            except:
                pass
            #----------------

            #ajout 07 02 2019
            parking_interieur=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-parking-indoorParkingSpaceCount"}).td
                parking_interieur=nettoye(e2.text)
            except:
                pass

            parking_exterieur=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-parking-outdoorParkingSpaceCount"}).td
                parking_exterieur=nettoye(e2.text)
            except:
                pass

            #----------------
            environnement=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-surroundings-surroundingsType"}).td
                environnement=nettoye(e2.text)
            except:
                pass

            #ajout 12 02 2019
            premiere_occupation=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-newlyBuilt-isFirstOccupation"}).td
                premiere_occupation=nettoye(e2.text)
            except:
                pass
            #-----------------

            #ajout 13 02 2019
            distance_transport=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-surroundings-distanceTransports"}).td
                distance_transport=nettoye3(e2.text)
            except:
                pass
            #-----------------

            distance_ecole=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-surroundings-distanceSchool"}).td
                distance_ecole=nettoye3(e2.text)
            except:
                pass

            distance_commerce=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-surroundings-distanceShop"}).td
                distance_commerce=nettoye3(e2.text)
            except:
                pass

            surface_habitable=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-livingDescription-habitableArea"}).td
                surface_habitable=nettoye(e2.text)
            except:
                pass

            #ajout 14 02 2019 09:40
            feux_ouverts=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-livingDescription-firePlaceCount"}).td
                feux_ouverts=nettoye(e2.text)
            except:
                pass
            #----------------

            #ajout 13 02 2019
            porte_d_acces=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-industrialDescription-accessDoorCount"}).td
                porte_d_acces=nettoye(e2.text)
            except:
                pass

            porte_de_section=""
            try:
                e2=soup0.find("tr", {"aria-label":"general-industrialDescription-sectionalDoorCount"}).td
                porte_de_section=nettoye(e2.text)
            except:
                pass
            #---------------

            #ajout 07 02 2019
            nombre_piece=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-livingDescription-roomCount"}).td
                nombre_piece=nettoye(e2.text)
            except:
                pass
            #--------------

            living=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-livingDescription-hasLivingRoom"}).td
                living=nettoye(e2.text)
            except:
                pass

            surface_living=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-livingDescription-livingRoomArea"}).td
                surface_living=nettoye(e2.text)
            except:
                pass

            #ajout 07 02 2019
            salle_a_manger=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-livingDescription-hasDiningRoom"}).td
                salle_a_manger=nettoye(e2.text)
            except:
                pass

            surface_salle_a_manger=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-livingDescription-diningRoomArea"}).td
                surface_salle_a_manger=nettoye(e2.text)
            except:
                pass

            #----------

            surface_cuisine=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-kitchenDescription-kitchenArea"}).td
                surface_cuisine=nettoye(e2.text)
            except:
                pass

            amenagement_cuisine=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-kitchenDescription-kitchenType"}).td
                amenagement_cuisine=nettoye(e2.text)
            except:
                pass

            teledistribution=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-cableTV"}).td
                teledistribution=nettoye(e2.text)
            except:
                pass

            surface_chambre1=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bedroomDescription-1Area"}).td
                surface_chambre1=nettoye(e2.text)
            except:
                pass

            surface_chambre2=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bedroomDescription-2Area"}).td
                surface_chambre2=nettoye(e2.text)
            except:
                pass

            surface_chambre3=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bedroomDescription-3Area"}).td
                surface_chambre3=nettoye(e2.text)
            except:
                pass

            surface_chambre4=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bedroomDescription-4Area"}).td
                surface_chambre4=nettoye(e2.text)
            except:
                pass

            surface_chambre5=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bedroomDescription-5Area"}).td
                surface_chambre5=nettoye(e2.text)
            except:
                pass

            surface_chambre6=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bedroomDescription-6Area"}).td
                surface_chambre6=nettoye(e2.text)
            except:
                pass

            surface_chambre7=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bedroomDescription-7Area"}).td
                surface_chambre7=nettoye(e2.text)
            except:
                pass

            surface_chambre8=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bedroomDescription-8Area"}).td
                surface_chambre8=nettoye(e2.text)
            except:
                pass

            surface_chambre9=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bedroomDescription-9Area"}).td
                surface_chambre9=nettoye(e2.text)
            except:
                pass

            surface_chambre10=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bedroomDescription-10Area"}).td
                surface_chambre10=nettoye(e2.text)
            except:
                pass

            salle_douche=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bathroomDescription-showerRoomCount"}).td
                salle_douche=nettoye(e2.text)
            except:
                pass

            toilette=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bathroomDescription-toiletCount"}).td
                toilette=nettoye(e2.text)
            except:
                pass

            #ajout 09 02 2019
            surface_showroom=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-largeEnterpriseDescription-floorAreaOfShowroom"}).td
                surface_showroom=nettoye(e2.text)
            except:
                pass
            #----------------

            #ajout 14 02 2019 09:40
            buanderie=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-bathroomDescription-hasLaundryRoom"}).td
                buanderie=nettoye(e2.text)
            except:
                pass
            #-----------------

            bureau=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-SMEDescription-studyProperty"}).td
                bureau=nettoye(e2.text)
            except:
                pass

            #ajout 14 02 2019 09:40
            profession_liberale=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-SMEDescription-workSpaceProperty"}).td
                profession_liberale=nettoye(e2.text)
            except:
                pass
            #-----------------

            surface_bureau=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-SMEDescription-studym2"}).td
                surface_bureau=nettoye(e2.text)
            except:
                pass

            #ajout 07 02 2019
            surface_profession_liberale=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-SMEDescription-workSpacem2"}).td
                surface_profession_liberale=nettoye(e2.text)
            except:
                pass

            cave=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-basementAndAtticDescription-hasBasement"}).td
                cave=nettoye(e2.text)
            except:
                pass

            #ajout 07 02 2019
            surface_cave=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-basementAndAtticDescription-basementArea"}).td
                surface_cave=nettoye(e2.text)
            except:
                pass
            #---------------

            #ajout 09 02 2019
            grenier=""
            try:
                e2=soup0.find("tr", {"aria-label":"interior-basementAndAtticDescription-attic"}).td
                grenier=nettoye(e2.text)
            except:
                pass
            #----------------

            largeur_terrain_rue=""
            try:
                e2=soup0.find("tr", {"aria-label":"exterior-landDescription-widthOfPlotToStreet"}).td
                largeur_terrain_rue=nettoye(e2.text)
            except:
                pass

            #ajout 07 02 2019
            profondeur_terrain=""
            try:
                e2=soup0.find("tr", {"aria-label":"exterior-landDescription-depthOfPlot"}).td
                profondeur_terrain=nettoye(e2.text)
            except:
                pass

            orientation=""
            try:
                e2=soup0.find("tr", {"aria-label":"exterior-landDescription-orientationGarden"}).td
                orientation=nettoye(e2.text)
            except:
                pass

            #---------------

            #ajout 09 02 2019
            superficie_du_terrain=""
            try:
                e2=soup0.find("tr", {"aria-label":"exterior-landDescription-surfaceAreaOfPlot"}).td
                superficie_du_terrain=nettoye(e2.text)
            except:
                pass
            #------------------

            raccordement_egout=""
            try:
                e2=soup0.find("tr", {"aria-label":"exterior-landDescription-connectionToSewerNetwork"}).td
                raccordement_egout=nettoye(e2.text)
            except:
                pass

            #ajout 07 02 2019
            gaz_eau_electricite=""
            try:
                e2=soup0.find("tr", {"aria-label":"exterior-landDescription-gasWaterElectricity"}).td
                gaz_eau_electricite=nettoye(e2.text)
            except:
                pass

            jardin=""
            try:
                e2=soup0.find("tr", {"aria-label":"exterior-outdoorDescription-hasGarden"}).td
                jardin=nettoye(e2.text)
            except:
                pass

            surface_jardin=""
            try:
                e2=soup0.find("tr", {"aria-label":"exterior-outdoorDescription-areaOfGarden"}).td
                surface_jardin=nettoye(e2.text)
            except:
                pass

            #--------------

            #ajout 14 02 2019
            orientation_terrasse=""
            try:
                e2=soup0.find("tr", {"aria-label":"exterior-outdoorDescription-orientationTerrace"}).td
                orientation_terrasse=nettoye(e2.text)
            except:
                pass
            #---------------
            terrasse=""
            try:
                e2=soup0.find("tr", {"aria-label":"exterior-outdoorDescription-terrace"}).td
                terrasse=nettoye(e2.text)
            except:
                pass

            surface_terrasse=""
            try:
                e2=soup0.find("tr", {"aria-label":"exterior-outdoorDescription-terracem2"}).td
                surface_terrasse=nettoye(e2.text)
            except:
                pass

            #ajout 07 02 2019
            ascenseur=""
            try:
                e2=soup0.find("tr", {"aria-label":"facilities-commonBuildingDescription-lift"}).td
                ascenseur=nettoye(e2.text)
            except:
                pass
            #-------------

            #ajout 13 02 2019
            acces_handicape=""
            try:
                e2=soup0.find("tr", {"aria-label":"facilities-commonBuildingDescription-disabledAccess"}).td
                acces_handicape=nettoye(e2.text)
            except:
                pass
            #----------------

            piscine=""
            try:
                e2=soup0.find("tr", {"aria-label":"facilities-welnessEquipment-swimmingPool"}).td
                piscine=nettoye(e2.text)
            except:
                pass

            parlophone=""
            try:
                e2=soup0.find("tr", {"aria-label":"facilities-privateEquipment-intercom"}).td
                parlophone=nettoye(e2.text)
            except:
                pass

            alarme=""
            try:
                e2=soup0.find("tr", {"aria-label":"facilities-privateEquipment-secureAccessAlarm"}).td
                alarme=nettoye(e2.text)
            except:
                pass

            #ajout 07 02 2019
            porte_blindee=""
            try:
                e2=soup0.find("tr", {"aria-label":"facilities-privateEquipment-reinforcedDoor"}).td
                porte_blindee=nettoye(e2.text)
            except:
                pass
            #---------------

            permis_batir_obtenu=""
            try:
                e2=soup0.find("tr", {"aria-label":"planning-buildingRegulation-planningPermissionObtained"}).td
                permis_batir_obtenu=nettoye(e2.text)
            except:
                pass

            autorisation_lotissement=""
            try:
                e2=soup0.find("tr", {"aria-label":"planning-buildingRegulation-subdivisionPermit"}).td
                autorisation_lotissement=nettoye(e2.text)
            except:
                pass

            #ajout 07 02 2019
            affectation_urban_recente_denomination_plan=""
            try:
                e2=soup0.find("tr", {"aria-label":"planning-buildingRegulation-latestLandUseDesignation"}).td
                affectation_urban_recente_denomination_plan=nettoye(e2.text)
            except:
                pass
            #-------------------

            droit_preemption_plan_execution_spatial=""
            try:
                e2=soup0.find("tr", {"aria-label":"planning-buildingRegulation-possiblePriorityPurchaseRight"}).td
                droit_preemption_plan_execution_spatial=nettoye(e2.text)
            except:
                pass

            citation_infraction_urbanistique=""
            try:
                e2=soup0.find("tr", {"aria-label":"planning-buildingRegulation-proceedingsForBreachOfPlanningRegulations"}).td
                citation_infraction_urbanistique=nettoye(e2.text)
            except:
                pass

            #ajout 07 02 2019
            information_zones_inondables=""
            try:
                e2=soup0.find("tr", {"aria-label":"planning-buildingRegulation-floodZoneInfo"}).td
                information_zones_inondables=nettoye(e2.text)
            except:
                pass

            loyer_mensuel_demande=""
            try:
                e2=soup0.find("tr", {"aria-label":u"Loyer mensuel demandé"}).td
                loyer_mensuel_demande=nettoye(e2.text)
            except:
                pass
            #-------------

            #ajout 14 02 2019
            loyer_demande=""
            try:
                e2=soup0.find("tr", {"aria-label":u"Loyer demandé"}).td
                loyer_demande=nettoye(e2.text)
            except:
                pass

            loyer_annuel=""
            try:
                e2=soup0.find("tr", {"aria-label":"financial-yearlyRentalPrice"}).td
                loyer_annuel=nettoye(e2.text)
            except:
                pass

            loyer_mensuel=""
            try:
                e2=soup0.find("tr", {"aria-label":"financial-monthlyRentalPrice"}).td
                loyer_mensuel=nettoye(e2.text)
            except:
                pass
            #---------------

            #ajout 07 02 2019
            charge_mensuelle=""
            try:
                e2=soup0.find("tr", {"aria-label":"financial-monthlyCharges"}).td
                charge_mensuelle=nettoye(e2.text)
            except:
                pass

            prix_au_m2=""
            try:
                e2=soup0.find("tr", {"aria-label":"financial-m2Price"}).td
                prix_au_m2=nettoye(e2.text)
            except:
                pass

            revenu_cadastral=""
            try:
                e2=soup0.find("tr", {"aria-label":"financial-cadastralIncome"}).td
                revenu_cadastral=nettoye(e2.text)
            except:
                pass

            prix_demande_hors_droits_enregistrement_hors_frais_notaire=""
            try:
                e2=soup0.find("tr", {"aria-label":"financial-vatProfile-vatIncluded"}).td
                if e2==None:
                    e22=soup0.find(lambda tag:tag.name=="th" and "Prix demandé hors droits d'enregistrement et hors frais de notaire" in tag.text)
                    if e22!=None:
                        prix_demande_hors_droits_enregistrement_hors_frais_notaire="oui"
                else:
                    prix_demande_hors_droits_enregistrement_hors_frais_notaire=nettoye(e2.text)
            except:
                pass

            cpeb_consommation_energetique=""
            try:
                e2=soup0.find("tr", {"aria-label":"energy-energyConsumption"}).td
                cpeb_consommation_energetique=nettoye(e2.text)
            except:
                pass

            #ajout 07 02 2019
            classe_energetique=""
            try:
                e2=soup0.find("th", {"class":"iw-propertypage-verticals-characteristic-value"}).img
                classe_energetique=nettoye(e2["src"])
            except:
                pass

            numero_rapport_cpeb=""
            try:
                e2=soup0.find("tr", {"aria-label":"energy-EPCreferenceNumber"}).td
                numero_rapport_cpeb=nettoye(e2.text)
            except:
                pass

            consommation_theorique_energie_primaire=""
            try:
                e2=soup0.find("tr", {"aria-label":"energy-yearlyTheoreticalTotalEnergyConsumption"}).td
                consommation_theorique_energie_primaire=nettoye(e2.text)
            except:
                pass

            #----------------
            emission_co2=""
            try:
                e2=soup0.find("tr", {"aria-label":"energy-CO2emission"}).td
                emission_co2=nettoye(e2.text)
            except:
                pass

            chauffage=""
            try:
                e2=soup0.find("tr", {"aria-label":"energy-Heating"}).td
                chauffage=nettoye(e2.text)
            except:
                pass

            double_vitrage=""
            try:
                e2=soup0.find("tr", {"aria-label":"energy-doubleGlazing"}).td
                double_vitrage=nettoye(e2.text)
            except:
                pass

            attestation_as_built=""
            try:
                e2=soup0.find("tr", {"aria-label":"energy-buildingRegulation-asBuiltPlan"}).td
                attestation_as_built=nettoye(e2.text)
            except:
                pass

            attestation_conformite_installation_electrique=""
            try:
                e2=soup0.find("tr", {"aria-label":"energy-inspectionReportOfTheElectricalInstallation"}).td
                attestation_conformite_installation_electrique=nettoye(e2.text)
            except:
                pass

            #ajout 07 02 2019
            attestation_conformite_citernes_mazout=""
            try:
                e2=soup0.find("tr", {"aria-label":"energy-conformityCertificationForFuelTanks"}).td
                attestation_conformite_citernes_mazout=nettoye(e2.text)
            except:
                pass

            #--------------

            agence_nom=""
            try:
                e2=soup0.find("td", {"data-label":"name"})
                agence_nom=nettoye(e2.text)
            except:
                pass

            agence_adresse=""
            agence_cp=""
            agence_ville=""
            agence_num_voie=""
            try:
                e2=soup0.find("tr", {"data-label":"iwPropertyPageVerticals.contact.address"})
                agence_element_adresse=e2.contents[3].contents
                agence_adresse_avant=agence_element_adresse[0].strip()
                agence_adresse_apres=agence_element_adresse[2].strip()
                agence_cp=agence_adresse_apres.split(" - ")[0].strip()
                agence_ville=agence_adresse_apres.split(" - ")[1].strip()
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

            agence_agree_ipi=""
            try:
                e2=soup0.find("tr", {"data-label":"iwPropertyPageVerticals.contact.IPI"})
                agence_agree_ipi=nettoye2(e2.contents[3].text)
            except:
                pass

            immoweb_code=""
            try:
                e2=soup0.find("tr", {"data-label":"iwPropertyPageVerticals.contact.immowebReferenceNo"})
                immoweb_code=nettoye2(e2.contents[3].text)
            except:
                pass

            ref_agence=""
            try:
                e2=soup0.find("tr", {"data-label":"iwPropertyPageVerticals.contact.refAgency"})
                ref_agence=nettoye2(e2.contents[3].text)
            except:
                pass

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            tel=""
            disponibilite_tel=""
            fax=""
            disponibilite_fax=""
            mobile=""
            disponibilite_mobile = ""
            try:
                driver.find_element_by_id("pp-section-contact-area-phone-button").click()
                time.sleep(3)
                element_telephone_dispo = driver.find_element_by_xpath("//div[@class='phone']/div[@class='annotation']")
                disponibilite_tel=element_telephone_dispo.text
            except:
                pass

            try:
                element_telephone = driver.find_element_by_xpath("//div[@class='phone']/div[@class='phone']")
                tel=element_telephone.text
            except:
                pass
            try:
                element_fax_dispo = driver.find_element_by_xpath("//div[@class='fax']/div[@class='annotation']")
                disponibilite_fax=element_fax_dispo.text
            except:
                pass

            try:
                element_fax = driver.find_element_by_xpath("//div[@class='fax']/div[@class='phone']")
                fax=element_fax.text
            except:
                pass
            try:
                element_mobile_dispo = driver.find_element_by_xpath("//div[@class='mobile']/div[@class='annotation']")
                disponibilite_mobile=element_mobile_dispo.text
                element_mobile = driver.find_element_by_xpath("//div[@class='mobile']/div[@class='phone']")
                mobile=element_mobile.text
            except:
                pass

            #------------------------
            #-------maj 07/02/2019----
            if z==1:
                rep=rep+"\\"+date2_
                if(os.access(rep,os.F_OK)==False):
                    os.makedirs(rep,777)
                export = open(rep + "\\" + categorie+"_"+str(date_)+".txt", "w")
                export.write("lien_url"+"\t"+"categorie"+"\t"+"bien"+"\t"+"designation"+"\t"+"num_voie"+"\t"+"adresse"+"\t"+"cp"+"\t"+"ville"+"\t"+"prix"+"\t"+"emplacement"+"\t"+"surface"+"\t"+"chambre"+"\t"+"salle_bain"+"\t"+"habitable"+"\t"+"bien_disponible"+"\t"+"date_de_livraison"+"\t"+"disponible_le"+"\t"+"quartier_ou_lieu_dit"+"\t"+"annee_de_construction"+"\t"+"nombre_etage"+"\t"+"nombre_logement"+"\t"+"etat_batiment"+"\t"+"largeur_facade_rue"+"\t"+"nombre_facade"+"\t"+"surface_disponible"+"\t"+"parking_interieur"+"\t"+"parking_exterieur"+"\t"+"environnement"+"\t"+"premiere_occupation"+"\t"+"distance_transport"+"\t"+"distance_ecole"+"\t"+"distance_commerce"+"\t"+"surface_habitable"+"\t"+"feux_ouverts"+"\t"+"porte_d_acces"+"\t"+"porte_de_section"+"\t"+"nombre_piece"+"\t"+"living"+"\t"+"surface_living"+"\t"+"salle_a_manger"+"\t"+"surface_salle_a_manger"+"\t"+"surface_cuisine"+"\t"+"amenagement_cuisine"+"\t"+"teledistribution"+"\t"+"surface_chambre1"+"\t"+"surface_chambre2"+"\t"+"surface_chambre3"+"\t"+"surface_chambre4"+"\t"+"surface_chambre5"+"\t"+"surface_chambre6"+"\t"+"surface_chambre7"+"\t"+"surface_chambre8"+"\t"+"surface_chambre9"+"\t"+"surface_chambre10"+"\t"+"salle_douche"+"\t"+"toilette"+"\t"+"surface_showroom"+"\t"+"buanderie"+"\t"+"bureau"+"\t"+"profession_liberale"+"\t"+"surface_bureau"+"\t"+"surface_profession_liberale"+"\t"+"cave"+"\t"+"surface_cave"+"\t"+"largeur_terrain_rue"+"\t"+"profondeur_terrain"+"\t"+"orientation"+"\t"+"raccordement_egout"+"\t"+"gaz_eau_electricite"+"\t"+"jardin"+"\t"+"surface_jardin"+"\t"+"orientation_terrasse"+"\t"+"terrasse"+"\t"+"surface_terrasse"+"\t"+"ascenseur"+"\t"+"acces_handicape"+"\t"+"piscine"+"\t"+"parlophone"+"\t"+"alarme"+"\t"+"porte_blindee"+"\t"+"permis_batir_obtenu"+"\t"+"autorisation_lotissement"+"\t"+"affectation_urban_recente_denomination_plan"+"\t"+"droit_preemption_plan_execution_spatial"+"\t"+"citation_infraction_urbanistique"+"\t"+"information_zones_inondables"+"\t"+"loyer_mensuel_demande"+"\t"+"loyer_demande"+"\t"+"loyer_annuel"+"\t"+"loyer_mensuel"+"\t"+"charge_mensuelle"+"\t"+"prix_au_m2"+"\t"+"revenu_cadastral"+"\t"+"prix_demande_hors_droits_enregistrement_hors_frais_notaire"+"\t"+"cpeb_consommation_energetique"+"\t"+"classe_energetique"+"\t"+"numero_rapport_cpeb"+"\t"+"consommation_theorique_energie_primaire"+"\t"+"emission_co2"+"\t"+"chauffage"+"\t"+"double_vitrage"+"\t"+"attestation_as_built"+"\t"+"attestation_conformite_installation_electrique"+"\t"+"attestation_conformite_citernes_mazout"+"\t"+"agence_nom"+"\t"+"agence_num_voie"+"\t"+"agence_adresse"+"\t"+"agence_cp"+"\t"+"agence_ville"+"\t"+"agence_agree_ipi"+"\t"+"immoweb_code"+"\t"+"ref_promoteur"+"\t"+"nom_immeuble"+"\t"+"ref_agence"+"\t"+"tel"+"\t"+"disponibilite_tel"+"\t"+"mobile"+"\t"+"disponibilite_mobile"+"\t"+"fax"+"\t"+"disponibilite_fax"+"\t"+"lien_photo"+"\t"+"page"+"\n")
                export.close()

            insertion("table_scrapping_immo",["lien_url","categorie","bien","designation","num_voie","adresse","cp","ville","prix","emplacement","surface","chambre","salle_bain","habitable","bien_disponible","date_de_livraison","disponible_le","quartier_ou_lieu_dit","annee_de_construction","nombre_etage","nombre_logement","etat_batiment","largeur_facade_rue","nombre_facade","surface_disponible","parking_interieur","parking_exterieur","environnement","premiere_occupation","distance_transport","distance_ecole","distance_commerce","surface_habitable","feux_ouverts","porte_d_acces","porte_de_section","nombre_piece","living","surface_living","salle_a_manger","surface_salle_a_manger","surface_cuisine","amenagement_cuisine","teledistribution","surface_chambre1","surface_chambre2","surface_chambre3","surface_chambre4","surface_chambre5","surface_chambre6","surface_chambre7","surface_chambre8","surface_chambre9","surface_chambre10","salle_douche","toilette","surface_showroom","buanderie","bureau","profession_liberale","surface_bureau","surface_profession_liberale","cave","surface_cave","largeur_terrain_rue","profondeur_terrain","orientation","raccordement_egout","gaz_eau_electricite","jardin","surface_jardin","orientation_terrasse","terrasse","surface_terrasse","ascenseur","acces_handicape","piscine","parlophone","alarme","porte_blindee","permis_batir_obtenu","autorisation_lotissement","affectation_urban_recente_denomination_plan","droit_preemption_plan_execution_spatial","citation_infraction_urbanistique","information_zones_inondables","loyer_mensuel_demande","loyer_demande","loyer_annuel","loyer_mensuel","charge_mensuelle","prix_au_m2","revenu_cadastral","prix_demande_hors_droits_enregistrement_hors_frais_notaire","cpeb_consommation_energetique","classe_energetique","numero_rapport_cpeb","consommation_theorique_energie_primaire","emission_co2","chauffage","double_vitrage","attestation_as_built","attestation_conformite_installation_electrique","attestation_conformite_citernes_mazout","agence_nom","agence_num_voie","agence_adresse","agence_cp","agence_ville","agence_agree_ipi","immoweb_code","ref_promoteur","nom_immeuble","ref_agence","tel","disponibilite_tel","mobile","disponibilite_mobile","fax","disponibilite_fax","lien_photo","page","cle"], [lien_url,categorie,bien,designation,num_voie,adresse,cp,ville,prix,emplacement,surface,chambre,salle_bain,habitable,bien_disponible,date_de_livraison,disponible_le,quartier_ou_lieu_dit,annee_de_construction,nombre_etage,nombre_logement,etat_batiment,largeur_facade_rue,nombre_facade,surface_disponible,parking_interieur,parking_exterieur,environnement,premiere_occupation,distance_transport,distance_ecole,distance_commerce,surface_habitable,feux_ouverts,porte_d_acces,porte_de_section,nombre_piece,living,surface_living,salle_a_manger,surface_salle_a_manger,surface_cuisine,amenagement_cuisine,teledistribution,surface_chambre1,surface_chambre2,surface_chambre3,surface_chambre4,surface_chambre5,surface_chambre6,surface_chambre7,surface_chambre8,surface_chambre9,surface_chambre10,salle_douche,toilette,surface_showroom,buanderie,bureau,profession_liberale,surface_bureau,surface_profession_liberale,cave,surface_cave,largeur_terrain_rue,profondeur_terrain,orientation,raccordement_egout,gaz_eau_electricite,jardin,surface_jardin,orientation_terrasse,terrasse,surface_terrasse,ascenseur,acces_handicape,piscine,parlophone,alarme,porte_blindee,permis_batir_obtenu,autorisation_lotissement,affectation_urban_recente_denomination_plan,droit_preemption_plan_execution_spatial,citation_infraction_urbanistique,information_zones_inondables,loyer_mensuel_demande,loyer_demande,loyer_annuel,loyer_mensuel,charge_mensuelle,prix_au_m2,revenu_cadastral,prix_demande_hors_droits_enregistrement_hors_frais_notaire,cpeb_consommation_energetique,classe_energetique,numero_rapport_cpeb,consommation_theorique_energie_primaire,emission_co2,chauffage,double_vitrage,attestation_as_built,attestation_conformite_installation_electrique,attestation_conformite_citernes_mazout,agence_nom,agence_num_voie,agence_adresse,agence_cp,agence_ville,agence_agree_ipi,immoweb_code,ref_promoteur,nom_immeuble,ref_agence,tel,disponibilite_tel,mobile,disponibilite_mobile,fax,disponibilite_fax,lien_photo,page1,cle],local)
            print("insertion {0} '{1}' | '{2}'".format(categorie, bien, page1))
            export = open(rep + "\\" + categorie+"_"+str(date_)+".txt", "a")
            export.write(lien_url+"\t"+categorie+"\t"+bien+"\t"+designation+"\t"+num_voie+"\t"+adresse+"\t"+cp+"\t"+ville+"\t"+prix+"\t"+emplacement+"\t"+surface+"\t"+chambre+"\t"+salle_bain+"\t"+habitable+"\t"+bien_disponible+"\t"+date_de_livraison+"\t"+disponible_le+"\t"+quartier_ou_lieu_dit+"\t"+annee_de_construction+"\t"+nombre_etage+"\t"+nombre_logement+"\t"+etat_batiment+"\t"+largeur_facade_rue+"\t"+nombre_facade+"\t"+surface_disponible+"\t"+parking_interieur+"\t"+parking_exterieur+"\t"+environnement+"\t"+premiere_occupation+"\t"+distance_transport+"\t"+distance_ecole+"\t"+distance_commerce+"\t"+surface_habitable+"\t"+feux_ouverts+"\t"+porte_d_acces+"\t"+porte_de_section+"\t"+nombre_piece+"\t"+living+"\t"+surface_living+"\t"+salle_a_manger+"\t"+surface_salle_a_manger+"\t"+surface_cuisine+"\t"+amenagement_cuisine+"\t"+teledistribution+"\t"+surface_chambre1+"\t"+surface_chambre2+"\t"+surface_chambre3+"\t"+surface_chambre4+"\t"+surface_chambre5+"\t"+surface_chambre6+"\t"+surface_chambre7+"\t"+surface_chambre8+"\t"+surface_chambre9+"\t"+surface_chambre10+"\t"+salle_douche+"\t"+toilette+"\t"+surface_showroom+"\t"+buanderie+"\t"+bureau+"\t"+profession_liberale+"\t"+surface_bureau+"\t"+surface_profession_liberale+"\t"+cave+"\t"+surface_cave+"\t"+largeur_terrain_rue+"\t"+profondeur_terrain+"\t"+orientation+"\t"+raccordement_egout+"\t"+gaz_eau_electricite+"\t"+jardin+"\t"+surface_jardin+"\t"+orientation_terrasse+"\t"+terrasse+"\t"+surface_terrasse+"\t"+ascenseur+"\t"+acces_handicape+"\t"+piscine+"\t"+parlophone+"\t"+alarme+"\t"+porte_blindee+"\t"+permis_batir_obtenu+"\t"+autorisation_lotissement+"\t"+affectation_urban_recente_denomination_plan+"\t"+droit_preemption_plan_execution_spatial+"\t"+citation_infraction_urbanistique+"\t"+information_zones_inondables+"\t"+loyer_mensuel_demande+"\t"+loyer_demande+"\t"+loyer_annuel+"\t"+loyer_mensuel+"\t"+charge_mensuelle+"\t"+prix_au_m2+"\t"+revenu_cadastral+"\t"+prix_demande_hors_droits_enregistrement_hors_frais_notaire+"\t"+cpeb_consommation_energetique+"\t"+classe_energetique+"\t"+numero_rapport_cpeb+"\t"+consommation_theorique_energie_primaire+"\t"+emission_co2+"\t"+chauffage+"\t"+double_vitrage+"\t"+attestation_as_built+"\t"+attestation_conformite_installation_electrique+"\t"+attestation_conformite_citernes_mazout+"\t"+agence_nom+"\t"+agence_num_voie+"\t"+agence_adresse+"\t"+agence_cp+"\t"+agence_ville+"\t"+agence_agree_ipi+"\t"+immoweb_code+"\t"+ref_promoteur+"\t"+nom_immeuble+"\t"+ref_agence+"\t"+tel+"\t"+disponibilite_tel+"\t"+mobile+"\t"+disponibilite_mobile+"\t"+fax+"\t"+disponibilite_fax+"\t"+lien_photo+"\t"+page1+"\n")
            export.close()

            if bien.strip()=="Promotions Maisons" or bien.strip()=="Promotions appartements":
                if bien_disponible!="":
                    try:
                        # element_close=driver.find_element_by_xpath("//div[@class='modal-dialog']/div[@class='modal-content']/modal-header/div[@class='modal-header']/div[@class='close-button x visible-lg-block visible-xlg-block visible-xxlg-block icon--close']")
                        element_close=driver.find_element_by_xpath("//*[@id='newpropertypage']/iw-pp-app/iw-propertypage/iw-modal/modal/div/div/modal-header/div/div[2]")
                        element_close.click()
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
                        element_tables=driver.find_elements_by_xpath("//div[@id='group-section']/span/iw-propertypage-verticals-section-group/div/div/div/table")
                        nombre_tables=len(element_tables)
                        for x in range(nombre_tables):
                            if x==2:
                                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                            element_tables=driver.find_elements_by_xpath("//div[@id='group-section']/span/iw-propertypage-verticals-section-group/div/div/div/table")
                            liste_element_tr=element_tables[x].find_elements_by_xpath("./tbody/tr")
                            nombre_tr=len(liste_element_tr)-1
                            for xx in range(nombre_tr):
                                if xx==8:
                                    pass
                                try:
                                    element_verif_vendu=element_tables[x].find_element_by_xpath("./tbody/tr["+str(xx+2)+"]/td/span[text()='Vendu']")
                                    continue
                                except:
                                    pass

                                prix=""
                                try:
                                    element_prix2=element_tables[x].find_element_by_xpath("./tbody/tr["+str(xx+2)+"]/td[@class='click']")
                                    prix=nettoye(element_prix2.text)
                                except:
                                    pass

                                #ajout 13 02 2019
                                emplacement=""
                                try:
                                    element_emplacement=element_tables[x].find_element_by_xpath("./tbody/tr["+str(xx+2)+"]/td[3]")
                                    emplacement=nettoye(element_emplacement.text)
                                except:
                                    pass

                                button=element_tables[x].find_element_by_xpath("./tbody/tr["+str(xx+2)+"]/td[@class='buttons']/span[@class='icon--info']")
                                button.click()
                                time.sleep(2)

                                s_script2="return $('#iw-propertypage-verticals-in-modal').html()"
                                html2=driver.execute_script(s_script2)
                                soup2=BeautifulSoup(html2, "lxml")

                                immoweb_code=""
                                try:
                                    e2=soup2.find(lambda tag:tag.name=="b" and "Immoweb code:" in tag.text)
                                    immoweb_code=nettoye(e2.text).replace("|","").replace("Immoweb code:","").strip()
                                except:
                                    pass

                                #ajout 13 02 2019
                                ref_promoteur=""
                                try:
                                    e2=soup2.find(lambda tag:tag.name=="b" and "Ref. Promoteurs:" in tag.text)
                                    ref_promoteur=nettoye(e2.text).replace("|","").replace("Ref. Promoteurs:","").strip()
                                except:
                                    pass

                                nom_immeuble=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"general-buildingDescription-estateName"}).td
                                    nom_immeuble=nettoye(e2.text)
                                except:
                                    pass
                                #----------------

                                annee_de_construction=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"general-buildingDescription-constructionYear"}).td
                                    annee_de_construction=nettoye(e2.text)
                                except:
                                    pass

                                nombre_facade=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"general-buildingDescription-facadeCount"}).td
                                    nombre_facade=nettoye(e2.text)
                                except:
                                    pass

                                parking_exterieur=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"general-parking-outdoorParkingSpaceCount"}).td
                                    parking_exterieur=nettoye(e2.text)
                                except:
                                    pass

                                environnement=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"general-surroundings-surroundingsType"}).td
                                    environnement=nettoye(e2.text)
                                except:
                                    pass

                                premiere_occupation=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"general-newlyBuilt-isFirstOccupation"}).td
                                    premiere_occupation=nettoye(e2.text)
                                except:
                                    pass

                                surface_habitable=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"interior-livingDescription-habitableArea"}).td
                                    surface_habitable=nettoye(e2.text)
                                except:
                                    pass

                                #ajout 14 02 2019 09:40
                                feux_ouverts=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"interior-livingDescription-firePlaceCount"}).td
                                    feux_ouverts=nettoye(e2.text)
                                except:
                                    pass

                                #----------------

                                amenagement_cuisine=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"interior-kitchenDescription-kitchenType"}).td
                                    amenagement_cuisine=nettoye(e2.text)
                                except:
                                    pass

                                chambre=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"interior-bedroomDescription-count"}).td
                                    chambre=nettoye(e2.text)
                                except:
                                    pass

                                salle_bain=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"interior-bathroomDescription-bathroomCount"}).td
                                    salle_bain=nettoye(e2.text)
                                except:
                                    pass

                                toilette=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"interior-bathroomDescription-toiletCount"}).td
                                    toilette=nettoye(e2.text)
                                except:
                                    pass

                                cpeb_consommation_energetique=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"energy-energyConsumption"}).td
                                    cpeb_consommation_energetique=nettoye(e2.text)
                                except:
                                    pass

                                classe_energetique=""
                                try:
                                    e2=soup2.find("th", {"class":"iw-propertypage-verticals-characteristic-value"}).img
                                    classe_energetique=nettoye(e2["src"])
                                except:
                                    pass

                                chauffage=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"energy-Heating"}).td
                                    chauffage=nettoye(e2.text)
                                except:
                                    pass

                                double_vitrage=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"energy-doubleGlazing"}).td
                                    double_vitrage=nettoye(e2.text)
                                except:
                                    pass

                                attestation_as_built=""
                                try:
                                    e2=soup2.find("tr", {"aria-label":"energy-buildingRegulation-asBuiltPlan"}).td
                                    attestation_as_built=nettoye(e2.text)
                                except:
                                    pass

                                insertion("table_scrapping_immo",["lien_url","categorie","bien","designation","num_voie","adresse","cp","ville","prix","emplacement","surface","chambre","salle_bain","habitable","bien_disponible","date_de_livraison","disponible_le","quartier_ou_lieu_dit","annee_de_construction","nombre_etage","nombre_logement","etat_batiment","largeur_facade_rue","nombre_facade","parking_interieur","parking_exterieur","environnement","premiere_occupation","distance_ecole","distance_commerce","surface_habitable","feux_ouverts","porte_d_acces","porte_de_section","nombre_piece","living","surface_living","salle_a_manger","surface_salle_a_manger","surface_cuisine","amenagement_cuisine","teledistribution","surface_chambre1","surface_chambre2","surface_chambre3","surface_chambre4","surface_chambre5","surface_chambre6","surface_chambre7","surface_chambre8","surface_chambre9","surface_chambre10","salle_douche","toilette","surface_showroom","buanderie","bureau","profession_liberale","surface_bureau","surface_profession_liberale","cave","surface_cave","largeur_terrain_rue","profondeur_terrain","orientation","raccordement_egout","gaz_eau_electricite","jardin","surface_jardin","orientation_terrasse","terrasse","surface_terrasse","ascenseur","acces_handicape","piscine","parlophone","alarme","porte_blindee","permis_batir_obtenu","autorisation_lotissement","affectation_urban_recente_denomination_plan","droit_preemption_plan_execution_spatial","citation_infraction_urbanistique","information_zones_inondables","loyer_mensuel_demande","loyer_demande","loyer_annuel","loyer_mensuel","charge_mensuelle","revenu_cadastral","prix_demande_hors_droits_enregistrement_hors_frais_notaire","cpeb_consommation_energetique","classe_energetique","numero_rapport_cpeb","consommation_theorique_energie_primaire","emission_co2","chauffage","double_vitrage","attestation_as_built","attestation_conformite_installation_electrique","attestation_conformite_citernes_mazout","agence_nom","agence_num_voie","agence_adresse","agence_cp","agence_ville","agence_agree_ipi","immoweb_code","ref_promoteur","nom_immeuble","ref_agence","tel","disponibilite_tel","mobile","disponibilite_mobile","fax","disponibilite_fax","lien_photo","page","cle"], [lien_url,categorie,bien,designation,num_voie,adresse,cp,ville,prix,emplacement,surface,chambre,salle_bain,habitable,bien_disponible,date_de_livraison,disponible_le,quartier_ou_lieu_dit,annee_de_construction,nombre_etage,nombre_logement,etat_batiment,largeur_facade_rue,nombre_facade,parking_interieur,parking_exterieur,environnement,premiere_occupation,distance_ecole,distance_commerce,surface_habitable,feux_ouverts,porte_d_acces,porte_de_section,nombre_piece,living,surface_living,salle_a_manger,surface_salle_a_manger,surface_cuisine,amenagement_cuisine,teledistribution,surface_chambre1,surface_chambre2,surface_chambre3,surface_chambre4,surface_chambre5,surface_chambre6,surface_chambre7,surface_chambre8,surface_chambre9,surface_chambre10,salle_douche,toilette,surface_showroom,buanderie,bureau,profession_liberale,surface_bureau,surface_profession_liberale,cave,surface_cave,largeur_terrain_rue,profondeur_terrain,orientation,raccordement_egout,gaz_eau_electricite,jardin,surface_jardin,orientation_terrasse,terrasse,surface_terrasse,ascenseur,acces_handicape,piscine,parlophone,alarme,porte_blindee,permis_batir_obtenu,autorisation_lotissement,affectation_urban_recente_denomination_plan,droit_preemption_plan_execution_spatial,citation_infraction_urbanistique,information_zones_inondables,loyer_mensuel_demande,loyer_demande,loyer_annuel,loyer_mensuel,charge_mensuelle,revenu_cadastral,prix_demande_hors_droits_enregistrement_hors_frais_notaire,cpeb_consommation_energetique,classe_energetique,numero_rapport_cpeb,consommation_theorique_energie_primaire,emission_co2,chauffage,double_vitrage,attestation_as_built,attestation_conformite_installation_electrique,attestation_conformite_citernes_mazout,agence_nom,agence_num_voie,agence_adresse,agence_cp,agence_ville,agence_agree_ipi,immoweb_code,ref_promoteur,nom_immeuble,ref_agence,tel,disponibilite_tel,mobile,disponibilite_mobile,fax,disponibilite_fax,lien_photo,page1,cle],local)
                                print("insertion {0} '{1}' | '{2}'".format(categorie, bien, page1))
                                export = open(rep + "\\" + categorie+"_"+str(date_)+".txt", "a")
                                #export.write(lien_url+"\t"+categorie+"\t"+bien+"\t"+designation+"\t"+num_voie+"\t"+adresse+"\t"+cp+"\t"+ville+"\t"+prix+"\t"+emplacement+"\t"+surface+"\t"+chambre+"\t"+salle_bain+"\t"+habitable+"\t"+bien_disponible+"\t"+date_de_livraison+"\t"+disponible_le+"\t"+quartier_ou_lieu_dit+"\t"+annee_de_construction+"\t"+nombre_etage+"\t"+nombre_logement+"\t"+etat_batiment+"\t"+largeur_facade_rue+"\t"+nombre_facade+"\t"+parking_interieur+"\t"+parking_exterieur+"\t"+environnement+"\t"+premiere_occupation+"\t"+distance_ecole+"\t"+distance_commerce+"\t"+surface_habitable+"\t"+feux_ouverts+"\t"+porte_d_acces+"\t"+porte_de_section+"\t"+nombre_piece+"\t"+living+"\t"+surface_living+"\t"+salle_a_manger+"\t"+surface_salle_a_manger+"\t"+surface_cuisine+"\t"+amenagement_cuisine+"\t"+teledistribution+"\t"+surface_chambre1+"\t"+surface_chambre2+"\t"+surface_chambre3+"\t"+surface_chambre4+"\t"+surface_chambre5+"\t"+surface_chambre6+"\t"+surface_chambre7+"\t"+surface_chambre8+"\t"+surface_chambre9+"\t"+surface_chambre10+"\t"+salle_douche+"\t"+toilette+"\t"+surface_showroom+"\t"+buanderie+"\t"+bureau+"\t"+profession_liberale+"\t"+surface_bureau+"\t"+surface_profession_liberale+"\t"+cave+"\t"+surface_cave+"\t"+largeur_terrain_rue+"\t"+profondeur_terrain+"\t"+orientation+"\t"+raccordement_egout+"\t"+gaz_eau_electricite+"\t"+jardin+"\t"+surface_jardin+"\t"+orientation_terrasse+"\t"+terrasse+"\t"+surface_terrasse+"\t"+ascenseur+"\t"+acces_handicape+"\t"+piscine+"\t"+parlophone+"\t"+alarme+"\t"+porte_blindee+"\t"+permis_batir_obtenu+"\t"+autorisation_lotissement+"\t"+affectation_urban_recente_denomination_plan+"\t"+droit_preemption_plan_execution_spatial+"\t"+citation_infraction_urbanistique+"\t"+information_zones_inondables+"\t"+loyer_mensuel_demande+"\t"+loyer_demande+"\t"+loyer_annuel+"\t"+loyer_mensuel+"\t"+charge_mensuelle+"\t"+revenu_cadastral+"\t"+prix_demande_hors_droits_enregistrement_hors_frais_notaire+"\t"+cpeb_consommation_energetique+"\t"+classe_energetique+"\t"+numero_rapport_cpeb+"\t"+consommation_theorique_energie_primaire+"\t"+emission_co2+"\t"+chauffage+"\t"+double_vitrage+"\t"+attestation_as_built+"\t"+attestation_conformite_installation_electrique+"\t"+attestation_conformite_citernes_mazout+"\t"+agence_nom+"\t"+agence_num_voie+"\t"+agence_adresse+"\t"+agence_cp+"\t"+agence_ville+"\t"+agence_agree_ipi+"\t"+immoweb_code+"\t"+ref_promoteur+"\t"+nom_immeuble+"\t"+ref_agence+"\t"+tel+"\t"+disponibilite_tel+"\t"+mobile+"\t"+disponibilite_mobile+"\t"+fax+"\t"+disponibilite_fax+"\t"+lien_photo+"\t"+page1+"\n")
                                export.write(lien_url+"\t"+categorie+"\t"+bien+"\t"+designation+"\t"+num_voie+"\t"+adresse+"\t"+cp+"\t"+ville+"\t"+prix+"\t"+emplacement+"\t"+surface+"\t"+chambre+"\t"+salle_bain+"\t"+habitable+"\t"+bien_disponible+"\t"+date_de_livraison+"\t"+disponible_le+"\t"+quartier_ou_lieu_dit+"\t"+annee_de_construction+"\t"+nombre_etage+"\t"+nombre_logement+"\t"+etat_batiment+"\t"+largeur_facade_rue+"\t"+nombre_facade+"\t"+surface_disponible+"\t"+parking_interieur+"\t"+parking_exterieur+"\t"+environnement+"\t"+premiere_occupation+"\t"+distance_transport+"\t"+distance_ecole+"\t"+distance_commerce+"\t"+surface_habitable+"\t"+feux_ouverts+"\t"+porte_d_acces+"\t"+porte_de_section+"\t"+nombre_piece+"\t"+living+"\t"+surface_living+"\t"+salle_a_manger+"\t"+surface_salle_a_manger+"\t"+surface_cuisine+"\t"+amenagement_cuisine+"\t"+teledistribution+"\t"+surface_chambre1+"\t"+surface_chambre2+"\t"+surface_chambre3+"\t"+surface_chambre4+"\t"+surface_chambre5+"\t"+surface_chambre6+"\t"+surface_chambre7+"\t"+surface_chambre8+"\t"+surface_chambre9+"\t"+surface_chambre10+"\t"+salle_douche+"\t"+toilette+"\t"+surface_showroom+"\t"+buanderie+"\t"+bureau+"\t"+profession_liberale+"\t"+surface_bureau+"\t"+surface_profession_liberale+"\t"+cave+"\t"+surface_cave+"\t"+largeur_terrain_rue+"\t"+profondeur_terrain+"\t"+orientation+"\t"+raccordement_egout+"\t"+gaz_eau_electricite+"\t"+jardin+"\t"+surface_jardin+"\t"+orientation_terrasse+"\t"+terrasse+"\t"+surface_terrasse+"\t"+ascenseur+"\t"+acces_handicape+"\t"+piscine+"\t"+parlophone+"\t"+alarme+"\t"+porte_blindee+"\t"+permis_batir_obtenu+"\t"+autorisation_lotissement+"\t"+affectation_urban_recente_denomination_plan+"\t"+droit_preemption_plan_execution_spatial+"\t"+citation_infraction_urbanistique+"\t"+information_zones_inondables+"\t"+loyer_mensuel_demande+"\t"+loyer_demande+"\t"+loyer_annuel+"\t"+loyer_mensuel+"\t"+charge_mensuelle+"\t"+prix_au_m2+"\t"+revenu_cadastral+"\t"+prix_demande_hors_droits_enregistrement_hors_frais_notaire+"\t"+cpeb_consommation_energetique+"\t"+classe_energetique+"\t"+numero_rapport_cpeb+"\t"+consommation_theorique_energie_primaire+"\t"+emission_co2+"\t"+chauffage+"\t"+double_vitrage+"\t"+attestation_as_built+"\t"+attestation_conformite_installation_electrique+"\t"+attestation_conformite_citernes_mazout+"\t"+agence_nom+"\t"+agence_num_voie+"\t"+agence_adresse+"\t"+agence_cp+"\t"+agence_ville+"\t"+agence_agree_ipi+"\t"+immoweb_code+"\t"+ref_promoteur+"\t"+nom_immeuble+"\t"+ref_agence+"\t"+tel+"\t"+disponibilite_tel+"\t"+mobile+"\t"+disponibilite_mobile+"\t"+fax+"\t"+disponibilite_fax+"\t"+lien_photo+"\t"+page1+"\n")
                                export.close()

                                driver.find_element_by_xpath("//*[@id='newpropertypage']/iw-pp-app/iw-propertypage/iw-modal/modal/div/div/modal-header/div/div[2]").click()
                                time.sleep(1)
                    except:
                        pass



            curlocal.execute("update table_recup_liste_a_vendre set traite='o' where idenr="+str(enr["idenr"]))
            local.commit()

        try:
            driver.close()
        except:
            pass

        trace = open("trace_agence.txt", "a")
        trace.write("FIN Scrapping "+categorie+" !"+"\n")
        trace.close()

        #Suppression du fichier .lock
        if os.path.exists('agence.lock')==True:
            os.remove('agence.lock')

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
        if os.path.exists('agence.lock')==True:
            os.remove('agence.lock')

        sys.exit(0)
