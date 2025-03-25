from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

API_ENDPOINT = "https://dragonball-api.com/api/characters"
NUM_PERSONAGENS = 44  # Número total de personagens na API

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        idade = request.form.get('idade', None)

        if not idade or not idade.isdigit() or int(idade) < 1 or int(idade) > 100:
            return render_template('index.html', erro="Informe uma idade válida entre 1 e 100")

        idade = int(idade)
        # Gera um ID aleatório baseado na idade, para garantir alguma variação
        random.seed(idade)  # Usa a idade como semente para o gerador aleatório
        personagem_id = random.randint(1, NUM_PERSONAGENS)

        try:
            response = requests.get(f"{API_ENDPOINT}/{personagem_id}", verify=False)
            response.raise_for_status()
            personagem = response.json()

            if personagem:
                nome = personagem['name']
                url_imagem = personagem['image']
                raca = personagem.get('race', 'Desconhecida')
                afiliacao = personagem.get('affiliation', 'Nenhuma')

                return render_template('index.html', nome=nome, url_imagem=url_imagem, raca=raca, afiliacao=afiliacao)
            else:
                return render_template('index.html', erro="Personagem não encontrado")
        except requests.exceptions.RequestException as e:
            return render_template('index.html', erro=f"Erro ao buscar detalhes do personagem: {e}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)