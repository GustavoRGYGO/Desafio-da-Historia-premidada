from fastapi import FastAPI, HTTPException, Query, Request
import httpx
import logging
from httpx import ConnectTimeout, HTTPStatusError
import time
from dotenv import load_dotenv
import os

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")
load_dotenv()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    # Determina o nível de log com base no status HTTP
    if response.status_code == 200:
        log_status = "INFO"
    elif response.status_code in (400, 404):
        log_status = "ERROR"
    else:  # Exemplo para sem conexão
        log_status = "CRITICAL"

    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status HTTP: {response.status_code} - "
        f"Status log: {log_status} - "
        f"Tempo: {process_time:.2f}ms - "
        f"Query: {dict(request.query_params)}"
    )

    return response

@app.get("/cliente-endereco")
async def get_cliente_endereco(cpf: str = Query(...), nome: str = Query(...), cep: int = Query(...)):
    # verifica a quantidade de caracteres do CPF.
    if len(cpf) < 11 or len(cpf) > 11:
        raise HTTPException(status_code=400, detail="O CPF é inválido!")

    strcep=str(cep)
    t=len(strcep)
    if t<8:
        for _ in range(8-t):
            strcep='0'+strcep
    #Link da api
    url = f"https://brasilapi.com.br/api/cep/v1/{strcep}"

    try:
        proxy_usu=os.getenv("PROXY")
        # para depuração
        print(proxy_usu)

        async with httpx.AsyncClient(timeout=10.0, verify=False, proxy=proxy_usu) as client:
            response = await client.get(url)
        response.raise_for_status()

        data = response.json()
        status_http = str(response.status_code)

        if status_http == "200":
            return {
                "cpf": cpf,
                "cep": strcep,
                "state": data.get("state"),
                "city": data.get("city"),
                "neighborhood": data.get("neighborhood"),
                "street": data.get("street"),
                "service": data.get("service", "viacep")
            } 

    except ConnectTimeout:
        logger.error("Timeout ao conectar com a BrasilAPI")
        raise HTTPException(status_code=504, detail="Timeout ao conectar com a BrasilAPI")

    except HTTPStatusError as e:
        if str(e.response.status_code) == "400":
            raise HTTPException(status_code=400, detail="O número de caracteres do CEP está incorreto.")

        if str(e.response.status_code) == "404":
            raise HTTPException(status_code=404, detail="O CEP inserido não existe.")

        raise HTTPException(status_code=400, detail="Erro não informado.")

    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")