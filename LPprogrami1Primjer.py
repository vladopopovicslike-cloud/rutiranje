import datetime as dt
import xlsxwriter
import clarkModul

from openpyxl import load_workbook
from scipy.spatial import distance
import itertools, simplejson, json

import pulp
from collections import defaultdict
from pulp import *
global a_time, broj_reda
import pickle
broj_reda=0
import numpy as np

def izracunaj_rute(klijenti, routes, vehicles, osobine, prebacivanje, rutabroj):
    path_to_cplex = r'C:\Program Files\SCIPOptSuite 7.0.3\bin\scip.exe'
    guests=klijenti
    #print "guests", guests
    a3=dt.datetime.now()
    #print ("a3"+str (a3))
    #print routes
    keys = list(range(len(routes)))  #kljucevi od novog rjecnika ruta. Idu od 0,1,2 do ukupnog broja ruta
    zipbObj = zip(keys, routes)     #spojeni kljucevi i rute, tj lista i klucevi rjecnika routes koji su isto smesteni u listu. (1,((1,2,3),"kombi"))
    dictOfroutes = dict(zipbObj)    #spojene liste pretvorene u rjecnik
    #print keys
    #print dictOfroutes
    

    x = LpVariable.dicts('route', keys, 
                                lowBound = 0,
                                upBound = 1,
                                cat = 'Integer')

    routing_model = LpProblem("Fix Fleet Routing Model", LpMinimize)


    routing_model += LpAffineExpression((x[key],routes[dictOfroutes[key]][1]) for key in keys)

    #routing_model += 1000*LpAffineExpression((x[route],routes[route][1]) for route in routes)>=fcilja
        
    for guest in guests:
        routing_model += LpAffineExpression((x[key],1) for key in keys
                                    if guest in dictOfroutes[key][0]) == 1
    
        
    routing_model += LpAffineExpression((x[key],1) for key in keys)==rutabroj
    
    #for key in keys:
        #routing_model += x[key]*routes[dictOfroutes[key]][8]<=3

    #for route in routes:
        #routing_model += x[route]*routes[route][6] <= 9000
        
    a4=dt.datetime.now()


    ctime=(a4-a3).seconds
    #print ("Zavrseno pravljenje pulp modela. Trajanje:" + str (ctime) )

    #print ("pocinje pulp racunanje")
    a3=dt.datetime.now()

    #pulp.scip_path=r'C:\Program Files\SCIPOptSuite 7.0.3\bin\scip.exe'
    #solver = pulp.CPLEX_CMD(path=path_to_cplex)
    #import pulp.solvers as solvers
    ##routing_model.writeMPS('L1ab.mps')
    #options = ['epgap = 0.25']
    solver=pulp.CPLEX_CMD(msg=True,path=r'C:\Program Files\IBM\ILOG\CPLEX_Studio201\cplex\bin\x64_win64\cplex.exe',timelimit=600)

    #routing_model.solve(solver(options=['set mip tolerances mipgap 0.25']))
    routing_model.solve(solver)
    #print array_1d.value()

    #routing_model.solve(GLPK_PY())
    #routing_model.solve(PULP_GLPK_CMD(msg=1,maxSeconds=240))

    #routing_model.solve(PULP_CBC_CMD(msg=1,fracGap=0.9))
    ##routing_model.solve(PULP_CBC_CMD(msg=1))

    a4=dt.datetime.now()
    ctime=(a4-a3).seconds
    print ("Pulp zavrsen. Trajanje:" + str (ctime) )
    print pulp.LpStatus[routing_model.status]
    
    #if pulp.LpStatus[routing_model.status]=="Infeasible":
        #print ("ponovo cemo")
        #print pulp.value(routing_model.objective)
        #izracunaj_rute(broj_klijenata, routes, vehicles, osobine, prebacivanje, pulp.value(routing_model.objective))
   

    ###Preoblikovanje rezultata

    rute_iz_res=defaultdict(list); broj_ruta=0; broj_ruta_kombia=0; broj_ruta_kamiona_3t=0; broj_ruta_kamiona_7t=0;

    broj_ruta={}
    rute_vozila=defaultdict(list)
    vreme_rute=defaultdict(list)
    
    for v in vehicles:
            j=0
            for key in keys:
                    if v==dictOfroutes[key][1] and x[key].value() > 0:
                            #print v, x[key].value()
                            if prebacivanje==True:
                                #print ("krecem da pretvaram")
                                route1=vrati_brojeve(dictOfroutes[key], osobine)
                                rute_iz_res[route1]=routes[dictOfroutes[key]]

                                j=j+1; 
                                rute_vozila[v].append (route1)
                                broj_ruta [v]=j
                                ##vreme_rute[route1].append (routes[route][6])

                            else:
                                j=j+1;
                                #print key, dictOfroutes[key]
                                rute_vozila[v].append (dictOfroutes[key])
                                broj_ruta [v]=j
                                ##vreme_rute[route].append (routes[route][6])

                                rute_iz_res[dictOfroutes[key]]=routes[dictOfroutes[key]]
                                
            #if j>0:
                    #print "Broj ruta " + str (v) +" je: "+ str (broj_ruta[v])
                    #print rute_vozila[v]
     
    

    #print "GAP", pulp.CPLEX_CMD

    #print ("Given (cll):" + str(br_koleta) + "    Given (kg):" + str(uk_masa))
    #print ("Capacity (cll):" + str(kapaciteti_voznog_parka (vehicles)[0]) + "    Capacity (kg):" + str(kapaciteti_voznog_parka (vehicles)[1]))

    print pulp.LpStatus[routing_model.status]
    print pulp.value(routing_model.objective)


    #if prebacivanje==False:
    #routing_model.writeLP('routing_model3.lp')
    #routing_model.writeMPS('L1.mps')

    #ovo treba nekad poslije vjerovatno za racuanje odstupanja od srednje vrijednsoti za vrijeme na ui
    #array_1d = np.array([x[key].value()*routes[dictOfroutes[key]][8] for key in keys])
    #odstupanje=np.std(array_1d)
    #print odstupanje
    


    return (rute_iz_res, rute_vozila, broj_ruta, 0, pulp.value(routing_model.objective), pulp.LpStatus[routing_model.status])


