from openpyxl import load_workbook
import itertools, simplejson, json
from collections import defaultdict
import pickle
#import clarkModulPovrat1,noviDodatak5, clarkModulPovrat1novi2,
import clarkWrightPovrat
#clarkModulPovrat1-daje vise gigantskih ruta povrata za jednu povratnu tacku. Dvojka je neka ranija verzija keca
#clarkModulPovrat3-daje tacno jednu gigantsku povratnu za jednu tacku-onu najkracu

def lista_ruta(d1,vector1, broj_klijenata1, fields, br_klijenata_neg):
        end_pov=max(5,round(br_klijenata_neg/5)); brojac_pov=end_pov-3; solutions_list=[];rute_povrata=defaultdict(list)
        
        for i in range(2,len(d1)):
                #t=fields[0]
                #fields[0]=fields[i]
                #fields[i]=t
                # fields dolazi sa prvim clanom koji nije depo tj 1 jer je prilikom pravljenja fields pri racunanju negativne matrice, na kraju
                # zamijenjena mjesta prvom i zadnjem clanu, te je jedinica otisla na kraj. U prvom prolasku se ne mijenja nista.
                # Poslije sa svakim narednim prolaskom druga lokacija biva pocetna, i takav niz onda ulazi u klar koji ne dira prvu i zadnju lokaiju.
                # moze ovako zato sto je prvo i=0 pa ne dolazi do rotiranja prvog clana niza koji je na poziciji jedan. 
                novafields=fields[1:];novafields=novafields[:-1]
                #salje mu kao argument prethodno skupljene rute povrata
                #(rute_povrata)=clarkModulPovrat1novi2.racunaj(d1,vector1, broj_klijenata1, novafields, fields[0],end_pov, rute_povrata)
                (rute_povrata)=clarkWrightPovrat.racunaj(d1,vector1, broj_klijenata1, novafields, i,end_pov, rute_povrata)
                #print "ruta povrata", rute_povrata
                #(ruta,duzina)=clarkModulPovrat.racunaj(d1,vector1, broj_klijenata1, fields, fields[0],brojac_pov,brojac_pov)

                #t=noviDodatak5.izracunaj_trajanje(durations1,ruta)
                #trajanje=round((t/3600000),2)+round(float((len(ruta)*10 + br_koleta1*5 + len(lokacije_istovara)*10)/60),2)
                #print fields[0],fields, novafields
                #print listaRuta
                #for ruta in listaRuta:
                        
                        #print rute_povrata
                #rute_povrata[tuple(ruta)].append(trajanje)
                               
        ##solutions_list.append(rute_povrata)
        ##print solutions_list
         
        ##pickle.dump(solutions_list, open('t.p', 'wb'))
        ##return(solutions_list)
        #print rute_povrata
        #print "ukupan broj gigantskih ruta povrata: " + str(len(rute_povrata))
        return (rute_povrata)
