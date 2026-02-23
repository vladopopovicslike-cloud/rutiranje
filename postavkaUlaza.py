from openpyxl import load_workbook
from collections import defaultdict
import xlsxwriter 
import pickle, random
from random import choice

def napravi_semu(randomklijenti,kolona):
    randomklijenti_p=[];kolicina_p={}
    for i in randomklijenti:
        #3 Ako je klijentu dodijeljeno vise od 0 paleta u posmatranom periodu on ulazi u spisak klijenata za taj period
        if kolona[randomklijenti.index(i)]>0:
            randomklijenti_p.append(i)
            #kolicina_p.append(kolona[randomklijenti.index(i)])
            #3 ovdje se pravi lista kolicina za spisak klijenata koji se opsluzuju u posmatranom periodu. Ova dva spiska idu za pravljenje opste matrice i pozitivne 
            kolicina_p[i]=kolona[randomklijenti.index(i)]
    return(randomklijenti_p,kolicina_p)

def napravi_seme_neg(randomklijenti_poz,n):
    randomklijenti_n=defaultdict(list);randomklijenti_n_svi=[];  kolicina_n={};randomklijenti_svi={};
    for k in range(1,4):
        negkolicina={}
        for j in range (n[k]):
            a=choice([i for i in randomklijenti_poz[k] if i not in randomklijenti_n_svi])
            randomklijenti_n[k].append(a)
            negkolicina[-a]=1
            #kolicina_n[k].append(1)
            randomklijenti_n_svi.append(a)
        kolicina_n[k]=negkolicina
        randomklijenti_n[k] =[element*(-1) for element in randomklijenti_n[k]]
        randomklijenti_svi[k] = randomklijenti_poz[k] + randomklijenti_n[k]
    return (randomklijenti_n,kolicina_n, randomklijenti_svi)

def napravi_raspodjelu_od_fje(kolicina, sema_p):
    semav1=defaultdict(list)
    for q in kolicina:
	k=0
	for i in sema_p[q]:
	    semav1[q].append(i-k)
	    k=i
    return semav1

def napravi_posebnu(kolicina, sema, semav, nova_raspodela,ws5):
    semav_posebna=defaultdict(list)
    for q in kolicina:
        k=0;suma={};suma[0]=0;suma[1]=0;suma[2]=0;nova_v={}
        for s in sema[q]:
            for j in range (3):
                if s[j]>0:
                    suma[j]+=semav[q][k]
            k+=1
        #print "suma", q, suma[0], suma[1], suma[2]    
        for j in range (3):
            k=0;nova_v[j]=0
            for s in sema[q]:
                if s[j]>0:
                    #print semav[q][k],suma[j],s[j]
                    nova_v[j]+=semav[q][k]/suma[j]*s[j]
                k+=1
            semav_posebna[q].append(nova_v[j])

    #print "posebna semav", semav_posebna

    suma={};suma[0]=0;suma[1]=0;suma[2]=0
    for j in range (3):
        for q in kolicina:
            #print "sumaj",suma[j] 
            #print j,q,semav_posebna[q][j] 
            suma[j]+=semav_posebna[q][j]*nova_raspodela[q]
        #print suma[j]
    #print suma
    ws5.append(["Paleta po posjeti"])
    ws5.append(["",suma[0],suma[1],suma[2]])
    for q in kolicina:
        ws5.append([q, semav_posebna[q][0], semav_posebna[q][1], semav_posebna[q][2], sum(semav_posebna[q])])
        
    return suma


