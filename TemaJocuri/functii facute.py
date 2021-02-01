grid_joc = [['#' for x in range(10)] for y in range(10)]
scor_jucatori={'x':0,'y':0}


def print_stare_joc(grid_joc):
    for i in range(10):
        print('   ', i, end='')
    print()
    for i in range(len(grid_joc)):
        print(i, grid_joc[i])


def stare_joc_initial(grid):
    grid[4][4] = 'x'
    grid[5][4] = 'x'
    grid[4][5] = '0'
    grid[5][5] = '0'
    return grid


grid_joc = stare_joc_initial(grid_joc)


def mutare(semn, grid):
    print('Prima pozitie')
    x = int(input('Coordonate linie:'))
    y = int(input('Coordonate coloana:'))
    grid_copie = deepcopy(grid)

    if (x < 0 or x > 9 or y < 0 or y > 9):
        print('Pozitia cautata este in afara matricei')
        return mutare(semn, grid)

    if (grid[x][y] != '#'):
        print('Pozitia dorita nu este libera,mai incercati odata')
        return mutare(semn, grid)
    else:
        grid_copie[x][y] = semn

        rez = mutare2(semn, grid_copie, x, y)
        if (rez == False):
            return mutare(semn, grid)
        else:
            return rez


def mutare2(semn, grid, x, y):
    print('A doua pozitie')
    copie_grid = deepcopy(grid)
    x2 = int(input('Coordonate linie:'))
    y2 = int(input('Coordonate coloana:'))

    if (x < 0 or x > 9 or y < 0 or y > 9):
        print('Pozitia cautata este in afara matricei')
        return mutare2(semn, grid, x, y)

    if copie_grid[x2][y2] != '#':
        print('Pozitia dorita nu este libera,mai incercati odata')
        return mutare2(semn, grid, x, y)

    if ((abs(x - x2) + abs(y - y2)) > 1):
        print('A doua pozitie trebuie sa fie langa prima pozitie,pe coloana sau pe verticala, mai incercati odata')
        return mutare2(semn, grid, x, y)
    else:
        if (check_mutare(copie_grid, x, y, x2, y2) == False):
            print('Mutarea nu e valida,nu indeplineste conditia de a fi vecin cu un x si un 0')
            return False
        copie_grid[x2][y2] = semn

    print(semn, punct(copie_grid, x, y, semn))
    print(semn, punct(copie_grid, x2, y2, semn))
    return copie_grid


def check_mutare(grid, x, y, x2, y2):
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
    linie_cautare = x
    coloana_cautare = y
    for i in mat_poz_c:
        scor = math.floor(scor)
        linie_cautare = x + i
        for j in mat_poz_c:
            coloana_cautare = y + j
            if (linie_cautare not in range(10) and coloana_cautare not in range(10)):
                continue
            if (grid[linie_cautare][coloana_cautare] == semn):

                if (linie_cautare + i) in range(10) and (linie_cautare + j) in range(10):
                    if (grid[linie_cautare + i][coloana_cautare + j] == semn):
                        scor = scor + 1
                        continue

                if (linie_cautare - i) in range(10) and (linie_cautare - j) in range(10):
                    if (grid[linie_cautare - i][coloana_cautare - j] == semn):
                        scor = scor + 0.5
                        continue
    return math.floor(scor)


# 2 7 0
# 3 7 x

def pozitii_valabile(grid):
    pozitii_vect = []
    for x1 in range(10):
        for y1 in range(10):
            for x2 in range(10):
                for y2 in range(10):
                    if (x1 == x2 and y1 == y2):
                        continue
                    else:
                        if ((abs(x1 - x2) + abs(y1 - y2)) > 1):
                            continue

                        if (grid[x1][y1] != '#' or grid[x2][y2] != '#'):
                            continue

                        if (check_mutare(grid, x1, y1, x2, y2) == True):
                            if (x2, y2, x1, y1) not in pozitii_vect:
                                pozitii_vect.append((x1, y1, x2, y2))
    return pozitii_vect


def final_joc(grid):
    if (len(pozitii_valabile(grid)) != 0):
        return False
    else:
        return True


####DE VERIFICAT MAI MULTE CONDITII DE JOC
# if(semn=='0'):
#     conditie_0=True
# if(semn=='x'):
#     conditie_x=True


#
# ap = []
# mat_poz_vec = [-1, 0, 1]
# for i in mat_poz_vec:
#     ap.append(i)
# print(ap)

print_stare_joc(grid_joc)
print(pozitii_valabile(grid_joc))
print(len(pozitii_valabile(grid_joc)))

for i in range(12):
    if (final_joc(grid_joc)):
        print('Final joc')
        break
    print(pozitii_valabile(grid_joc))
    grid_joc = mutare('x', grid_joc)
    print_stare_joc(grid_joc)
# print_stare_joc(grid_joc)
# print(pozitii_valabile(grid_joc))
# grid_joc=mutare('0',grid_joc)
# print_stare_joc(grid_joc)
# grid_joc = mutare('x', grid_joc)
# print_stare_joc(grid_joc)
# grid_joc=mutare('0',grid_joc)
# print_stare_joc(grid_joc)
# grid_joc = mutare('x', grid_joc)
# print_stare_joc(grid_joc)
# grid_joc=mutare('0',grid_joc)
# print_stare_joc(grid_joc)
