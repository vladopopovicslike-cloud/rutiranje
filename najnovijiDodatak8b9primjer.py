from pylab import *
import matplotlib.pyplot as plt
import xlsxwriter
from openpyxl import load_workbook
from scipy.spatial import distance
import itertools
#import dijkstra5
import collections 
from collections import defaultdict
import mplleaflet
#import datetime as dt
import datetime as dt
#wb = load_workbook(filename = 'D:\Google Drive\Voli_konacno.xlsx');ws = wb['Sheet2']
# Ovo je varijanta svako sa svakim i sa proračunatim vremenom 
# vremenska granica vr
#3 JE ORIGINALA, 4 SA RJECNIKOM ZA TABOO I 5 JE 3 SA DODATAKOM YA OPTIMIYACIJU RAYVOYNE
#vr=28000

t =  [[0 for x in range(200+1)] for y in range(200+1)]
arbajt=90000;mincll=5.0/60;minfix=10.0/60
global opt_ruta, opt_duzina
def spoji_rute (rute_razvozne, rute_povratne, vehicles, osobine1,osobine2, d,osobine3,vreme_rada,tsv):
    #mj mjerna jedinica za predjeni put ako je 1 onda je metrima, ako je 1000 onda je u km
    mj=1
    vr=vreme_rada
    ukupno1=ukupno2=ukupno3=ukupno4=ukupno5=ukupno6=ukupno7=ukupno8=ukupno9=0; broj1=0; broj2=0
    "ovo je za racunanje proteklog vremena"
    len_rute=len(d)+1
    #len_rute=len(d)+1
    global opt_ruta, opt_duzina
    #cjepkanje velikih povratnih na male
    #sve_male_vozila=defaultdict(list)
    #rute_male=defaultdict(list)
    final_male=defaultdict(list)

    #1 PRIPREMA                
    for vehicle in vehicles:
            #print "MAX NOSIVOST: " + str(vehicles[vehicle][0])
            start_time = dt.datetime.now()
            skup_razvoznih=[]
            recnik_povratnih=defaultdict(list)
            skup_povratnih_svih=defaultdict(list)
             
            for razvozna_tuple in rute_razvozne:
                
                """
                #if razvozna[1]==vehicle:
                razvozna_ruta=[]; razvozna_duzina=0; masa1=0; broj_koleta1=0 
                spisak_klijenata0=[]; dostupnost=0; tkm=0; lokacije_istovara=[]
                broj_koleta=0;ukupna_masa=0;duzina_pov=0; povrat_brk=0; povrat_kg=0; trajanje=1
                nova_dvaopt=[];nova_dvaopt1=[]; nesto=True; p=1
                #print "razzzzzzzzzzz"
                #print razvozna
                """
                #print "velika RAZVOZNA", razvozna_tuple
                m=0;razvozna_ruta=[]; razvozna_duzina=0
                razvozna=list(razvozna_tuple[0])
                #print "tu je", razvozna
                br_klijenata_razvoz=0
                len_razvozne=len(razvozna)+1
                for r in razvozna[1:]:
                    razvozna_ruta=[1]
                    ukupan_brk_razvoz=0
                    ukupan_br_klijenata_razvoz=0
                    razvozna_duzina=0
                    p=1
                    m=m+1
                    for i in razvozna[m:]:
                        brk_iz_xls=osobine1[i][0]
                        #masa_iz_xls=osobine1[i][1]; lokacija=osobine1[i][2]; dostupnost=osobine1[i][3]
                        brk_check_razvoz=ukupan_brk_razvoz+abs(osobine1[i][0])
                        br_klijenata_check_razvoz=ukupan_br_klijenata_razvoz+1
                        ui_vrijeme_razvoz=(brk_check_razvoz*mincll)+(minfix*br_klijenata_check_razvoz)
                        #print "ui_vrijeme_razvoz", ui_vrijeme_razvoz,br_klijenata_check_razvoz
                        #print razvozna_ruta, ui_vrijeme_razvoz
                        if brk_check_razvoz<vehicles[vehicle][0] and ui_vrijeme_razvoz<vr:
                            #razvozna_ruta.append(i)
                            razvozna_ruta.append(osobine1[i][4])
                            razvozna_ruta_set=set(razvozna_ruta)
                            ukupan_brk_razvoz=brk_check_razvoz
                            ukupan_br_klijenata_razvoz=br_klijenata_check_razvoz
                            razvozna_duzina=razvozna_duzina+d[p][osobine1[i][4]]
                            p=razvozna_ruta[-1]
                            #print "ui_vrijeme_razvoz1", ui_vrijeme_razvoz,br_klijenata_check_razvoz
                            #print "razvozna ruta", razvozna_ruta

                            end_time = dt.datetime.now(); razlika=(end_time - start_time).microseconds; ukupno1=ukupno1+razlika
                            #print("1 Duration:",razlika, ukupno1)

    #2 PROVJERA RAZVOZNE DA LI JE VEC UKLJUCENA I UKLJUCIVANJE I SKUP POTECIJALNIH RUTA
                            start_time = dt.datetime.now()
                            if razvozna_ruta_set not in skup_razvoznih:
                                #if razvozna_ruta_set==set([1, 158, 15, 10, 100, 103, 126, 28, 170, 175, 173, 174]):
                                    #print "rrs", razvozna_ruta_set
                                skup_povratnih=[]
                                skup_razvoznih.append(razvozna_ruta_set)
                                
                                tabu_check (razvozna_ruta+[1], razvozna_duzina+d[p][1], d,len_razvozne,2)
                                
                                upisna_ruta_gore=opt_ruta
                                upisna_duzina_gore=opt_duzina
                                upisna_razvozna_duzina_gore=upisna_duzina_gore
                                ui_vrijeme=ui_vrijeme_razvoz
                                #if upisna_ruta_gore not in skup_razvoznih:
                                #skup_razvoznih.append(list(upisna_ruta_gore))
                                #print "BEZ POVRATA",upisna_ruta_gore, upisna_duzina_gore
                                voznja=izracunaj_duzinu (upisna_ruta_gore[:],tsv)/1000/3600
                                trajanje_rute=voznja + ui_vrijeme
                                if trajanje_rute<arbajt:
                                    
                                    final_male[tuple(upisna_ruta_gore[:]),vehicle]=[round(upisna_duzina_gore/mj,2),
                                    round(upisna_duzina_gore/mj,2),0,round(upisna_razvozna_duzina_gore/mj,2),0,
                                    ukupan_brk_razvoz,0,ukupan_brk_razvoz,round(ui_vrijeme,2),ukupan_br_klijenata_razvoz,round(trajanje_rute,2),round(voznja,2)]

                                    end_time = dt.datetime.now(); razlika=(end_time - start_time).microseconds; ukupno2=ukupno2+razlika
                                    #print("2 Duration:",razlika,ukupno2)

    #3 PROVJERA RAZVOZNA SA POCETNOM POVRATNOM DA LI MOZE VREMSKI DA SE UKLOPI
                                    start_time = dt.datetime.now()
                                    for povratna in rute_povratne:            
                                        #ukupna_ruta=[]
                                        #dostupnost=0; tkm=0; lokacije_istovara=[]
                                        #broj_koleta=0;ukupna_masa=0;duzina_pov=0; povrat_brk=0; povrat_kg=0; trajanje=1

                                        lista_povrata=list(povratna)
                                        #lista_povrata=list(povratna[0]) 
                                        #print "povratna", povratna

                                        povratna_ruta=[] 
                                        povratna_duzina=0
                                        #print lista_povrata, lista_povrata[0]          
                                        k=osobine2[lista_povrata[0]][4]
                                                
                                        ukupan_br_klijenata_check=ukupan_br_klijenata_razvoz+1
                                        ukupan_brk_povrat=abs(osobine2[lista_povrata[0]][0])
                                        ukupno_koleta=ukupan_brk_razvoz+ukupan_brk_povrat
                                        ui_vrijeme=ukupno_koleta*mincll+minfix*ukupan_br_klijenata_check
                                                
                                        if ui_vrijeme<vr:
                                                #print "ui_vrijeme sa jednom povratom",ui_vrijeme,ukupno_koleta,ukupan_br_klijenata_check 
                                                ukupan_br_klijenata=ukupan_br_klijenata_check
                                                razvozna_duzina_zaopt=razvozna_duzina+d[razvozna_ruta[-1]][abs(k)]
                                                razvozna_ruta_zaopt=razvozna_ruta+[k]
                                                prvi_povratni=len(razvozna_ruta_zaopt)-1

                                                tabu_check (razvozna_ruta_zaopt, razvozna_duzina_zaopt, d,len_rute,2)
                                                    
                                                upisna_razvozna_ruta=opt_ruta+[1]
                                                upisna_razvozna_duzina=opt_duzina+d[abs(k)][1]
                                                #print "sa pocetnom povratnom",upisna_razvozna_ruta, upisna_razvozna_duzina
                                                #ukupan_br_klijenata=len(upisna_razvozna_ruta)-2
                                                #print upisna_razvozna_ruta,ukupan_br_klijenata
                                                voznja=izracunaj_duzinu (upisna_razvozna_ruta[:],tsv)/1000/3600
                                                trajanje_rute=voznja + ui_vrijeme
                                                if trajanje_rute<arbajt:
                                                    #print "sa početnom povratnom", upisna_razvozna_ruta, ukupan_br_klijenata
                     
                                                    final_male[tuple(upisna_razvozna_ruta[:]),vehicle]=[round(upisna_razvozna_duzina/mj,2),round(upisna_razvozna_duzina/mj,2),prvi_povratni,round(opt_duzina/mj,2),round(d[abs(k)][1]/mj,2),ukupan_brk_razvoz,ukupan_brk_povrat,ukupno_koleta,round(ui_vrijeme,2),ukupan_br_klijenata,round(trajanje_rute,2),round(voznja,2)]
                                                    upisna_razvozna_ruta=upisna_razvozna_ruta[:-2]    
                                                    upisna_razvozna_duzina=upisna_razvozna_duzina - d[abs(upisna_razvozna_ruta[-1])][abs(k)] - d[abs(k)][1]
                                                    #print "razvozna za spajanje",upisna_razvozna_ruta,upisna_razvozna_duzina

                                                    povratna_ruta.append(upisna_razvozna_ruta[-1])
                                                    povratna_ruta.append(k)
                                                    povratna_duzina=d[abs(upisna_razvozna_ruta[-1])][abs(k)]

                                                    upisna_razvozna_ruta=upisna_razvozna_ruta[:-1]
                                                    #print "povratna prije prebacivanja",lista_povrata

                                                    end_time = dt.datetime.now(); razlika=(end_time - start_time).microseconds; ukupno3=ukupno3+razlika
                                                    #print("3 Duration:",razlika,ukupno3)

    #4 PROVJERA POVRATNE DA LI MOZE STATI KOLICINSKI I VREMENSKI
                                                    for j in lista_povrata[1:]:
                                                        start_time = dt.datetime.now()
                                                        #print "povratna",lista_povrata 
                                                        brk_check= ukupan_brk_povrat+abs(osobine2[j][0])
                                                        ukupno_koleta=ukupan_brk_razvoz+brk_check
                                                        ukupan_br_klijenata_check=ukupan_br_klijenata+1
                                                        ui_vrijeme=ukupno_koleta*mincll+minfix*ukupan_br_klijenata_check
                                                            
                                                        #masa_check=ukupna_masa+osobine2[j][1]
                                                        #lokacija_p=osobine2[j][2];dostupnost_p=osobine2[j][3]
                                                        

                                                        if brk_check<=vehicles[vehicle][0] and ui_vrijeme<vr:
                                                                #samo ako ovi uslovi nisu zadovljeni ne dodaje se novi povratni cvor nego se prelazi na sledeci, a pamti se poslednji dodat preko k=povratna_ruta[-1]
                                                                #and masa_check<vehicles[vehicle][3]
                                                                ukupan_br_klijenata=ukupan_br_klijenata_check
                                                                ukupan_brk_povrat=brk_check
                                                                #print "UKUPAAAN KLIJENT I KOLETA",ukupan_br_klijenata,ukupno_koleta, ui_vrijeme
                                                                povratna_ruta.append(osobine2[j][4])
                                                                #print "povratna gore", povratna_ruta
                                                                povratna_duzina=povratna_duzina+d[abs(k)][abs(osobine2[j][4])]
                                                                povratna_ruta_set=set(povratna_ruta)
                                                                #print povratna_ruta,"ui_vrijeme sa svim povratom",ui_vrijeme,ukupno_koleta,ukupan_br_klijenata
                                                                #print "povratna_ruta set", povratna_ruta_set
                                                                end_time = dt.datetime.now(); razlika=(end_time - start_time).microseconds; ukupno4=ukupno4+razlika
                                                                #print("4 Duration:",razlika,ukupno4)
                                                                


    #5 PROVJRA DA LI JE TAKVA POVRATNA VEC BILA I GENERALNO DA LI JE BILA ZA BILO KOJU RAZVOZNU
                                                                start_time = dt.datetime.now()
                                                                #if povratna_ruta[0]==194:
                                                                        #print "upisna razvozna1", povratna_ruta
                                                                if povratna_ruta_set not in skup_povratnih:
                                                                        #ako i trenutna kombinacija se ne dodaje na raavoznu na nju se nastavlja kalemiti sledeci povratni preko k=povratna_ruta[-1]
                                                                        skup_povratnih.append(povratna_ruta_set)
                                                                        #print  povratna_ruta_set  
                                                                        if tuple(povratna_ruta_set) not in skup_povratnih_svih:     
                                                                                pozicija_stara=povratna_ruta.index(osobine2[j][4])
                                                                                #print "povratna", povratna_ruta,osobine2[j][4],pozicija_stara

                                                                                povratna_ruta_zaopt=povratna_ruta+[1]
                                                                                povratna_duzina_zaopt=povratna_duzina + d[abs(osobine2[j][4])][1]

                                                                                tabu_check (povratna_ruta_zaopt, povratna_duzina_zaopt, d,len_rute,3)

                                                                                #if set(povratna_ruta_zaopt)==set([143, 145, -145, -146, 1]):
                                                                                    #print povratna_ruta_zaopt,opt_ruta

                                                                                nova_povratna=opt_ruta
                                                                                nova_povratna_duz=opt_duzina

                                                                                pozicija_nova=opt_ruta.index(osobine2[j][4])
                                                                               
                                                                                #print "opt povratna", opt_ruta, osobine2[j][4],pozicija_nova

                                                                                end_time = dt.datetime.now(); razlika=(end_time - start_time).microseconds; ukupno5=ukupno5+razlika
                                                                                #print("5 Duration:",razlika,ukupno5)
                                                                                

    #6 PROVJERA DA LI SE PROMIJENILA POCETNA POVRTANA
                                                                                start_time = dt.datetime.now()
                                                                                if opt_ruta[1]!=povratna_ruta[1]:
                                                                                        
                                                                                        #print "STAROO", opt_ruta[1],povratna_ruta[1], upisna_razvozna_ruta, opt_ruta[1],upisna_razvozna_duzina,opt_ruta[0],opt_ruta[1]
                                                                                        
                                                                                        tabu_check (upisna_razvozna_ruta + [opt_ruta[0]]+[opt_ruta[1]],upisna_razvozna_duzina+d[abs(opt_ruta[0])][abs(opt_ruta[1])], d,len_rute,4)

                                                                                        upisna_razvozna_ruta1=opt_ruta
                                                                                        upisna_razvozna_duzina1=opt_duzina
                                                                                        #if opt_ruta==[1, 125, 146, 37, 143, 145, -145, -146]:
                                                                                                #print "6", upisna_razvozna_ruta1
                                                                                        
                                                                                        upisna_ruta=upisna_razvozna_ruta1+nova_povratna [2:]
                                                                                        upisna_duzina=upisna_razvozna_duzina1 + nova_povratna_duz - d[abs(nova_povratna[0])][abs(nova_povratna[1])]
                                                                                     
                                                                                        skup_povratnih_svih[tuple(povratna_ruta_set)].append(list(nova_povratna))
                                                                                        recnik_povratnih[tuple(nova_povratna)].append(nova_povratna_duz)
                                                                                        recnik_povratnih[tuple(nova_povratna)].append(ukupan_brk_povrat)
                                                                                        #print "11", upisna_ruta
                                                                                        voznja=izracunaj_duzinu (upisna_ruta[:],tsv)/1000/3600
                                                                                        trajanje_rute= voznja + ui_vrijeme
                                                                                        if trajanje_rute<arbajt:
                                                                                            #print "prvi", upisna_ruta[:],ui_vrijeme
                                                                                            #if upisna_ruta==[1, 125, 146, 37, 143, 145, -145, -146, 1]:
                                                                                                #print "6", upisna_razvozna_ruta1

                                                                                            final_male[tuple(upisna_ruta[:]),vehicle]=[round(upisna_duzina/mj,2),round(upisna_duzina/mj,2),prvi_povratni,round(upisna_razvozna_duzina/mj, 2),round(nova_povratna_duz/mj,2),ukupan_brk_razvoz,ukupan_brk_povrat,ukupno_koleta,round(ui_vrijeme,2), ukupan_br_klijenata,round(trajanje_rute,2), round(voznja,2)]
                                                                                            #print "STARA UPISNA", upisna_ruta, upisna_razvozna_ruta1,nova_povratna,nova_povratna_duz

                                                                                        
                                                                                else:


                                                                                    upisna_ruta=upisna_razvozna_ruta+nova_povratna
                                                                                    upisna_duzina=upisna_razvozna_duzina + nova_povratna_duz
                                                                                 
                                                                                    skup_povratnih_svih[tuple(povratna_ruta_set)].append(list(nova_povratna))
                                                                                    recnik_povratnih[tuple(nova_povratna)].append(nova_povratna_duz)
                                                                                    recnik_povratnih[tuple(nova_povratna)].append(ukupan_brk_povrat)
                                                                                   
                                                                                    #print "ukpna", upisna_ruta,upisna_duzina
                                                                                    voznja=izracunaj_duzinu (upisna_ruta[:],tsv)/1000/3600
                                                                                    trajanje_rute= voznja+ ui_vrijeme
                                                                                    #print "trajanje", trajanje_rute
                                                                                    if trajanje_rute<arbajt:
                                                                                        #print "drugi", upisna_ruta[:],ui_vrijeme
                                                                                        #if upisna_ruta==[1, 125, 146, 37, 143, 145, -145, -146, 1]:
                                                                                            #print "6.1", upisna_razvozna_ruta
                                                                                        final_male[tuple(upisna_ruta[:]),vehicle]=[round(upisna_duzina/mj,2),round(upisna_duzina/mj,2),prvi_povratni,round(upisna_razvozna_duzina/mj,2),round(nova_povratna_duz/mj,2),ukupan_brk_razvoz,ukupan_brk_povrat,ukupno_koleta,round(ui_vrijeme,2), ukupan_br_klijenata,round(trajanje_rute,2), round(voznja,2)]

                                                                                end_time = dt.datetime.now(); razlika=(end_time - start_time).microseconds; ukupno6=ukupno6+razlika
                                                                                #print("6 Duration:",razlika,ukupno6)

    #7 PROVJERA DA LI PROMIJENILA POVRATNA NA BILO KOM MJESTU
                                                                                start_time = dt.datetime.now() 
                                                                                if nova_povratna!=povratna_ruta_zaopt:
                                                                                    ruta=nova_povratna[:-1]
                                                                                    duzina=nova_povratna_duz-d[abs(nova_povratna[-2])][1]
                                                                                    br_koleta=ukupan_brk_povrat
                                                                                    
                                                                                    ruta1=upisna_ruta[:-1]
                                                                                    duzina1=upisna_duzina-d[abs(nova_povratna[-2])][1]
                                                                                    #print "ruta1",ruta1, duzina1, upisna_ruta,duzina, pozicija_nova, pozicija_stara 
                                                                                    
                                                                                    for i in ruta[pozicija_nova:-1]:
                                                                                            
                                                                                        duzina=duzina-d[abs(ruta[-2])][abs(ruta[-1])]+d[abs(ruta[-2])][1];
                                                                                        br_koleta=br_koleta-abs(osobine3["neg",ruta[-1]][0])
                                                                                        #br_koleta=br_koleta-abs(osobine3[ruta[-1]][0]) 
                                                                                        ruta=ruta[:-1]
                                                                                        
                                                                                        duzina1=duzina1-d[abs(ruta1[-2])][abs(ruta1[-1])]+d[abs(ruta1[-2])][1]
                                                                                        ruta1=ruta1[:-1]
                                                                                        ruta2=ruta1+[1]
                                                                                        #print "ruta2",ruta2,duzina1 
                                                                                            
                                                                                        recnik_povratnih[tuple(ruta+[1])].append(duzina)
                                                                                        recnik_povratnih[tuple(ruta+[1])].append(br_koleta)
                                                                                        skup_povratnih_svih[tuple(povratna_ruta_set)].append(list(ruta+[1]))
                                                                                        #print "zapamceno", ruta, duzina
                                                                                        ukupno_koleta=ukupan_brk_razvoz+br_koleta
                                                                                        ukupan_br_klijenata2=len(ruta2)-2
                                                                                        ui_vrijeme=ukupno_koleta*mincll+minfix*ukupan_br_klijenata2
                                                                                        voznja=izracunaj_duzinu (ruta2[:],tsv)/1000/3600
                                                                                        trajanje_rute=voznja + ui_vrijeme
                                                                                        if trajanje_rute<arbajt:
                                                                                            #print "teci", ruta2[:],ui_vrijeme
                                                                                            #if ruta2==[1, 125, 146, 37, 143, 145, -145, -146, 1]:
                                                                                                #print "7",upisna_ruta, povratna_ruta, nova_povratna
                                                                                                
                                                                                            final_male[tuple(ruta2[:]),vehicle]=[round(duzina1/mj,2),round(duzina1/mj,2),prvi_povratni,round(upisna_razvozna_duzina/mj,2),round(duzina/mj,2),ukupan_brk_razvoz,br_koleta,ukupno_koleta,round(ui_vrijeme,2),ukupan_br_klijenata2,round(trajanje_rute,2), round(voznja,2)]

                                                                                        duzina=duzina-d[abs(ruta[-1])][1]
                                                                                        duzina1=duzina1-d[abs(ruta1[-1])][1]
                                                                                    end_time = dt.datetime.now(); razlika=(end_time - start_time).microseconds; ukupno7=ukupno7+razlika
                                                                                #print("7 Duration:",razlika,ukupno7)
                                      
    #8 AKO JE POVRATNA VEC BILA, PROVJERA DA LI SE MIJENJAO NJEN PRVI CLAN 
                                                                                    
                                                                        else:
                                                                                start_time = dt.datetime.now()
                                                                                t=tuple(povratna_ruta_set)
                                                                                #if set(skup_povratnih_svih[t][0])==set([194, -29, -195, -194]):
                                                                                        #print "upisna razvozna1", povratna_ruta, upisna_razvozna_ruta
                                                                                

                                                                                #print "ELSE", skup_povratnih_svih[t][0], povratna_ruta,upisna_razvozna_ruta, skup_povratnih_svih[t][0][1],povratna_ruta[1]
                                                                                if skup_povratnih_svih[t][0][1]!=povratna_ruta[1]:
                                                                                    
                                                                                    nulti=skup_povratnih_svih[t][0][0]
                                                                                    prvi=skup_povratnih_svih[t][0][1]
                                                                                    tabu_check (upisna_razvozna_ruta + [nulti]+[prvi],upisna_razvozna_duzina+d[abs(nulti)][abs(prvi)], d,len_rute,5.1)
                                                                                    #if opt_ruta==[1, 125, 146, 37, 143, 145, -145, -146]:
                                                                                        #print "neki", skup_povratnih_svih[t][0],povratna_ruta,upisna_razvozna_ruta,opt_ruta
                                                                                    
                                                                                    upisna_razvozna_ruta1=opt_ruta
                                                                                    upisna_razvozna_duzina1=opt_duzina
                                                                                    for zap_ruta in skup_povratnih_svih[tuple(povratna_ruta_set)]:
                                                                                        broj1=broj1+1
                                                                                        #print zap_ruta, tuple(povratna_ruta_set), skup_povratnih_svih[tuple(povratna_ruta_set)]
                                                                                        
                                                                                        nov_pov=[upisna_razvozna_ruta1[-2]]+zap_ruta[1:];nov_pov_duz=izracunaj_duzinu(nov_pov,d);len_rute=len(zap_ruta)
                                                                                        
                                                                                        tabu_check (nov_pov,nov_pov_duz, d,len_rute,5.2)
                                                                                        
                                                                                        zap_ruta1=opt_ruta;zap_duzina1=opt_duzina
                                                                                        upisna_ruta=upisna_razvozna_ruta1[:-1]+zap_ruta1[1:]
                                                                                        #recnik_pov_duzina=zap_duzina1-d[zap_ruta1[0]][zap_ruta1[1]]
                                                                                        upisna_duzina=upisna_razvozna_duzina1-d[upisna_razvozna_ruta1[-2]][abs(upisna_razvozna_ruta1[-1])] + zap_duzina1
                                                                                        #if nov_pov_duz!=zap_duzina1:
                                                                                            #print upisna_razvozna_ruta1,upisna_razvozna_duzina1-d[upisna_razvozna_ruta1[-2]][upisna_razvozna_ruta1[-1]],nov_pov, nov_pov_duz, zap_ruta1, zap_duzina1
                                                                                            #print upisna_ruta, upisna_duzina

                                                                                        br_koleta=recnik_povratnih[tuple(zap_ruta)][1]
                                                                                        #print "prvo", upisna_ruta, upisna_duzina
                                                                                        ukupno_koleta=ukupan_brk_razvoz+br_koleta
                                                                                        
                                                                                        ukupno_koleta=ukupan_brk_razvoz+br_koleta
                                                                                        ukupan_br_klijenata3=len(upisna_ruta)-2
                                                                                        ui_vrijeme=ukupno_koleta*mincll+minfix*ukupan_br_klijenata3
                                                                                        #print "ui_vrijeme zapamceno",ui_vrijeme,ukupno_koleta,ukupan_br_klijenata
                                                                                        voznja=izracunaj_duzinu (upisna_ruta[:],tsv)/1000/3600
                                                                                        trajanje_rute= voznja + ui_vrijeme
                                                                                        if trajanje_rute<arbajt:
                                                                                            #print "četvrta", upisna_ruta[:],ui_vrijeme
                                                                                            #if upisna_ruta==[1, 125, 146, 37, 143, 145, -145, -146, 1]:
                                                                                                #print "8", upisna_ruta[:], round(upisna_duzina/1000,2), upisna_razvozna_ruta1,zap_ruta1,zap_duzina1,nov_pov, nov_pov_duz
                                                                                                #print upisna_razvozna_duzina1,upisna_razvozna_ruta1[-2],upisna_razvozna_ruta1[-1], d[upisna_razvozna_ruta1[-2]][upisna_razvozna_ruta1[-1]]
                                                                                            #ovdje se ranije duzina dijelila sa 1000 i zaokruzivala na dvije decimale. i onda kad se saberu ove male u konacno rjesnje, bude manja duzina
                                                                                            final_male[tuple(upisna_ruta[:]),vehicle]=[round(upisna_duzina/mj,2),round(upisna_duzina/mj,2),prvi_povratni,round(upisna_razvozna_duzina1/mj,2),round(nov_pov_duz/mj,2),ukupan_brk_razvoz,br_koleta,ukupno_koleta,round(ui_vrijeme,2),ukupan_br_klijenata3,round(trajanje_rute,2), round(voznja,2)]
                                                                                               

                                                                                    end_time = dt.datetime.now(); razlika=(end_time - start_time).microseconds; ukupno8=ukupno8+razlika
                                                                                    #print("8 Duration:",razlika/1000/60,ukupno8, broj1)

    #9 AKO JE POVRATNA VEC BILA, A NIJE SE MIJENJAO NJEN PRVI CLAN
                                                                                
                                                                                else:
                                                                                    broj2=broj2+1
                                                                                    start_time = dt.datetime.now()
                                                                                    #print "drugo", skup_povratnih_svih[tuple(povratna_ruta_set)]
                                                                                    for zap_ruta in skup_povratnih_svih[tuple(povratna_ruta_set)]:
                                                                                        #print "drugo", zap_ruta, tuple(povratna_ruta_set), skup_povratnih_svih[tuple(povratna_ruta_set)]
                                                                                        upisna_ruta=upisna_razvozna_ruta+zap_ruta
                                                                                        recnik_pov_duzina=recnik_povratnih[tuple(zap_ruta)][0]
                                                                                        upisna_duzina=upisna_razvozna_duzina + recnik_pov_duzina
                                                                                        br_koleta=recnik_povratnih[tuple(zap_ruta)][1]
                                                                                        #print "dolje", upisna_ruta, upisna_razvozna_ruta, zap_ruta, upisna_duzina
                                                                                        ukupno_koleta=ukupan_brk_razvoz+br_koleta
                                                                                        ukupan_br_klijenata4=len(upisna_ruta)-2
                                                                                        ui_vrijeme=ukupno_koleta*mincll+minfix*ukupan_br_klijenata4
                                                                                        #print "ui_vrijeme zapamceno",ui_vrijeme,ukupno_koleta,ukupan_br_klijenata
                                                                                        voznja=izracunaj_duzinu (upisna_ruta[:],tsv)/1000/3600
                                                                                        trajanje_rute= voznja+ ui_vrijeme
                                                                                        if trajanje_rute<arbajt:
                                                                                            #print "peta", upisna_ruta[:],ui_vrijeme
                                                                                            #if upisna_ruta==[1, 125, 146, 37, 143, 145, -145, -146, 1]:
                                                                                                #print "9",upisna_razvozna_ruta,zap_ruta,skup_povratnih_svih[tuple(povratna_ruta_set)],povratna_ruta_set,round(ui_vrijeme,2),round(trajanje_rute,2)
                                                                                            final_male[tuple(upisna_ruta[:]),vehicle]=[round(upisna_duzina/mj,2),round(upisna_duzina/mj,2),prvi_povratni,round(upisna_razvozna_duzina/mj,2),round(recnik_pov_duzina/mj,2),ukupan_brk_razvoz,br_koleta,ukupno_koleta,round(ui_vrijeme,2),ukupan_br_klijenata4,round(trajanje_rute,2), round(voznja,2)]
                                                                                    end_time = dt.datetime.now(); razlika=(end_time - start_time).microseconds; ukupno9=ukupno9+razlika
                                                                                    #print("9 Duration:",razlika/1000/60,ukupno9)

                                                                                

                                                                k=povratna_ruta[-1]

            print "ukupno",ukupno1/1000000, ukupno2/1000000, ukupno3/1000000, ukupno4/1000000, ukupno5/1000000, ukupno6/1000000, ukupno7/1000000, ukupno8/1000000, ukupno9/1000000, broj1,broj2                                                    
    return (final_male, skup_povratnih_svih)

