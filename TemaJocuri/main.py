
import time
from copy import deepcopy
from statistics import median


class Manager:
    def __init__(self):
        self.timp_start_joc=None
        self.timp_final_joc=None
        self.timp_miscari_calculator=[]
        self.numar_miscari_jucator=0
        self.numar_miscari_calculator=0
        self.nr_nod_generate=[]

    def date_final_calculator(self):

        if(self.numar_miscari_calculator!=0):
            print('Timp total rulare:',self.timp_final_joc-self.timp_start_joc)
            print('Timp minim de gandire calculator:',min(self.timp_miscari_calculator))
            print('Timp maxim de gandire calculator:', max(self.timp_miscari_calculator))
            print('Mediana timp calculator:',median(self.timp_miscari_calculator))
            print('Numar minim de noduri generate:',min(self.nr_nod_generate))
            print('Numar  maxim de noduri generate:', max(self.nr_nod_generate))
            print('Mediana numar de noduri generate:',median(self.nr_nod_generate))
            print('Nr mutari user:',self.numar_miscari_jucator)
            print('Nr mutari calculator:',self.numar_miscari_calculator)


manager=Manager()
class Joc:
    #NR_COLOANE=10
    JMIN = None
    JMAX = None

    def __init__(self, table=None,scor_jucatori={'x': 0, '0': 0}):
        if table is not None:
            self.matr = table
            self.scor_jucatori=scor_jucatori
        else:
            self.matr = [['#' for x in range(10)] for y in range(10)]
            self.matr[4][4] = 'x'
            self.matr[5][4] = 'x'
            self.matr[4][5] = '0'
            self.matr[5][5] = '0'
            self.scor_jucatori = {'x': 0, '0': 0}

    @classmethod
    def jucator_opus(cls, jucator):
        if jucator == cls.JMIN:
            return cls.JMAX
        else:
            return cls.JMIN

    def final(self,final_fortat=False):
        if (len(self.mutari()) != 0 and final_fortat==False):
            return False
        else:

            if(self.scor_jucatori['x']>self.scor_jucatori['0']):

                return 'x'
            elif self.scor_jucatori['x'] == self.scor_jucatori['0']:

                return 'remiza'
            else:
                return '0'

    def check_mutare(self, x, y, x2, y2):
        mat_poz_vec = [-1, 0, 1]
        poziti_gasite = []

        for i in mat_poz_vec:
            linie_cautare = x - i
            for j in mat_poz_vec:
                coloana_cautare = y - j
                if i == 0 and j == 0:
                    continue
                if (linie_cautare > 9 or linie_cautare < 0 or coloana_cautare < 0 or coloana_cautare > 9 or (
                        coloana_cautare == y2 and linie_cautare == x2)):
                    continue
                poziti_gasite.append(self.matr[linie_cautare][coloana_cautare])

        for i in mat_poz_vec:
            linie_cautare = x2 - i
            for j in mat_poz_vec:
                coloana_cautare = y2 - j
                if (i == 0 and j == 0):
                    continue
                if (linie_cautare > 9 or linie_cautare < 0 or coloana_cautare < 0 or coloana_cautare > 9 or (
                        coloana_cautare == y and linie_cautare == x)):
                    continue
                poziti_gasite.append(self.matr[linie_cautare][coloana_cautare])

        if 'x' in poziti_gasite:
            if '0' in poziti_gasite:
                return True

        return False





    def mutari(self,semn='#'):
        pozitii_vect = []
        stari_tabla_posibile=[]
        for x1 in range(10):
            for y1 in range(10):
                for x2 in range(10):
                    for y2 in range(10):
                        if (x1 == x2 and y1 == y2):
                            continue
                        else:
                            if ((abs(x1 - x2) + abs(y1 - y2)) > 1):
                                continue

                            if (self.matr[x1][y1] != '#' or self.matr[x2][y2] != '#'):
                                continue

                            if (self.check_mutare(x=x1,y=y1,x2=x2,y2=y2) == True):
                                if (x2, y2, x1, y1) not in pozitii_vect:
                                    pozitii_vect.append((x1, y1, x2, y2))
                                    copie_tabla=deepcopy(self.matr)
                                    copie_tabla[x1][y1]=semn
                                    copie_tabla[x2][y2] = semn
                                    scor_dupa_mutare = deepcopy(self.scor_jucatori)
                                    if(semn!='#'):
                                        scor_mutare=punct(copie_tabla,x1,y1,semn)
                                        scor_mutare=scor_mutare+punct(copie_tabla,x2,y2,semn)
                                        scor_dupa_mutare[semn] = scor_dupa_mutare[semn] + scor_mutare


                                    stari_tabla_posibile.append(Joc(copie_tabla,scor_dupa_mutare)) #de adaugat scor
        return stari_tabla_posibile





    def estimeaza_scor(self, adancime):
        t_final = self.final()
        # if (adancime==0): era comentat de dinainte

        if t_final == self.__class__.JMAX:  # self.__class__ referinta catre clasa instantei
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)

        elif t_final == 'remiza':
            return 0
        else:
            if(self.scor_jucatori[self.__class__.JMAX] == self.scor_jucatori[self.__class__.JMIN]):
                return len(self.mutari())%4 #in caz de scoruri egale, o sa caute mutarea care ii ofera cele mai multe posibilitati
                #este cu mod 4 pentru a nu avea o pondere prea mare si a o alege in defavoarea altor mutari
            return self.scor_jucatori[self.__class__.JMAX] - self.scor_jucatori[self.__class__.JMIN]

    def estimeaza_scor2(self, adancime):
        t_final = self.final()
        # if (adancime==0): era comentat de dinainte

        if t_final == self.__class__.JMAX:  # self.__class__ referinta catre clasa instantei
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)

        elif t_final == 'remiza':
            return 0
        else:
            return self.scor_jucatori[self.__class__.JMAX] - self.scor_jucatori[self.__class__.JMIN]*2
            #aceasta estimare este agresiva impotriva jucatorului, algoritmul va incerca sa il blocheze


    def print_stare_joc(self):
        for i in range(10):
            print('   ', i, end='')
        print()
        for i in range(len(self.matr)):
            print(i, self.matr[i])


