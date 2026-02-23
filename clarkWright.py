def racunaj(d,rute_razvoza):
   
    from openpyxl import load_workbook
    #wb = load_workbook(filename = 'D:\Google Drive\Voli_konacno.xlsx');ws = wb['Sheet2']
    import datetime as dt
    from collections import defaultdict
    #print "broj gigantski ruta razvoza sa depom kao ciljem: " + str(len(rute_razvoza))

    class Usteda:
        def __init__ (self, cvori, cvorj,vrednost):
            self.cvori=cvori
            self.cvorj=cvorj
            self.vrednost=vrednost
            
        def __repr__(self):
            return '{}: {} {} {}'.format(self.__class__.__name__,
                                      self.cvori,
                                      self.cvorj,
                                      self.vrednost)
        def __lt__(self, other):
            if hasattr(other, 'vrednost'):
                return self.vrednost > other.vrednost
            
    class Route:
        def __init__ (self, rb, fields, duzina):
            self.rb=rb
            self.fields=fields
            self.duzina=duzina
            
        def __repr__(self):
            return '{}: {} {}'.format(self.__class__.__name__,
                                      self.rb,
                                      self.fields)
        #def __cmp_float__(self, other):
            #if hasattr(other, 'duzina'):
                #return self.duzina.__cmp__(other.duzina)
    class Tabo:
        def __init__ (self, i, k, value,frequency):
            self.i=i
            self.k=k
            self.value=value
            
    red_matrice=len(d) #"red matrice"
    broj_klijenata=len(d)-2 #broj klijenata. -2 je jer ne ulaze nula i 1
    #mora se ici sa 0 u matrici jer poslije priliko 2opt postoji 0 kao clan
    ustede=[]
    #d[1]=[0,1,2,3,4,5,6,7,8,9,10,11,12] to je len(d) je 13. moze se staviti do len(d) jer niz krece od nule. tako da je 12. clan zapravo poslednji u nizu

    for i in range (2, red_matrice):
         for j in range(2,red_matrice):
             if i!=j:
                 vrednost=d[1][j] - d[i][j]
                 ustede.append (Usteda (i,j,vrednost))
                         
    ustede.sort(reverse=True)
    """def brisi_od_desnog_ustede(desni):
        for u in ustede:
            if u.cvorj==desni:
                ustede.remove (u) 

    def brisi_od_lijevog_ustede(lijevi):
        for u in ustede:
            if u.cvori==lijevi:
                ustede.remove (u)
    def brisi (cvoru_u):
        for u in ustede:
            if u.cvori==cvoru_u or u.cvorj==cvoru_u
            ustede.remove (u)"""
    def izracunaj_duzinu (fields):
        zbir=0
        # ako imamo niz 5,6,7,8,3 len je 5. cetvrti clan niza je broj 3. ako je len-1 i uzim 3 element za poslednju vrednost a to je 8. 
        # stavljeno -2 umjesto -1 da se ne bi racunao povratak u bazy. tako da ukupna duzina rute ne uzima u obzir put do baze iako se pise..
        #   ..da se zavrsava u bazi tj. u 1.
        for i in range(0,len(fields)-1):
                zbir=zbir+d[fields[i]][fields[i+1]]
        return zbir


    cw_ruta=[]
    cw_ruta.append(ustede[0].cvori);cw_ruta.append(ustede[0].cvorj)
   
    while len (cw_ruta)<broj_klijenata:
        #print "idem iznova"
        for u in ustede:
            #print "usteda", u
            if u.cvori==cw_ruta[-1]:
                if u.cvorj not in cw_ruta:
                    #print "cvorj", u.cvorj
                    cw_ruta.append(u.cvorj)
                    #print "1", cw_ruta
                    break
            elif u.cvorj==cw_ruta[0]:
                if u.cvori not in cw_ruta:
                    #print "cvori", u.cvori
                    #print "dadada", [u.cvori],cw_ruta
                    cw_ruta=[u.cvori] + cw_ruta
                    #print "2", cw_ruta
                    break
                #else: ustede.remove(u)
                #print "obrisao", u ne moye jer se pomjeri sledeca usteda i onda je preskoci
    cw_ruta=[1] + cw_ruta
    cw_duzina=izracunaj_duzinu(cw_ruta)
    #print cw_ruta, cw_duzina
            
    global solution, t

    def twoOptSwap_saduzinom(fields, i, k):
        newFields = fields[:]
        #print i,k,fields[i],fields[k] 
        #print "fields1:", newFields[i-1:k+2]
        duzina1=izracunaj_duzinu (newFields[i-1:k+2])
        # ne ukljucuje i broj na poziciji k+2, i-1 kaze da uzima od jednog broja prije i, a k+2 do jednog broja poslije k
        newFields[i:k+1] = fields[k:i-1:-1]
        # prvi dio ide od i do k, a drugi od k do i. stavljeno je i-1 da bi upalo i
        #ovo -1 znaci da se broj unazad, pa onda može da se stavi npr a[6:3:-1], a ne bi moglo samo a[6:3]
        #primjer a=[1,2,3,4,5,6,7,8], i=3, i=6, dobije se a=[1, 2, 3, 7, 6, 5, 4, 8]
        #print "fields2:", newFields[i-1:k+2]
        duzina2=izracunaj_duzinu (newFields[i-1:k+2])
        #print "duzina2-duzina1", duzina2, duzina1
        razlika=duzina1-duzina2
        return newFields,razlika


    solution=Route(1,cw_ruta+[0],cw_duzina)
    
    #print "solution", solution, solution.duzina
    #print "kw", cw_ruta,cw_duzina
    
    rute_razvoza[tuple(cw_ruta)]=[round (cw_duzina+d[cw_ruta[-1]][1],2),round (cw_duzina,2),2]

    end_raz=max(5,round((broj_klijenata)/4.5))
    brojac_raz=end_raz-3
    brcv_uruti= len(cw_ruta+[0])

    #t =  [[0 for x in range(brcv_uruti)] for y in range(brcv_uruti)] #vrijednost tabua
    tlong =  [[0 for x in range(brcv_uruti)] for y in range(brcv_uruti)]

    def tabu_deo (fields, duzina, zadato, iterator, t1, t2, rute_razvoza,  tlong1):
            global solution,currentbestRoute,t
            steta=zadato
            provera=False
            brojrute=-1;iterator=iterator
            najrazlika=0

            for i in range(0, brcv_uruti-1):
                for k in range(i + 2, brcv_uruti-1):
                    brojrute = brojrute+1
                    #ovo je za asimetricnu
                    tos, razlika_nova=twoOptSwap_saduzinom(fields, i+1, k)
                    ##tos=twoOptSwap(fields, i+1, k)
                    tos5=tos[:-1]
                    ##razlika=(duzina-gain)- solution.duzina
                    #i ovo
                    razlika=(duzina-razlika_nova)- solution.duzina

                    if razlika <najrazlika:
                        #print "too",tos5,rute_razvoza
                        if tuple(tos5) not in rute_razvoza:
                                provera=True
                                tosnaj=tos
                                inaj=fields[i+1]
                                knaj=fields[k]
                                najduzina=duzina-razlika_nova
                                najrazlika=razlika

                    elif provera==False:
                      if razlika + tlong[fields[i+1]][fields[k]] < steta:
                        if t[fields[i+1]][fields[k]]==0:
                            
                            if tuple(tos5) not in rute_razvoza:
                                steta=razlika + tlong[fields[i+1]][fields[k]]
                                sinaj=fields[i+1]
                                sknaj=fields[k]
                                stosnaj=tos
                                                                                                                                                                                   
            if provera==True:
                    currentbestRoute=Route(brojrute,tosnaj,najduzina)
                    solution=currentbestRoute
                    
                    for i in range(1, brcv_uruti):
                            for k in range(1, brcv_uruti):
                                  if t[fields[i]][fields[k]]>0:
                                        t[fields[i]][fields[k]]=t[fields[i]][fields[k]]-1
 
                    tlong[knaj][inaj]+=5000;tlong[inaj][knaj]+=5000
                    t[knaj][inaj]=t1 ;t[inaj][knaj]=t2
                     
                    iterator=iterator+1
                    tabu_deo (solution.fields,solution.duzina, 50000000000000, iterator, t1, t2, rute_razvoza, tlong1)
                    
            elif iterator<=broj_klijenata:
                    
                    nova_duzina=solution.duzina+steta
                    currentbestRoute=Route(brojrute,stosnaj,nova_duzina)
                    #ovdje moze da ide do brcv_uruti, jer je fields=cw_ruta+[0], kao i brcv_uruti= len(cw_ruta+[0]), pa onda to poslednje mjesto uzme 0.
                    #Tamo kod povrata nije bilo isto i zato se moralo ostaviti len(fields). Jer je fields bio fields=cw_ruta, a brcv_uruti= len(cw_ruta+[0])
                    # i onda nije moglo da se u fields listi trazi clan koji brcv_uruti-1, jer nije postojao. Zato je tu ostavljeno da brcv_uruti= len(cw_ruta+[0])
                    # jer se moralo zbog maksimalne vrijednosti u fieldsu.
                    for i in range(1, brcv_uruti):
                        for k in range(1, brcv_uruti):
                            if t[fields[i]][fields[k]]>0:
                                t[fields[i]][fields[k]]=t[fields[i]][fields[k]]-1
                    tlong[sknaj][sinaj]+=5000;tlong[sinaj][sknaj]+=5000
                    t[sknaj][sinaj]=t1 ;t[sinaj][sknaj]=t2
                    #print "elif", iterator, t1,t2

                    iterator=iterator+1
                    tabu_deo (currentbestRoute.fields,currentbestRoute.duzina, 50000000000000, iterator, t1, t2, rute_razvoza, tlong1)
 
    while not brojac_raz>end_raz:
        try:
                t =  [[0 for x in range(brcv_uruti)] for y in range(brcv_uruti)]
                tlong1=tlong
                tabu_deo (cw_ruta+[0],cw_duzina, 500000000000000000,0,brojac_raz,brojac_raz, rute_razvoza,tlong1)
                #print "novi taboooooo:", brojac_raz,solution.duzina
        except Exception as e:
                print(e)
                #print ("except razvozne")
                #tabu_deo (solution.fields,solution.duzina, 50000000000000, 0, brojac_raz, brojac_raz, rute_razvoza, tlong1)

        sfr=[solution.fields]
        sf=solution.fields[:-1]
        sf_reverse=solution.fields [1:]
        sf_r=sf_reverse[::-1]
        #print sf
        rute_razvoza[tuple(sf)]=[round (solution.duzina+d[sf[-1]][1],2),round (solution.duzina,2),2]
        brojac_raz+=1
        solution=Route(1,cw_ruta+[0],cw_duzina)

    #print "ukupan broj gigantskih ruta razvoza sa i bez depoom kao ciljem: " + str(len(rute_razvoza))
    #print rute_razvoza
    return (rute_razvoza)


"""
    f = open('D:\Google Drive\sf', 'w')
    simplejson.dump(sf, f)
    f.close()
"""




    
            
             