def tabu_check(ruta, duzina, d, len_razvozne,dio):
            end=max(5,round((len(ruta)-1)/4.5))
            br_pokretanja=end-3
            taboo=br_pokretanja
            #if set(ruta)==set([1, 125, 146, 37, 143, 145, -145, -146, 1]):
                #print  1, ruta,dio
            

            #if set(ruta)==set([1, 158, 15, 10, 100, 103, 126, 28, 170, 175, 173, 174, -7,1]):
                #print 2, ruta,dio

            #tlong =  [[0 for x in range(len_razvozne)] for y in range(len_razvozne)]
            #t =  [[0 for x in range(len_razvozne)] for y in range(len_razvozne)]
            #print   "duzina razvozna", len(razvozna)
            iterator=1
            rute_razvoza=[ruta]
            #print "od velike",rute_razvoza
            tlong = t = {}
            for i in ruta:
                for j in ruta:
                    tlong[i,j]=0
                    t[i,j]=0
            tabu_deo(ruta, duzina, ruta, duzina, iterator, taboo, rute_razvoza, tlong, br_pokretanja, t,d,dio)
            #tabu_deo(ruta, duzina, ruta, duzina, iterator, taboo, rute_razvoza, br_pokretanja, d)


def twoOptSwap(fields, i, k):
        newFields = fields[:]
        newFields[i:k+1] = fields[k:i-1:-1]
        return newFields


