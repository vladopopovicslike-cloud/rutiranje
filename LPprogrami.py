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


def izracunaj_rute(broj_klijenata, routes, vehicles, osobine, prebacivanje, rutabroj):
    path_to_cplex = r'C:\Program Files\SCIPOptSuite 7.0.3\bin\scip.exe'
    guests=range (2,broj_klijenata+1)
    a3=dt.datetime.now()
    #print ("a3"+str (a3))

    x = LpVariable.dicts('route', routes.keys(), 
                                lowBound = 0,
                                upBound = 1,
                                cat = 'Integer')

    routing_model = LpProblem("Fix Fleet Routing Model", LpMinimize)


    routing_model += 1000*LpAffineExpression((x[route],routes[route][1]) for route in routes)

    #routing_model += 1000*LpAffineExpression((x[route],routes[route][1]) for route in routes)>=fcilja
        
    for guest in guests:
        routing_model += LpAffineExpression((x[route],1) for route in routes
                                    if guest in route[0]) == 1
        
    #routing_model += LpAffineExpression((x[route],1) for route in routes)==rutabroj

    ##for route in routes:
        ##routing_model += x[route]*routes[route][6] <= 100000
        
    a4=dt.datetime.now()


    ctime=(a4-a3).seconds
    #print ("Zavrseno pravljenje pulp modela. Trajanje:" + str (ctime) )

    #print ("pocinje pulp racunanje")
    a3=dt.datetime.now()

    #pulp.scip_path=r'C:\Program Files\SCIPOptSuite 7.0.3\bin\scip.exe'
    #solver = pulp.CPLEX_CMD(path=path_to_cplex)
    #import pulp.solvers as solvers
    #routing_model.writeMPS('L1a.mps')
    solver = PULP_CBC_CMD(msg=1)
    routing_model.solve(solver)
    #routing_model.solve(GLPK_PY())
    #routing_model.solve(PULP_GLPK_CMD(msg=1,maxSeconds=240))

    #routing_model.solve(PULP_CBC_CMD(msg=1,fracGap=0.9))

    a4=dt.datetime.now()
    ctime=(a4-a3).seconds
    #print ("Pulp zavrsen. Trajanje:" + str (ctime) )
        #print LpStatus[routing_model.status]
    
        #if LpStatus[routing_model.status]=="Infeasible":
        #print ("ponovo cemo")
        #print pulp.value(routing_model.objective)
        #izracunaj_rute(broj_klijenata, routes, vehicles, osobine, prebacivanje, pulp.value(routing_model.objective))
   

    ###Preoblikovanje rezultata



    rute_iz_res=defaultdict(list); broj_ruta=0; broj_ruta_kombia=0; broj_ruta_kamiona_3t=0; broj_ruta_kamiona_7t=0;
    r_sve=[];r_sve_na_jednoj=[]
    num_of_vehicles={'kombi': 0, 'kamion_3.5t': 0, 'kamion_7t': 0}
    num_of_routes={'kombi': 0, 'kamion_3.5t': 0, 'kamion_7t': 0}

    suma_vremena=0 
    for route in routes:
        r=[]
        if x[route].value() == 1.0:
                                
            ##suma_vremena=suma_vremena + routes[route][6]           
            num_of_routes[route[1]]=num_of_routes[route[1]]+1
            #print (str(route)+str(vehicles[route[1]][0])+str(routes[route])+str(routes[route][7])+str(routes[route][8]))
            r_sve.append(1)
            for i in route[0]:
                    r.append(i)
                    r_sve.append(i)
                    
            if prebacivanje==True:
                    route1=vrati_brojeve(route, osobine)
                    rute_iz_res[route1]=routes[route]
                    #print ("prebacivanje")
                    #print  route
                    #print rute_iz_res
            else:
                    rute_iz_res[route]=routes[route]
                    
            broj_ruta=broj_ruta+1
            if route[1]== "kombi":
                    broj_ruta_kombia=broj_ruta_kombia + 1
            if route[1]== "kamion_3.5t":
                    broj_ruta_kamiona_3t=broj_ruta_kamiona_3t + 1
            if route[1]== "kamion_7t":
                    broj_ruta_kamiona_7t=broj_ruta_kamiona_7t + 1

    #print pulp.value(routing_model.objective)
    #print ("suma vremena")
    #print suma_vremena
                           
    r_sve.append(1)
    r_sve_na_jednoj.append(r_sve)

    #print "The choosen routes are " + str (broj_ruta) +"out of a total of %s:"%len(routes)
    #print "Broj ruta kombija " + str (broj_ruta_kombia) + "ili" + str (num_of_routes["kombi"])
    #print "Broj ruta kamiona3.5t " + str (broj_ruta_kamiona_3t)+ "ili"  + str (num_of_routes["kamion_3.5t"])
    #print "Broj ruta kamiona7t " + str (broj_ruta_kamiona_7t) + "ili" + str (num_of_routes["kamion_7t"])

    broj_ruta={}
    rute_vozila=defaultdict(list)
    vreme_rute=defaultdict(list)
    
    for v in vehicles:
            j=0
            for route in routes:
                    if v==route[1] and x[route].value() > 0:
                            if prebacivanje==True:
                                #print ("krecem da pretvaram")
                                route1=vrati_brojeve(route, osobine)

                                j=j+1; 
                                rute_vozila[v].append (route1)
                                broj_ruta [v]=j
                                ##vreme_rute[route1].append (routes[route][6])

                            else:
                                j=j+1; 
                                rute_vozila[v].append (route)
                                broj_ruta [v]=j
                                ##vreme_rute[route].append (routes[route][6])
            #if j>0:
                    #print "Broj ruta " + str (v) +" je: "+ str (broj_ruta[v])
                    #print rute_vozila[v]
     
    

    #print pulp.LpSolverDefault.fracGap

    #print ("Given (cll):" + str(br_koleta) + "    Given (kg):" + str(uk_masa))
    #print ("Capacity (cll):" + str(kapaciteti_voznog_parka (vehicles)[0]) + "    Capacity (kg):" + str(kapaciteti_voznog_parka (vehicles)[1]))

    #print LpStatus[routing_model.status]
    #print pulp.value(routing_model.objective)

    #if prebacivanje==False:
    #routing_model.writeLP('routing_model3.lp')
    #routing_model.writeMPS('L1.mps')

    return (rute_iz_res, rute_vozila, broj_ruta, 0, pulp.value(routing_model.objective), LpStatus[routing_model.status])

