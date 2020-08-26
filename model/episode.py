from data import alchemy


class EpisodeModel(alchemy.Model):
    __tablename__ = 'episoode'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    name = alchemy.Column(alchemy.String(80))
    season = alchemy.Column(alchemy.Integer)

    # criando ligação por chave estrangeira com a tabela shows
    show_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('shows.id'))

    def __init__(self, name, season, show_id):
        self.name = name
        self.season = season
        self.show_id = show_id

    def json(self):
        return {'name': self.name, 'season': self.season}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()

    def delete_db(self):
        alchemy.session.delete(self)
        alchemy.session.commit()