def posjeta_po_klijentu(kolicina,nova_raspodela, semav,sema, ws5):

    #v[q][j] je suma vjerovatnca svih sema recimo za 2 dnevna narucivanja da ce biti ujutru biti jedno od narucivanja.
    #Te vjerovatnoce za 2 za svaki od tri perioda treba pomnoziti sa vjerovatnocom da ce se pojaviti klijent br. 2
    # Vjerovatnoce sabrati za svaki tip porucivanja za prvi, drugi i treci period. da bi se dobila vjerov porucivanja za jutro, podne i vece

    v = defaultdict(dict);s = defaultdict(dict);v_sum={}
    for q in kolicina:
        for j in range (3):
             v[q][j]=0
             s[q][j]=0

    #rbr je redni broj seme
    for q in kolicina:
        k=0
        for i in sema[q]:
            for j in range (3):
                #print i[j]
                if i[j]>0:
                    v[q][j]+=semav[q][k]
            k+=1
        v_sum[q]=sum(v[q].values())
    for q in kolicina:
        for j in range (3):
            s[q][j]=v[q][j]*nova_raspodela[q]
            
    period={}; udiou_ukupnom={}
    # posjeta po klijentu u periodu [1], 2, 3: max jedna posjeta u jednom periodu
    
    for j in range(3):
        period[j]=0
        for q in kolicina:
            period[j]+=s[q][j]

    ukupno_svi=sum(period.values())            
    for j in range(3):
        udiou_ukupnom[j]=period[j]/ukupno_svi
            
    posjeta_po_klijentu=sum(period.values())
    print "Posjeta po klijentu po tipu i periodu", v,"sumarno", v_sum
    ws5.append(["Posjeta po klijentu po tipu i periodu"])
    ws5.append(["",period[0], period[1], period[2], sum(period.values())])
    for tip in v:
        ws5.append([tip, v[tip][0], v[tip][1], v[tip][2], v_sum[tip]])
    
    return (period, udiou_ukupnom, posjeta_po_klijentu)

def pll_po(sema, semav,raspodela, kolicina, ws5):
    pllpo_periodu={};pll_poklijentu={}; pll_poklijentu_potipu=defaultdict(dict)
    for j in range (3):
        pll_poklijentu[j]=0; pllpo_periodu[j]=0
        for q in kolicina:
            k=0;pll_poklijentu_potipu[q][j]=0
            for s in sema[q]:
                if s[j]>0:
                    #print q, semav[q][k],s[j],raspodela[q],j,k
                    pll_poklijentu[j]+=semav[q][k]*s[j]*raspodela[q]
                    pll_poklijentu_potipu[q][j]+=semav[q][k]*s[j]
                    #print pll_poklijentu[j]
                k+=1
    print "PLL po klijentu, tipu i periodu", pll_poklijentu_potipu

    ws5.append(["Paleta po klijentu po tipu i periodu"])
    ws5.append(["očekivanje", pll_poklijentu[0], pll_poklijentu[1], pll_poklijentu[2], sum(pll_poklijentu.values())])
    
    for tip in pll_poklijentu_potipu:
        ukupno=sum(pll_poklijentu_potipu[tip].values())
        ws5.append([tip, pll_poklijentu_potipu[tip][0], pll_poklijentu_potipu[tip][1], pll_poklijentu_potipu[tip][2], ukupno])

    return(pll_poklijentu)

def raspodelapo(kolicina, sema, semav, raspodela, ws5):
    tip={};tip_pll={};posjeta_tip={}; pllpo_klijentu={};pllpo_klijentu[1]=0;pllpo_klijentu[2]=0;pllpo_klijentu[3]=0
    tip[1]=0;tip[2]=0;tip[3]=0;tip_pll[1]=0;posjeta_tip[1]=0;
    for q in kolicina:
        posjeta_tip[q]=0
    for q in kolicina:
        k=0;tip_pll[q]=0
        for s in sema[q]:
            i=s.count(0)
            j=sum(s)
            tip[3-i]+=semav[q][k]*raspodela[q]
            tip_pll[j]+=semav[q][k]*raspodela[q]
            #pllpo_klijentu[1]+=s[0]*semav[q][k]*raspodela[q]; pllpo_klijentu[2]+=s[1]*semav[q][k]*raspodela[q]; pllpo_klijentu[3]+=s[2]*semav[q][k]*raspodela[q]
            posjeta_tip[j]+=(3-i)*semav[q][k]*raspodela[q]
            k+=1

    ws5.append(["Raspodjela klijenata po broju posjeta i paleta"])
    ws5.append([1, 2, 3, 4, 5, 6, 7, 8])
    ws5.append([tip[1], tip[2], tip[3]])
    ws5.append([tip_pll[1], tip_pll[2], tip_pll[3], tip_pll[4], tip_pll[5], tip_pll[6], tip_pll[7], tip_pll[8]])
    ws5.append([posjeta_tip[1], posjeta_tip[2], posjeta_tip[3], posjeta_tip[4], posjeta_tip[5], posjeta_tip[6], posjeta_tip[7],posjeta_tip[8]]) 
    return (tip, tip_pll)