def printaj_rute(rute_iz_res, osobine, instanca, tip, rute_vozila, broj_ruta, ws3, objective, status, benchmark_broj_ruta,benchmark_objective,ukupnopozineg, pozitivnih,negativnih, kapacitet, taboo, ukupno_mogucih_ruta, calc_time):
    ukupno_ruta=0;ukupno_vreme_rute=0
    for v in broj_ruta:
        ukupno_ruta=ukupno_ruta+broj_ruta[v]
        
        #print "Broj ruta " + str (v) +" je: "+ str (broj_ruta[v])
        for r in rute_vozila[v]:
            #del(rute_iz_res[r][9:])
            #print r
            #print rute_iz_res[r]
            ukupno=rute_iz_res[r][3]
            print "rute",r,rute_iz_res[r]
            print "vremeeee"
            ukupno_vreme_rute=ukupno_vreme_rute+rute_iz_res[r][-1]
            print "vreme", rute_iz_res[r][-1],ukupno_vreme_rute
            #print r, rute_iz_res[r][0],rute_iz_res[r][1],rute_iz_res[r][2]
            #for i in list(r[0]):
                #ukupno=ukupno-osobine[i][0]
                #print i, osobine[i][0], ukupno
         
    razlika_objective=objective-float(benchmark_objective)
    razlika_br_ruta=ukupno_ruta-int(benchmark_broj_ruta)
    print "Ukupno ruta: " + str (ukupno_ruta) + " / " + benchmark_broj_ruta
    print "Objectiv: " + str (objective) + " / " + benchmark_objective
    procenat=str(round((100*(objective-float(benchmark_objective))/objective),2))
    print "Razlika: " + str (objective-float(benchmark_objective)) + " / " + procenat + "%"
    ws3.append([instanca, tip, objective, benchmark_objective, razlika_objective, procenat, ukupno_ruta, benchmark_broj_ruta, razlika_br_ruta, status, ukupnopozineg, pozitivnih, negativnih, kapacitet, ukupno_vreme_rute, ukupno_mogucih_ruta, calc_time])


def vrati_brojeve (route, osobine):
    route1=[]
    #print ("stara ruta")
    #print route
    for i in route[0]:
        route1.append(osobine[i][4])
    r=tuple(route1)
    r1=route[1]
    r2=(r,r1)
    return r2

def izracunaj_vozila (rute_iz_res, rute_vozila, broj_ruta, vreme_rute, vehicles):

    y = LpVariable.dicts("vehicle",((route,i)for v in broj_ruta for route in rute_vozila[v]  for i in range (1,broj_ruta[v]+1)), 
                                lowBound = 0,
                                upBound = 1,
                                cat = 'Integer')

    z = LpVariable.dicts("vehicle",((v,i) for v in broj_ruta for i in range (1,broj_ruta[v]+1)), 
                                lowBound = 0,
                                upBound = 1,
                                cat = 'Integer')

    size_model = LpProblem("Fleet Size Routing Model", LpMinimize)

    size_model += LpAffineExpression((z[v,i],vehicles[v][5]) for v in broj_ruta for i in range (1,broj_ruta[v]+1))

    for v in broj_ruta:
            for route in rute_vozila[v]:
                    size_model += LpAffineExpression((y[route,i],1) for i in range (1,broj_ruta[v]+1))==1
                         
    for v in broj_ruta:
            for i in range (1,broj_ruta[v]+1):
                    size_model += LpAffineExpression((y[route,i],vreme_rute[route][0])for route in rute_vozila[v]) - 100000*z[v,i]==0
                   

    #fracGap=0.2
    size_model.solve(PULP_CBC_CMD(msg=1))
    print pulp.LpStatus[size_model.status]
    print pulp.value(size_model.objective)

    broj_vozila={}
    for v in broj_ruta:
            broj_vozila[v]=0
            for i in range (1,broj_ruta[v]+1):
                    if z[v,i].value()==1:
                            print v, i
                            broj_vozila[v]=broj_vozila[v]+1
                            for route in rute_vozila[v]:
                                    if y[route,i].value()==1:
                                            print route, rute_iz_res[route][1], rute_iz_res[route][3], rute_iz_res[route][7]
            print broj_vozila[v] 
