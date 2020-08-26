from urllib import request
import json
from flask import Flask, request, jsonify
from data import alchemy
from model import show, episode

app = Flask(__name__)

# inicializando o sqlalchemy
alchemy.init_app(app)

# a string do banco de dados que será utilizada
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# track modifications, perigosa
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# propagações de exceções relacionadas ao banco de dados
app.config['PROPAGATE_EXCEPTIONS'] = True

# secret da APP
app.secret_key = 'paulo96'


# uma execução feita somente antes da primeira request
@app.before_first_request
def create_tables():
    alchemy.create_all()


@app.route('/api/all', methods=['GET'])
def home():
    res = show.ShowModel.query.all()
    r = [{'id': i.id, 'name': i.name} for i in res]
    return jsonify(r)


@app.route('/api/delete/<int:id>', methods=['DELETE'])
def delete(id):
    data = show.ShowModel.find_by_id(id=id)
    data.delete()
    msg = f"{id} deletado com sucesso"
    res = {
        'status': 'sucesso',
        'mensagem': msg
    }
    return res


@app.route('/api/show', methods=['POST'])
def create_show():
    data = request.get_json()
    new_show = show.ShowModel(data['name'])
    new_show.save_db()
    result = show.ShowModel.find_by_id(new_show.id)
    return jsonify(result.json())


@app.route('/api/show/<int:id>')  # sem method é GET
def get(id):
    res = show.ShowModel.find_by_id(id)
    if res:
        return res.json()
    return {'status': 404,
            'message': 'série não encontrada'}


@app.route('/api/show/<string:name>/episode', methods=['POST'])
def create_ep_show(name):
    data = request.get_json()
    parent = show.ShowModel.find_by_name(name)
    if parent:
        new_ep = episode.EpisodeModel(name=data['name'], season=data['season'], show_id=parent.id)
        new_ep.save_db()
        return new_ep.json()
    return {'status': 404,
            'message': 'série não encontrada'}


if __name__ == '__main__':
    app.run(port=3000)
