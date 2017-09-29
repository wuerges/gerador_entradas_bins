import ezodf
import re





def parse_fase(fase, number):
#    print("F:", fase)
    if not fase:
        return number
    f = re.match('(\d+)ª', fase)
    if f:
        return int(f.group(1))
    return None

def parse_professores(texto):
    return re.split(r'\s+e\s+', texto)

class Sheet:
    def __init__(self, sheet):
        self.sheet = sheet

    def professores(self):

        professores = set()
        oferta = []
        nome_dos_docentes = 'Nome do(s) Docente(s)'

        fase = 0
        for i in range(2, self.sheet.nrows()):
            prof = self.sheet[i, 6].value
            fase_cell = self.sheet[i, 0].value
            disc_cell = self.sheet[i, 3].value

            fase = parse_fase(fase_cell, fase)
            if fase:
                if prof and prof != nome_dos_docentes:
                    pp = parse_professores(prof)
                    for p in pp:
                        professores.add(p)
                    oferta.append((pp, fase, disc_cell))

        return professores, oferta

class NameMap:
    def __init__(self):
        self.names = {}
        self.count = 0

    def get(self, name, p='P'):
        if name in self.names:
            return self.names[name]
        cod = "%s%d" % (p, self.count+1)
        self.names[name] = cod
        self.count += 1
        return cod

def get_fases(oferta):
    fases = set()
    for ps, f, d in oferta:
        fases.add(f)
    return fases

prof_map = NameMap()
disc_map = NameMap()
diurno_map = NameMap()
noturno_map = NameMap()

name = 'oferta.ods'

doc = ezodf.opendoc(name)


s1 = Sheet(doc.sheets[0])
s2 = Sheet(doc.sheets[1])

profs1, ofertas1 = s1.professores()
profs2, ofertas2 = s2.professores()

print("""% Nro de dias com aula na semana
% Numero de turnos
% Para cada turno
%      Nome do turno
%      Numero de periodos
%      Para cada periodo
%           Numero de horas aula
%           Numero de horarios no turno com estas horas aula
%           Para cada Horário
%                Número do horario

5 3 M 2  3 5  0  2  4  6  8
         2 5  1  3  5  7  9
    T 2  3 5 10 12 14 16 18
         2 5 11 13 15 17 19
    N 2  2 5 20 22 24 26 28
         2 5 21 23 25 27 29

% Nro de Professores
% Para cada Professor
%      Nome
%      Numero de horarios que nao deseja trabalhar
%      Para cada Horário
%           Número do horario""")

profs = profs1 | profs2
print(len(profs))
for p in profs:
    print("%s 0" % prof_map.get(p))

print("""% Nro de Semestres 
% Para cada Semestre
%      Nome
%      Numero de salas de aula
%      Para cada sala de aula
%           Numero de horarios que estao disponveis
%           Para cada Horário
%                Número do horario
%           Numero de horarios preferidos
%           Para cada Horário
%                Número do horario""")

print(len(get_fases(ofertas1)) + len(get_fases(ofertas2)))
for i, f in enumerate(get_fases(ofertas1)):
    print(diurno_map.get(f, 'V'), 1, 101+i, "10 10 11 12 13 14 15 16 17 18 19 0")
for i, f in enumerate(get_fases(ofertas2)):
    print(noturno_map.get(f, 'N'), 1, 101+i, "10 20 21 22 23 24 25 26 27 28 29 0")


print("""% Nro de Disciplinas 
% Para cada Disciplina
%      Nome
%      Numero de creditod
%      Nome do semestre que esta associada
%      Numero de periodos
%      Para cada periodo
%           Numero de horas aula
%           Numero de professores
%           Para cada professor
%                Nome do professor""")
print(len(ofertas1) + len(ofertas2))
for ps, f, d in ofertas1:
    print("%s 4 %s" % (disc_map.get(d, 'D'), diurno_map.get(f)), end=' ')
    s = " ".join([prof_map.get(p) for p in ps])
    print("2 3 %d %s 2 %d %s" % (len(ps), s, len(ps), s))
for ps, f, d in ofertas2:
    print("%s 4 %s" % (disc_map.get(d, 'D'), noturno_map.get(f)), end=' ')
    s = " ".join([prof_map.get(p) for p in ps])
    print("2 2 %d %s 2 %d %s" % (len(ps), s, len(ps), s))
        

print("""% Pesos relativos entre preferencias ( 3 tipos de preferencias)
3
% 4 periodos consecutivos peso:
4
% preferencias dos professores peso:
3
% periodos de 3 horas com disiplina de 2 horas
5
""")
