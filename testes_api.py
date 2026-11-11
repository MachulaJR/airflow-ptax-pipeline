import requests
url = ("https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
       "CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)")

parametros = {"@moeda": "'USD'", "@dataCotacao": "'09-11-2026'", "$format": "json"}
resposta = requests.get(url=url, timeout=15, params=parametros)

print(resposta.status_code)

resposta.raise_for_status

dados = resposta.json()

print(dados)