class Stare:
    def __init__(self,tabla_joc,j_curent,adancime,parinte=None,estimare=None):
        self.tabla_joc=tabla_joc
        self.j_curent=j_curent
        self.adancime=adancime
        self.estimare=estimare
        self.mutari_posibile=[]
        self.stare_aleasa=None


    def mutari(self):
        l_mutari=self.tabla_joc.mutari(self.j_curent)
        juc_opus=Joc.jucator_opus(self.j_curent)
        l_stari_mutari=[Stare(mutare,juc_opus,self.adancime-1,parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def print_stare_joc(self):
        print('Juc curent:'+self.j_curent)
        for i in range(10):
            print('   ', i, end='')
        print()
        for i in range(len(self.tabla_joc.matr)):
            print(i, self.tabla_joc.matr[i])



def min_max(stare):


    if stare.adancime==0 or stare.tabla_joc.final():
        stare.estimare=stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    stare.mutari_posibile=stare.mutari()


    mutariCuEstimare=[min_max(x) for x in stare.mutari_posibile]


    if(stare.j_curent==Joc.JMAX):
        stare.stare_aleasa=max(mutariCuEstimare,key=lambda x:x.estimare)
    else:
        stare.stare_aleasa=min(mutariCuEstimare,key=lambda x:x.estimare)

    stare.estimare=stare.stare_aleasa.estimare
    return stare

def alpha_beta(alpha, beta, stare):

    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)  # aici construim subarborele pentru stare_noua

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')
        # completati cu rationament similar pe cazul stare.j_curent==Joc.JMAX
        for mutare in stare.mutari_posibile:
            # calculeaza estimarea
            stare_noua = alpha_beta(alpha, beta, mutare)  # aici construim subarborele pentru stare_noua

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    final=stare_curenta.tabla_joc.final()
    if(final):
        if(final=='remiza'):
            print('Remiza!')
        else:
            print('A castigat '+final)
            return True
    return False



def check_mutare_user(grid, x, y, x2, y2):
    mat_poz_vec = [-1, 0, 1]
    poziti_gasite = []

    for i in mat_poz_vec:
        linie_cautare = x - i
        for j in mat_poz_vec:
            coloana_cautare = y - j
            if (i == 0 and j == 0):
                continue
            if (linie_cautare > 9 or linie_cautare < 0 or coloana_cautare < 0 or coloana_cautare > 9 or (
                    coloana_cautare == y2 and linie_cautare == x2)):
                continue
            poziti_gasite.append(grid[linie_cautare][coloana_cautare])

    for i in mat_poz_vec:
        linie_cautare = x2 - i
        for j in mat_poz_vec:
            coloana_cautare = y2 - j
            if (i == 0 and j == 0):
                continue
            if (linie_cautare > 9 or linie_cautare < 0 or coloana_cautare < 0 or coloana_cautare > 9 or (
                    coloana_cautare == y and linie_cautare == x)):
                continue
            poziti_gasite.append(grid[linie_cautare][coloana_cautare])

    if 'x' in poziti_gasite:
        if '0' in poziti_gasite:
            return True

    return False




def punct(grid, x, y, semn):
    scor = 0
    mat_poz_c = [-1, 1]

    for i in mat_poz_c:

        linie_cautare = x + i
        for j in mat_poz_c:
            coloana_cautare = y + j
            if (linie_cautare  in range(10) and coloana_cautare  in range(10)):

                if (grid[linie_cautare][coloana_cautare] == semn):

                    if ((linie_cautare + i) in range(10)) and ((coloana_cautare + j) in range(10)):
                        if (grid[linie_cautare + i][coloana_cautare + j] == semn):
                            scor = scor + 1
                           # print(i,j)
                           # print('Combinatie norocoasa:',x,y,linie_cautare,coloana_cautare,linie_cautare+i,coloana_cautare+j)
                            continue

                    if (linie_cautare - 2*i) in range(10) and (coloana_cautare - 2*j) in range(10):
                        if (grid[linie_cautare - 2*i][coloana_cautare - 2*j] == semn):
                            #print(i,j)
                            #print('Combinatie norocoasa:', x, y, linie_cautare, coloana_cautare, linie_cautare - 2*i,
                                 # coloana_cautare - 2*j)
                            scor = scor + 0.5
                            continue


    return int(scor)








def main():
    # initializare algoritm
    manager.timp_start_joc = time.time()
    raspuns_valid = False
    print('Pentru a iesi oricand din joc, scrieti cand este randul dumneavoastra \'exit\'')
    # TO DO 1
    while not raspuns_valid:
        tip_algoritm = input("Algoritmul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? ").lower()
        if (Joc.JMIN in ['x', '0']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie x sau 0.")
    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'
    # expresie= val_true if conditie else val_false  (conditie? val_true: val_false)

    #greutate joc
    raspuns_valid2=False
    while not raspuns_valid2:
        dificultate=input("Care doriti sa fie dificultatea?[usor/mediu/greu]:").lower()
        if(dificultate in ['usor','mediu','greu']):
            raspuns_valid2=True
        else:
            print('Nu exista optiunea aleasa')

    if(dificultate=='usor'):
        ADANCIME_MAX=2
    elif(dificultate=='mediu'):
        ADANCIME_MAX=3
    elif(dificultate=='greu'):
        ADANCIME_MAX=5
    # initializare tabla
    tabla_curenta = Joc()  # apelam constructorul
    print("Tabla initiala")
    #print(str(tabla_curenta))
    tabla_curenta.print_stare_joc()

    # creare stare initiala

    stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX)

    while True:
        print("SCOR:", stare_curenta.tabla_joc.scor_jucatori)
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul

            # TO DO 4

            print("Acum muta utilizatorul cu simbolul", stare_curenta.j_curent)
            t_inainte = int(round(time.time() * 1000))
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    linie=input("linie=")
                    if (linie == 'exit'):
                        print('Castigatorul este:', stare_curenta.tabla_joc.final(final_fortat=True))
                        print('Scor=', stare_curenta.tabla_joc.scor_jucatori)
                        exit()
                    linie = int(linie)
                    coloana=input("coloana=")
                    if (coloana == 'exit'):
                        print('Castigatorul este:',stare_curenta.tabla_joc.final(final_fortat=True))
                        print('Scor=',stare_curenta.tabla_joc.scor_jucatori)
                        exit()
                    coloana = int(coloana)



                    linie2 = input("linie2=")
                    if (linie2 == 'exit'):
                        print('Castigatorul este:', stare_curenta.tabla_joc.final(final_fortat=True))
                        print('Scor=', stare_curenta.tabla_joc.scor_jucatori)
                        exit()
                    linie2 = int(linie2)
                    coloana2 = input("coloana2=")
                    if (coloana2 == 'exit'):
                        print('Castigatorul este:', stare_curenta.tabla_joc.final(final_fortat=True))
                        print('Scor=', stare_curenta.tabla_joc.scor_jucatori)
                        exit()
                    coloana2 = int(coloana2)







                    if (linie in range(10) and coloana in range(10) and linie2 in range(10) and coloana2 in range(10)):

                        if stare_curenta.tabla_joc.matr[linie][coloana] == '#' and stare_curenta.tabla_joc.matr[linie2][coloana2] == '#':

                            if ((abs(linie - linie2) + abs(coloana - coloana2)) <= 1):

                                if(check_mutare_user(stare_curenta.tabla_joc.matr,linie,coloana,linie2,coloana2)==True):
                                    raspuns_valid = True
                                else:
                                    print('Mutarea nu e valida,nu indeplineste conditia de a fi vecin cu un x si un 0')

                            else:
                                print('A doua pozitie trebuie sa fie langa prima pozitie,pe coloana sau pe verticala, mai incercati odata')

                        else:
                            print("Exista deja un simbol in pozitia ceruta.")
                    else:
                        print("Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0,1,2 ..... 9).")

                except ValueError:
                    print("Linia si coloana trebuie sa fie numere intregi")

            # dupa iesirea din while sigur am valide atat linia cat si coloana
            # deci pot plasa simbolul pe "tabla de joc"
            stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
            stare_curenta.tabla_joc.matr[linie2][coloana2] = Joc.JMIN

            scor=punct(stare_curenta.tabla_joc.matr,linie,coloana,Joc.JMIN)
            scor =scor+punct(stare_curenta.tabla_joc.matr, linie2, coloana2, Joc.JMIN)

            stare_curenta.tabla_joc.scor_jucatori[Joc.JMIN]=stare_curenta.tabla_joc.scor_jucatori[Joc.JMIN]+scor
            # afisarea starii jocului in urma mutarii utilizatorului
            t_dupa = int(round(time.time() * 1000))
            print("Jucatorul a gandit timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            manager.numar_miscari_jucator=manager.numar_miscari_jucator+1
            print("\nTabla dupa mutarea jucatorului")
            #print(str(stare_curenta))
            stare_curenta.print_stare_joc()
            # TO DO 8a
            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            print("Acum muta calculatorul cu simbolul", stare_curenta.j_curent)
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))

            # stare actualizata e starea mea curenta in care am setat stare_aleasa (mutarea urmatoare)
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)

            # print('1')
            # print(stare_curenta)
            # print('2')
            # print(stare_actualizata)
            # print('3')
            # print(stare_actualizata.stare_aleasa)
            # print('4')
            # print(stare_actualizata.stare_aleasa.tabla_joc)

            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc  # aici se face de fapt mutarea !!!
            print("Tabla dupa mutarea calculatorului")
            #print(str(stare_curenta))
            stare_curenta.print_stare_joc()

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            manager.timp_miscari_calculator.append(t_dupa-t_inainte)
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            manager.numar_miscari_calculator=manager.numar_miscari_calculator+1
            # TO DO 8b
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare.  jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)




if __name__ == '__main__':

    main()


