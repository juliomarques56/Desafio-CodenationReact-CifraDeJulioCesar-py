import requests
import json
import hashlib


def pegar_desafio(url):
    dados = requests.get(url).json()
    with open('answer.json', 'w') as f:
        json.dump(dados, f)

def hash_decifrada(texto_decifrado):
    hash_texto = hashlib.sha1()
    hash_texto.update(texto_decifrado.encode())
    return hash_texto.hexdigest()

def decifrar():
    with open('answer.json') as f:    
        dados = json.load(f)

    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    caracter_decifrado = ''

    for letra in dados['cifrado']:
        if letra in alfabeto:
            num = alfabeto.find(letra)
            num = num - dados['numero_casas']

            if num >= len(alfabeto):
                num = num - len(alfabeto)

            elif num < 0:
                num = num + len(alfabeto)
            
            caracter_decifrado = caracter_decifrado + alfabeto[num]
        else:
            caracter_decifrado = caracter_decifrado + letra

    return caracter_decifrado

def atualizar_json(texto_decifrado):
    pega_hash_decifrada = hash_decifrada(texto_decifrado)
    
    with open('answer.json', 'r+') as f:
        data = json.load(f)
        data['resumo_criptografico'] = pega_hash_decifrada
        data['decifrado'] = texto_decifrado
        f.seek(0)
        json.dump(data, f)
        f.truncate()

def enviar_form(token):
    POST = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=" + token
    answer = {'answer': open('answer.json', 'rb')}
    enviar = requests.post(POST, files=answer)
    print(enviar.headers)


if __name__ == '__main__':
    
    token = 'SEU_TOKEN'

    GET = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=" + token
    pegar_desafio(GET)
    decifrado = decifrar()
    atualizar_json(decifrado)
    enviar_form(token)