def printaj_rute(rute_iz_res, osobine, instanca, tip, rute_vozila, broj_ruta, ws3, objective, status, benchmark_broj_ruta,benchmark_objective,ukupnopozineg, pozitivnih,negativnih, kapacitet, taboo, taboo_pov, calc_time):
    ukupno_ruta=0
    for v in broj_ruta:
        ukupno_ruta=ukupno_ruta+broj_ruta[v]
        #print("Broj ruta " + str(v) +" je: "+ str(broj_ruta[v]))
        for r in rute_vozila[v]:
            print(r)
            print(rute_iz_res[r])
            ukupno=rute_iz_res[r][3]
            #print r, rute_iz_res[r][1],rute_iz_res[r][3],rute_iz_res[r][7]
            for i in list(r[0]):
                ukupno=ukupno-osobine[i][0]
                #print(i, osobine[i][0], ukupno)
         
    razlika_objective=objective-float(benchmark_objective)
    razlika_br_ruta=ukupno_ruta-int(benchmark_broj_ruta)
    print("Ukupno ruta: " + str(ukupno_ruta) + " / " + benchmark_broj_ruta)
    print("Objectiv: " + str(objective) + " / " + benchmark_objective)
    procenat=str(round((100*(objective-float(benchmark_objective))/objective),2))
    print("Razlika: " + str(objective-float(benchmark_objective)) + " / " + procenat + "%")
    ws3.append([instanca, tip, objective, benchmark_objective, razlika_objective, procenat, ukupno_ruta, benchmark_broj_ruta, razlika_br_ruta, status, ukupnopozineg, pozitivnih, negativnih, kapacitet, taboo, taboo_pov, calc_time])


def vrati_brojeve (route, osobine):
    route1=[]
    #print("stara ruta")
    #print(route)
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
    print(LpStatus[size_model.status])
    print(pulp.value(size_model.objective))

    broj_vozila={}
    for v in broj_ruta:
            broj_vozila[v]=0
            for i in range (1,broj_ruta[v]+1):
                    if z[v,i].value()==1:
                            print(v, i)
                            broj_vozila[v]=broj_vozila[v]+1
                            for route in rute_vozila[v]:
                                    if y[route,i].value()==1:
                                            print(route, rute_iz_res[route][1], rute_iz_res[route][3], rute_iz_res[route][7])
            print(broj_vozila[v]) 
