from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
import logging
from datetime import date 

logger = logging.getLogger(__name__)

address = ("/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)")

def buscar_cotacao(moeda: str, data: date, base_url: str = "https://olinda.bcb.gov.br") -> dict:

    url = base_url.rstrip("/") + address

    politica_retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429,500,502,503,504],
        allowed_methods=frozenset(['GET']),
        respect_retry_after_header=True
    )

    parametros = {
        "@moeda": f"'{moeda}'",
        "@dataCotacao": f"'{data:%m-%d-%Y}'",
        "$format": "json"                    
    }
    
    with requests.Session() as sessao:
        sessao.mount('https://', HTTPAdapter(max_retries=politica_retry))

        resposta = sessao.get(
            url=url,
            params=parametros,
            timeout=(5, 30)
        )
        
        resposta.raise_for_status()

        try:
            dados = resposta.json()
        except ValueError as e:
            raise ValueError('Json invalido!') from e

        if not isinstance(dados, dict) or "value" not in dados:
            raise ValueError(f"Formato invalido!: {str(dados)[:200]}")

    logger.info("PTAX %s %s: %d registro(s)", moeda, data, len(dados["value"]))
    return resposta.json()