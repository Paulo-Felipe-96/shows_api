from data import alchemy
from . import episodes

class ShowModel(alchemy.Model):
    __tablename__ = 'shows'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    name = alchemy.Column(alchemy.String(80))

    # episódios
    #lazy dynamic indica que o carregamento de episodios sera feito dinamicamente
    #nao tudo de uma vez
    episodes = alchemy.relationship(episodes.EpisodeModel, lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name, 'episodes': []}

    def save_db(self):
        # uma sessão de banco, gerando um pedaço
        # do banco que fica em memória para evitar
        # consultas demasiadas
        # essa instrução executa insert na base de dados
        alchemy.session.add(self)
        alchemy.session.commit()

    # classmethod para retornar a representação do que
    # se refere apenas àquele objeto
    # .first() traz somente um recurso, não uma lista

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()