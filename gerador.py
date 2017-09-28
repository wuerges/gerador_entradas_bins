import ezodf
import re



def parse_professores(texto):
    return re.split(r'\s+e\s+', texto)

def parse_fase(texto):
    return 1


class Sheet:
    def __init__(self, sheet):
        self.sheet = sheet

    def professores(self):

        professores = set()
        nome_dos_docentes = 'Nome do(s) Docente(s)'

        fase = 0
        for i in range(2, self.sheet.nrows()):
            prof = self.sheet[i, 6].value
            fase_cell = self.sheet[i, 0].value
            if fase_cell:
                fase = fase_cell
            if prof and prof != nome_dos_docentes:
                for p in parse_professores(prof):
                    professores.add((p, fase))

        return professores


name = 'oferta.ods'

doc = ezodf.opendoc(name)


s1 = Sheet(doc.sheets[0])

print(s1.professores())

#>>> doc.sheets[0][8,3].value
#'Estatística básica '
#>>> doc.sheets[0][8,0].value
#'2ª '
#>>> doc.sheets[0][7,0].value
#>>> doc.sheets[0][1,0].value
#'Fase'