def promjene_sumarno(kolicina, sema, semav, sema_novo, semav_novo, sema_prob_novo, nova_raspodela,ws5):
    ws5.append(["Promjene"])
    ws5.append(["","Prelaze na novu semu", "Sa manjim br pll", "Sa istim br pll", "Smanjili br posjeta", "Pri manjem br pll", "Pri istom br pll","Isti br posjeta", "Pri manjem br pll", "Pri istom br pll"])
    razlika_posjeta={};u1=0; u2=0; u3=0; u4=0; u5=0; u6=0; u7=0; u8=0; u9=0        
    for q in kolicina:
        #print "seme", sema, semav, sema_novo, semav_novo
        #print q, brojposjeta
        brojposjeta=0;brojposjetanew1=0;brojposjetanew2=0;brojposjetanew3=0;brojposjetanew4=0;brojposjetanew5=0;brojposjetanew6=0; brojpaleta1=0; brojpaleta2=0;
        # brojposjeta po starom, brojposjetanew1 po novom, brojposjetanew2 broj kod kojih se smanjio br posjeta i pll, new3 smanjio se broj posjeta a isit br pll
        # brojpaleta1 -smanjili br posjeta pri manjem br pll; brojpaleta2 -smanjili br posjeta pri istom br pll
        for i in range(len(sema[q])):
            brojposjeta+=(3-sema[q][i].count(0))*semav[q][i]
            for j in range(len(sema_novo[q])):
                if sema_novo[q][j].count(0)>sema[q][i].count(0):
                    brojposjetanew1+=semav_novo[q][j]*semav[q][i]
                    if sum(sema_novo[q][j])<sum(sema[q][i]):
                        brojposjetanew2+=semav_novo[q][j]*semav[q][i]
                    if sum(sema_novo[q][j])==sum(sema[q][i]):
                        brojposjetanew3+=semav_novo[q][j]*semav[q][i]
                else:
                    brojposjetanew4+=semav_novo[q][j]*semav[q][i]
                    if sum(sema_novo[q][j])<sum(sema[q][i]):
                        brojposjetanew5+=semav_novo[q][j]*semav[q][i]
                    #isti broj posjeta i isti br pll, posto nema novog stanja u kome je br posjeta veci
                    if sum(sema_novo[q][j])==sum(sema[q][i]):
                        brojposjetanew6+=semav_novo[q][j]*semav[q][i]
                     
                if sum(sema_novo[q][j])<sum(sema[q][i]):
                        brojpaleta1+=semav_novo[q][j]*semav[q][i]
                if sum(sema_novo[q][j])==sum(sema[q][i]):
                        brojpaleta2+=semav_novo[q][j]*semav[q][i]

        u1+=sema_prob_novo[q][-1]*nova_raspodela[q]; u2+=brojpaleta1*nova_raspodela[q]; u3+=brojpaleta2*nova_raspodela[q]; u4+=brojposjetanew1*nova_raspodela[q]; u5+=brojposjetanew2*nova_raspodela[q]; u6+=brojposjetanew3*nova_raspodela[q]                
        u7+=brojposjetanew4*nova_raspodela[q]; u8+=brojposjetanew5*nova_raspodela[q]; u9+=brojposjetanew6*nova_raspodela[q] 
        brojposjetanew=0
        for i in range(len(sema_novo[q])):
            brojposjetanew+=(3-sema_novo[q][i].count(0))*semav_novo[q][i]
        brojposjetanew+= (1-sum(semav_novo[q]))*brojposjeta     
        #razlika_posjeta[q]=brojposjeta-brojposjetanew
        
        #print "razlika", q,  sema_prob_novo[q][-1], brojpaleta1, brojpaleta2,"",brojposjetanew1, brojposjetanew2,brojposjetanew3
        ws5.append([q, sema_prob_novo[q][-1], brojpaleta1, brojpaleta2, brojposjetanew1, brojposjetanew2, brojposjetanew3, brojposjetanew4, brojposjetanew5, brojposjetanew6])

    
    ws5.append(["sumarno", u1, u2, u3, u4, u5, u6, u7, u8, u9])
    """
    print "sumarno", u1, u2, u3, u4, u5, u6
    print"""
    