def twoOptSwap_saduzinom(fields, i, k,d):
        newFields = fields[:]
        duzina1=izracunaj_duzinu (newFields[i-1:k+2],d)
        newFields[i:k+1] = fields[k:i-1:-1]
        duzina2=izracunaj_duzinu (newFields[i-1:k+2],d)
        razlika=duzina1-duzina2
        return newFields,razlika


def tabu_deo (fields, currentbest_duzina, solution_fields, solution_duzina, iterator, taboo, rute_razvoza, tlong, br_pokretanja, t,d,dio):
#def tabu_deo (fields, currentbest_duzina, solution_fields, solution_duzina, iterator, taboo, rute_razvoza, br_pokretanja,d):
            #print "kod taboo",solution_fields, solution_duzina
            global opt_ruta, opt_duzina
            opt_ruta=solution_fields
            opt_duzina=solution_duzina
            najrazlika=0
            steta=500000000
            provera=False
            #print "evo meee", fields
            for i in xrange(0, len(fields)-1):
                for k in xrange(i + 2, len(fields)-1):
                    
                    #gain = c(i, i+1) + c(k, k+1) - c(i, k) - c(i+1, k+1)
                    #gain=d[fields[i]][fields[i+1]]+d[fields[k]][fields[k+1]]-d[fields[i]][fields[k]]-d[fields[i+1]][fields[k+1]]
                    tos, razlika_nova=twoOptSwap_saduzinom(fields, i+1, k,d)
                    #tos=twoOptSwap(fields, i+1, k)
                    #razlika=(currentbest_duzina-gain)- solution_duzina
                    razlika=(currentbest_duzina-razlika_nova)- solution_duzina
                    if razlika<najrazlika:
                        if tos not in rute_razvoza:
                                #print "uslo",razlika,i+1, k, fields,tos
                                provera=True
                                tosnaj=tos
                                inaj=fields[i+1]
                                knaj=fields[k]
                                #najduzina=currentbest_duzina-gain
                                najduzina=currentbest_duzina-razlika_nova
                                najrazlika=razlika
                                #print inaj, knaj
                            
                    
                    elif razlika + tlong[fields[i+1],fields[k]] < steta:
                        #print "razlika kod stete",fields[i+1], fields[k], razlika, t[fields[i+1]][fields[k]],steta
                        if t[fields[i+1],fields[k]]==0:
                        #print "taboo", fields[i+1],fields[k],t[fields[i+1]][fields[k]]
                        #if t[fields[i+1]][fields[k]]==0:
                            if tos not in rute_razvoza:
                                
                                steta=razlika
                                sinaj=fields[i+1]
                                sknaj=fields[k]
                                stosnaj=tos
                                #print sinaj, sknaj, razlika,tlong[fields[i+1]][fields[k]],steta
                                         
                                                                                                                                                                                   
            if provera==True:
                    #print "provera je True. Zamijeni:", inaj, knaj
                    #print "fields",fields, " solution", solution_fields
                    solution_fields=tosnaj
                    solution_duzina=najduzina

                    #for i in xrange(1, len(fields)):
                            #for k in xrange(1, len(fields)):
                    for a in t:
                        if t[a]>0:
                            t[a]=t[a]-1
                                  #if t[fields[i],fields[k]]>0:
                                        #t[fields[i],fields[k]]=t[fields[i],fields[k]]-1
                                        #t[fields[k]][fields[i]]=t[fields[k]][fields[i]]-1
                                        #print "true", fields[i],fields[k],t[fields[i]][fields[k]]

                    tlong[knaj,inaj]+=500;tlong[inaj,knaj]+=500
                    t[knaj,inaj]=taboo ;t[inaj,knaj]=taboo
                     
                    #iterator=iterator+1
                    rute_razvoza.append(solution_fields)
                    #print "sve od",rute_razvoza 
                    opt_ruta=solution_fields
                    opt_duzina=solution_duzina
                    #print "ZAMJENA ",fields,solution_fields,inaj,knaj,  solution_duzina
                    tabu_deo(solution_fields, solution_duzina, solution_fields, solution_duzina, iterator, taboo, rute_razvoza, tlong, br_pokretanja, t,d,dio)
                    
            elif iterator<min(len(fields)-3,2):
            #elif iterator<len(fields)-2:
                #for i in xrange(1, len(fields)):
                        #for k in xrange(1, len(fields)):
                            #if t[fields[i],fields[k]]>0:
                                #t[fields[i],fields[k]]=t[fields[i],fields[k]]-1
                                #t[fields[k]][fields[i]]=t[fields[k]][fields[i]]-1
                                #print "elif", fields[i],fields[k],t[fields[i]][fields[k]]
                for a in t:
                    if t[a]>0:
                        t[a]=t[a]-1

                try:
                    #print "iterator", iterator, fields
                    nova_duzina=solution_duzina+steta
                    currentbest_fields=stosnaj
                    currentbest_duzina=nova_duzina 
                                    
                    #print iterator, "nema provere,zamijeni", sinaj, sknaj,tlong[sknaj][sinaj]
                    tlong[sknaj,sinaj]+=500;tlong[sinaj,sknaj]+=500
                    t[sknaj,sinaj]=taboo ;t[sinaj,sknaj]=taboo
                    
                    iterator=iterator+1
                    tabu_deo(currentbest_fields, currentbest_duzina, solution_fields, solution_duzina, iterator, taboo, rute_razvoza, tlong, br_pokretanja, t,d,dio)

                except Exception as e:
                    print(e)
                    print ("except", solution_fields, dio)
                    tabu_deo(solution_fields, solution_duzina, solution_fields, solution_duzina, iterator, taboo, rute_razvoza, tlong, br_pokretanja, t,d,dio)
            """       
            br_pokretanja=br_pokretanja-1 
            if br_pokretanja>0:
                tlong1=tlong
                t =  [[0 for x in range(len(t))] for y in range(len(t))]
                taboo+=1
                (solution_fields, solution_duzina, solution_fields, solution_duzina, iterator, taboo, rute_razvoza, tlong, tlong1, br_pokretanja, t,d)

            #print ("dole", solution_fields, solution_duzina)      
            #return (solution_fields, solution_duzina)
            """



def twoOptSwap(fields, i, k):
    newFields = fields[:]
    newFields[i:k+1] = fields[k:i-1:-1]
    return newFields

def izracunaj_duzinu (fields,d):
        zbir=0
        # ako imamo niz 5,6,7,8,3 len je 5. cetvrti clan niza je broj 3. ako je len-1 i uzim 3 element za poslednju vrednost a to je 8. 
        for i in range(0,len(fields)-1):
                zbir=zbir+d[abs(fields[i])][abs(fields[i+1])]
        return zbir

