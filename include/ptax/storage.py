from datetime import date
from pathlib import Path
import os
import json

def caminho_arquivo(base_path: str, moeda: str, data: date) -> Path:
    """Monta <base_path>/ptax/dt=AAAA-MM-DD/<MOEDA>.json (sem tocar no disco)."""
    moeda = moeda.strip().upper()

    if not moeda:
        raise ValueError("Moeda vazia.")
    if "/" in moeda or "\\" in moeda or ".." in moeda:
        raise ValueError(f"Moeda invalida: {moeda!r}")

    return Path(base_path) / "ptax" / f"dt={data:%Y-%m-%d}" / f"{moeda}.json"


def salvar_json(dados: dict, base_path: str, moeda: str, data: date) -> str:
    """Grava o JSON de forma atômica e devolve o caminho (str) do arquivo."""
    destino = caminho_arquivo(base_path, moeda, data)
    destino.parent.mkdir(parents=True, exist_ok=True)

    temporario = destino.with_name(destino.name + ".tmp")
    try:
        with open(temporario, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
        os.replace(temporario, destino)
    except Exception:
        temporario.unlink(missing_ok=True)
        raise

    return str(destino)

def ler_json(caminho: str) -> dict:
    """Lê o JSON gravado. Levanta erro claro se o arquivo não existir."""
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)

    