def generisanje_sema(broj_s):
    wb = load_workbook('G:\My Drive\postavka.xlsx')
    ws = wb["List1"];ws1 = wb["List2"]; ws2 = wb["List3"]; ws3 = wb["List4"]; ws4 = wb["List5"];ws5 = wb["List6"];
    randomklijenti= random.sample(range(2, 201), 70)
    sema=defaultdict(list);sema_prob=defaultdict(list);sema_novo=defaultdict(list);sema_prob_novo=defaultdict(list);semav=defaultdict(list);semav_novo=defaultdict(list)

    sema[2]=([1,0,1],[1,1,0],[0,1,1]);sema_prob[2]=[0.3,0.9,1]
    sema_novo[2]=[[1,0,0],[2,0,0]];sema_prob_novo[2]=[0.6,0.9]

    sema[3]=([1,1,1],[2,1,0],[2,0,1],[1,2,0]);sema_prob[3]=[0.7,0.8,0.9,1]
    sema_novo[3]=[[1,1,0],[2,1,0]];sema_prob_novo[3]=[0.3,0.5]

    sema[4]=([2,1,1],[1,2,1],[1,1,2]);sema_prob[4]=[0.8,0.9,1]
    sema_novo[4]=[[2,1,0],[2,2,0],[2,0,2],[1,1,1]];sema_prob_novo[4]=[0.2,0.3,0.4,0.5]

    sema[5]=([2,2,1],[2,1,2],[1,2,2]);sema_prob[5]=[0.8,0.9,1]
    sema_novo[5]=[[2,1,1],[2,2,0],[1,2,1]];sema_prob_novo[5]=[0.1,0.2,0.3]

    sema[6]=([2,2,2],[3,2,1],[2,3,1],[1,2,3]);sema_prob[6]=[0.3,0.6,0.9,1]
    sema_novo[6]=[[2,2,1],[2,2,1],[1,2,2]];sema_prob_novo[6]=[0.1,0.2,0.3]

    sema[7]=([3,2,2],[2,3,2],[2,2,3]);sema_prob[7]=[0.4,0.7,1]
    sema_novo[7]=[[2,2,2]];sema_prob_novo[7]=[0.1]

    sema[8]=([3,3,2],[3,2,3],[2,3,3],[4,2,2]);sema_prob[8]=[0.3,0.6,0.9,1]
    sema_novo[8]=[[3,2,2]];sema_prob_novo[8]=[0.1]

    kolicina=[2,3,4,5,6,7,8]
    raspodela=[0.07, 0.64, 0.79, 0.87, 0.93, 0.97, 1.00]

    
    sve_seme=[]

    # nova_raspodela je zapravo prava raspodela, a raspodela je funkcija raspodele
    k=0; nova_raspodela={};j=2
    for i in raspodela:
        nova_raspodela[j]=i-k
        k=i;j+=1

    for inst in range (broj_s):
        print inst
        promjene=defaultdict(list)
        kolicine_sve=[]; kolona1=[]; kolona2=[]; kolona3=[]; kolona1_novo=[]; kolona2_novo=[]; kolona3_novo=[]

        for i in range(len(randomklijenti)):
            random_broj=random.random()
            for j in range(len(raspodela)):
                if random_broj<=raspodela[j]:
                    kolicine_sve.append(kolicina[j])
                    #1 ovdje se svakom broju iz randomklijenti dodaje kojem tipu pripada tj koliko pll dnevno narucuje i to zapisuje u listi kolicine_sve
                    # tako da ako u listi kolicine_sve na nekom mjestu stoji tip 2 onda se to odnosi na klijenta broj taj i taj, na istom rednom mjestu u listi randomklijenti
                    break
        kolicine_sve_kon=kolicine_sve
        #print "kolicine_sve", kolicine_sve
        #promjene[q].append((a,b,c))-a je broj pll u starom stanju, b je broj pll u novom stanju ako se preslo u novo stanje, c je broj pll iz starog stanja prakticno isto kao i a- radi provjere je
        posjetapotipuiper_staro=defaultdict(dict);posjetapotipuiper_novo=defaultdict(dict);pllpotipuiper_staro=defaultdict(dict);pllpotipuiper_novo=defaultdict(dict)
        promjene_posjeta=defaultdict(list)
        for q in kolicina:
            #print "kolicina ", kolicine_sve.count(q);a=0
            k1=[];k2=[];k3=[];k1_novo=[];k2_novo=[];k3_novo=[];brojq=0
            for kol in kolicine_sve:
                if q==kol:
                    brojq=brojq+1
                    rand_broj=random.random()
                    #print sema_prob[q]
                    #print sema[q]
                    for i in range(len(sema_prob[q])):
                        #print "novo i=", i, rand_broj, sema_prob[q][i]
                        if rand_broj<=sema_prob[q][i]:
                            #print i,q,kol,sema[q][i]
                            #2 Ovdje se za svaki dio dana (kolona 1, 2, 3) dodijeljuje koliko pll ide u zavisnosti od tipa klijenta q i izavrane seme medju semama za q
                            #3 u podprogemu napravi seme se definise za svaki period dana koji klijenti se obilaze i koje kolicine im se dostavaljaju
                            kolona1.append(sema[q][i][0]);k1.append(sema[q][i][0])
                            kolona2.append(sema[q][i][1]);k2.append(sema[q][i][1])
                            kolona3.append(sema[q][i][2]);k3.append(sema[q][i][2])
                            a=sum(sema[q][i])
                            a1=sema[q][i].count(0)
                            rand_broj=random.random()
                            provjera=False
                            for j in range(len(sema_prob_novo[q])):
                                #print "novo j=", j
                                if rand_broj<=sema_prob_novo[q][j]:
                                    #print a,q,kol
                                    kolona1_novo.append(sema_novo[q][j][0]);k1_novo.append(sema_novo[q][j][0])
                                    kolona2_novo.append(sema_novo[q][j][1]);k2_novo.append(sema_novo[q][j][1])
                                    kolona3_novo.append(sema_novo[q][j][2]);k3_novo.append(sema_novo[q][j][2])
                                    b=sum(sema_novo[q][j])
                                    b1=sema_novo[q][j].count(0)
                                    promjene[q].append((a,b,0))
                                    promjene_posjeta[q].append((a1,b1,-1))
                                    provjera=True
                                    #print "brak drugi"
                                    ws4.append([q, sema[q][i][0],sema[q][i][1],sema[q][i][2],"novo",sema_novo[q][j][0],sema_novo[q][j][1],sema_novo[q][j][2]]) 
                                    break
                            if provjera==False:
                                kolona1_novo.append(sema[q][i][0]);k1_novo.append(sema[q][i][0])
                                kolona2_novo.append(sema[q][i][1]);k2_novo.append(sema[q][i][1])
                                kolona3_novo.append(sema[q][i][2]);k3_novo.append(sema[q][i][2])
                                c=sum(sema[q][i])
                                c1=sema[q][i].count(0)
                                promjene[q].append((a,0,c))
                                promjene_posjeta[q].append((a1,-1,c1))
                                ws4.append([q, sema[q][i][0],sema[q][i][1],sema[q][i][2],"novo",sema[q][i][0],sema[q][i][1],sema[q][i][2]]) 
                            #print "break prvi"    
                            break
            #print q, promjene_posjeta[q]
                        
            p1=posjetapotipuiper_staro[q][1]=(len(k1)- k1.count(0));p2=posjetapotipuiper_staro[q][2]=(len(k2)- k2.count(0));p3=posjetapotipuiper_staro[q][3]=(len(k3)- k3.count(0))
            p4=posjetapotipuiper_novo[q][1]=(len(k1_novo)- k1_novo.count(0));p5=posjetapotipuiper_novo[q][2]=(len(k2_novo)- k2_novo.count(0));p6=posjetapotipuiper_novo[q][3]=(len(k3_novo)- k3_novo.count(0))
            p7=pllpotipuiper_staro[q][1]=sum(k1);p8=pllpotipuiper_staro[q][2]=sum(k2);p9=pllpotipuiper_staro[q][3]=sum(k3)
            p10=pllpotipuiper_novo[q][1]=sum(k1_novo);p11=pllpotipuiper_novo[q][2]=sum(k2_novo);p12=pllpotipuiper_novo[q][3]=sum(k3_novo)

            ws3.append([q,brojq,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12])
                
        """print"Novi parametri"
        print posjetapotipuiper_staro, "novo", posjetapotipuiper_staro
        print pllpotipuiper_staro, "novo", pllpotipuiper_staro"""

           
        broj_posjeta=defaultdict(list);broj_paleta=defaultdict(list);broj_posjeta_novo=defaultdict(list);broj_paleta_novo=defaultdict(list)

        broj_posjeta[1]=(len(kolona1)- kolona1.count(0)); broj_posjeta[2]=(len(kolona2)- kolona2.count(0)); broj_posjeta[3]=(len(kolona3)- kolona3.count(0))
        broj_paleta[1]=sum(kolona1);broj_paleta[2]=sum(kolona2);broj_paleta[3]=sum(kolona3)

        broj_posjeta_novo[1]=(len(kolona1_novo)- kolona1_novo.count(0)); broj_posjeta_novo[2]=(len(kolona2_novo)- kolona2_novo.count(0)); broj_posjeta_novo[3]=(len(kolona3_novo)- kolona3_novo.count(0))
        broj_paleta_novo[1]=sum(kolona1_novo);broj_paleta_novo[2]=sum(kolona2_novo);broj_paleta_novo[3]=sum(kolona3_novo);

        randomklijenti_poz=defaultdict(list);kolicina_poz=defaultdict(list);kolicina_neg=defaultdict(list)
        randomklijenti_poz_novo=defaultdict(list);kolicina_poz_novo=defaultdict(list);randomklijenti_svi_novo=defaultdict(list)

        (randomklijenti_poz[1],kolicina_poz[1])=napravi_semu(randomklijenti,kolona1)
        (randomklijenti_poz[2],kolicina_poz[2])=napravi_semu(randomklijenti,kolona2)
        (randomklijenti_poz[3],kolicina_poz[3])=napravi_semu(randomklijenti,kolona3)

        (randomklijenti_poz_novo[1],kolicina_poz_novo[1])=napravi_semu(randomklijenti,kolona1_novo)
        (randomklijenti_poz_novo[2],kolicina_poz_novo[2])=napravi_semu(randomklijenti,kolona2_novo)
        (randomklijenti_poz_novo[3],kolicina_poz_novo[3])=napravi_semu(randomklijenti,kolona3_novo)

        br_neg = {1: 15, 2: 15, 3: 15};br_neg_novo = {1: 15, 2: 10, 3: 10}
        (randomklijenti_neg,kolicina_neg,randomklijenti_svi)=napravi_seme_neg(randomklijenti_poz,br_neg)
        (randomklijenti_neg_novo,kolicina_neg_novo,randomklijenti_svi_novo)=napravi_seme_neg(randomklijenti_poz_novo,br_neg_novo)
        print "negativno"
        print randomklijenti_neg,kolicina_neg
        print randomklijenti_neg_novo,kolicina_neg_novo
        for i in range(1,4):
            sema_kon=[randomklijenti_poz[i],kolicina_poz[i], randomklijenti_neg[i],kolicina_neg[i],randomklijenti_svi[i]]
            sve_seme.append(sema_kon)
            sema_kon=[randomklijenti_poz_novo[i],kolicina_poz_novo[i], randomklijenti_neg_novo[i],kolicina_neg_novo[i],randomklijenti_svi_novo[i]]
            sve_seme.append(sema_kon)
     
        ws.append([broj_posjeta[1], broj_posjeta[2],broj_posjeta[3],broj_paleta[1],broj_paleta[2],broj_paleta[3],"novo",broj_posjeta_novo[1], broj_posjeta_novo[2],broj_posjeta_novo[3],broj_paleta_novo[1],broj_paleta_novo[2],broj_paleta_novo[3]])
        #i je redni br promjene, a zapravo je q ide od 2 do 8. posto generisanjem se napravi vise klijenata tipa q, za svakog [q][j] se biljezi a, b i c
        #a-[] je broj pll u starom stanju, b-[1] je broj pll u novom stanju ako se preslo u novo stanje, c-[2]je broj pll iz starog stanja
        #promjene[q].append((a,b,c))-a je broj pll u starom stanju, b je broj pll u novom stanju ako se preslo u novo stanje, c je broj pll iz starog stanja prakticno isto kao i a- radi provjere je
        # promjene[i][j][a,b,c] c ili 2 je broj paleta novog stanja u slucaju da se zadrzalo starom stanje, tako da je isti kao a ili 0
        for i in promjene:
            brojac=0;brojac2=0;brojac3=0;brojac4=0;brojac5=0; brojac6=0; brojac7=0
            broj=len(promjene[i]); broj1=len(promjene_posjeta[i])
            #print i, broj, broj1
            for j in range(len(promjene[i])):
                    #ako je broj paleta u starom stanju nula, desila se promjena, nije znaci zadržana stara sema
                    if promjene[i][j][2]==0:
                            brojac=brojac+1
                            #ako je broj paleta u starom stanju razlicit od onog u novom, onda se smanjio broj paleta i to je brojac2. Znaci nije zadrzano staro stanje
                            if promjene[i][j][0]!=promjene[i][j][1]:
                                brojac2=brojac2+1
                                if promjene_posjeta[i][j][0]<promjene_posjeta[i][j][1]:
                                    brojac6+=1
                            #print i, brojac2, brojac6 
                            #ako je ostao isti onda je zadrzan isti broj paleta pri smanjenju broja posjeta
                            if promjene[i][j][0]==promjene[i][j][1]:
                                brojac3=brojac3+1
                                if promjene_posjeta[i][j][0]<promjene_posjeta[i][j][1]:
                                    brojac7+=1
                            #za posjete
                            if promjene_posjeta[i][j][0]<promjene_posjeta[i][j][1]:
                                brojac5+=1
                    # ako broj paleta u starom stanju nije nula, i jos jedna provjera ako je u novom nula (nepotrebna je) brojac4 pokazuje koliko ih je ostalo isto
                    if promjene[i][j][1]==0:
                            brojac4=brojac4+1

            #print "sumarno", i, brojac2, brojac6 
            ws1.append([i, broj, brojac, brojac2, brojac3, brojac4,brojac5, brojac6, brojac7])
            #ovi rezultati ne mogu da se dobiju prije gneresianja klijenata, jer se ne zna iz kog stanja se prelazi u koje.
        for q in promjene_posjeta:
            brojac=0
            for i in range(len(promjene_posjeta[q])):
                if promjene_posjeta[q][i][2]==-1:
                    brojac+=1
            #print "ctr", len(promjene_posjeta[q]), brojac

        klijent_pll={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0}; klijent_pll_novo={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0}
        for k in range(len(kolona1)):
            ukupno=kolona1[k]+kolona2[k]+kolona3[k]; 
            ukupno_novo=kolona1_novo[k]+kolona2_novo[k]+kolona3_novo[k]; 
            klijent_pll[ukupno]+=1
            klijent_pll_novo[ukupno_novo]+=1
        #print ukupno, ukupno_novo 
        #print klijent_pll
        #print klijent_pll_novo
        ws2.append([klijent_pll[1],klijent_pll[2],klijent_pll[3],klijent_pll[4],klijent_pll[5],klijent_pll[6],klijent_pll[7],klijent_pll[8],"novo", klijent_pll_novo[1],klijent_pll_novo[2],klijent_pll_novo[3],klijent_pll_novo[4],klijent_pll_novo[5],klijent_pll_novo[6],klijent_pll_novo[7],klijent_pll_novo[8]])

        
    print len(randomklijenti_poz[1]),len(randomklijenti_poz[2]), len(randomklijenti_poz[3])
    print len(kolicina_poz[1]),len(kolicina_poz[2]), len(kolicina_poz[3])
    print len(randomklijenti_poz_novo[1]),len(randomklijenti_poz_novo[2]), len(randomklijenti_poz_novo[3])
    print len(kolicina_poz_novo[1]),len(kolicina_poz_novo[2]), len(kolicina_poz_novo[3])

    print len(randomklijenti_neg[1]),len(randomklijenti_neg[2]), len(randomklijenti_neg[3])
    print len(kolicina_neg[1]),len(kolicina_neg[2]), len(kolicina_neg[3])
    print len(randomklijenti_neg_novo[1]),len(randomklijenti_neg_novo[2]), len(randomklijenti_neg_novo[3])
    print len(kolicina_neg_novo[1]),len(kolicina_neg_novo[2]), len(kolicina_neg_novo[3])
    print
    
    semav=napravi_raspodjelu_od_fje(kolicina, sema_prob)
    #1(po_periodu, udiou_ukupnom, ppk)=posjeta_po_klijentu(kolicina, nova_raspodela,semav,sema, ws5)
    
    semav_novo=napravi_raspodjelu_od_fje(kolicina, sema_prob_novo)
    #semav je raspodjela vjerovatnoca; sema_prob je fja raspodjele; semav_novo je raspodjela vjerovatnoca u novom stanu; sema_prob_novo je fja raspodjele u novom stanju

    promjene_sumarno(kolicina, sema, semav, sema_novo, semav_novo, sema_prob_novo,nova_raspodela,ws5)
    
    # Ovo ovdje se radi da bi se u šeme novog stanja i njihove raspodjele vjerovatnoća dodale šeme i njihov vjerovatnoće i starog stanja.
    #Prije dodavanja potrebno ih je pomnožiti sa vjerovatnoćom zadržavanja starog stanja
    for q in kolicina:
        k=0
        preostalo=1-sema_prob_novo[q][-1]
        for i in sema[q]:
            sema_novo[q].append(i)
            semav_novo[q].append(preostalo*semav[q][k])
            k+=1

    #1(po_periodu_novo, udiou_ukupnom_novo, ppk_novo)=posjeta_po_klijentu(kolicina,nova_raspodela,semav_novo,sema_novo,ws5)
    

    #3pllpo_klijentu=pll_po(sema, semav, nova_raspodela, kolicina, ws5)
    #4pllpo_klijentu_novo=pll_po(sema_novo, semav_novo, nova_raspodela, kolicina, ws5)

    (tip, tip_pll)=raspodelapo(kolicina, sema, semav, nova_raspodela, ws5)
    (tip_novo, tip_pll_novo)=raspodelapo([1]+kolicina, sema_novo, semav_novo, nova_raspodela,ws5)

    #7pllpo_posjeti=napravi_posebnu(kolicina, sema, semav, nova_raspodela, ws5)
    #8pllpo_posjeti_novo=napravi_posebnu(kolicina, sema_novo, semav_novo, nova_raspodela, ws5)

    """
    #DIO ZA PRORACUN PARAMETARA POSJETA PO STAROM I NOVOM
    
    print "nova raspodela", nova_raspodela
    print "Posjeta po klijentu po periodu", po_periodu, po_periodu_novo
    print "Udio u ukupnom (raspodjela ppk na tri)", udiou_ukupnom, udiou_ukupnom_novo
    print "Posjeta po klijentu sumarno ", ppk, ppk_novo
    print

    #DIO ZA PRORAČUN PLL i POSJETA PARAMETARA
    
    print "Raspodjela klijenata prema broju paleta-tipu(novo, za staro se zadaje-raspodela): ", tip_pll, tip_pll_novo
    print "Raspodjela klijenata prema broju posjeta: ",tip, tip_novo
    print
    
    s=sum(pllpo_klijentu.values()); s_novo=sum(pllpo_klijentu_novo.values())
    print "Paleta po klijentu po periodu:", pllpo_klijentu, pllpo_klijentu_novo; 
    print "Paleta po klijentu sumarno:",s,s/3, s_novo,s_novo/3
    print "Paleta po klijentu udio:",pllpo_klijentu[0]/s,pllpo_klijentu[1]/s, pllpo_klijentu[2]/s, "novo", pllpo_klijentu_novo[0]/s_novo,pllpo_klijentu_novo[1]/s_novo, pllpo_klijentu_novo[2]/s_novo 
    print

    s=sum(pllpo_posjeti.values()); s_novo=sum(pllpo_posjeti_novo.values())
    print "Paleta po posjeti po periodu:", pllpo_posjeti,pllpo_posjeti_novo;
    print "Paleta po posjeti sumarno:", s,s/3, s_novo,s_novo/3
    #print "Paleta po posjeti udio:", pllpo_posjeti[0]/s,pllpo_posjeti[1]/s,pllpo_posjeti[2]/s, "novo", pllpo_posjeti_novo[0]/s_novo,pllpo_posjeti_novo[1]/s_novo,pllpo_posjeti_novo[2]/s_novo
    """
    
    wb.save('G:\My Drive\postavka.xlsx')
    return(sve_seme)

    # ovo je za staro stanje: pllpo_posjeti- je različito ujutru, u podne i uvece zato je dato kao rjecnik
    #ovo je za novo: tip_novo je rječnik koji pokazuje koliko ima klijenata sa 1, 2 ili 3 posjete;  - pokazuje koliko klijenata prima 1,2..8 pll ukupno (prvi + drugi + treci period);
    #ovo je za novo: pllpo_posjeti_novo pokazuje koliko ima pll po posjeti u novom stanju po periodima
