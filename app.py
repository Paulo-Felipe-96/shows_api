from flask import Flask, request
from data import alchemy


app = Flask(__name__)
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


@app.route('/', methods=['GET'])
def home():
    test = {'status': 200,
            'message': 'functioning'}
    return test


if __name__ == '__main__':
    app.run(port=3000)
