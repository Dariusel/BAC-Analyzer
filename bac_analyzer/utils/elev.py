from dataclasses import dataclass, asdict

@dataclass
class Elev:
    cod: str = ''
    medie: None = None
    rezultat: None = None
    liceu: str = ''
    promotie_anterioara: bool = False
    forma_invatamant: str = ''
    specializare: str = ''
    limba_romana_competente: str = ''
    limba_romana_nota: None = None
    limba_romana_contestatie: None = None
    limba_romana_nota_finala: None = None
    limba_materna: None = None
    limba_materna_competente: None = None
    limba_materna_nota: None = None
    limba_materna_contestatie: None = None
    limba_materna_nota_finala: None = None
    limba_moderna_studiata_competente: str = ''
    limba_moderna_studiata_nota: None = None
    disciplina_obligatorie: str = ''
    disciplina_obligatorie_nota: None = None
    disciplina_obligatorie_contestatie: None = None
    disciplina_obligatorie_nota_finala: None = None
    disciplina_alegere: str = ''
    disciplina_alegere_nota: None = None
    disciplina_alegere_contestatie: None = None
    disciplina_alegere_nota_finala: None = None
    competente_digitale: None = None
    judet: str = ''
    page: None = None
    year: None = None

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def to_dict(self):
        return asdict(self)