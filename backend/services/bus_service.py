# Importa a bibliotecas p/ requisição HTTP, manipulação de tempo,
# além de importar as aplicações para cálculo de distância e ETA.
import requests
import time
from utils.geo_utils import calculate_distance, calculate_eta

## 1. CONFIGURAÇÕES PARA PERFORMANCE: Criação de variável endpoint, com
## informações do GPS da Prefeitura do Rio, evitando sobrecarga através
## de caches e limita os registros no histórico 
BUS_API = "http://dados.mobilidade.rio/gps/sppo"

CACHE_STORAGE = {} # Guarda cache por linha
CACHE_TTL_SEC = 10  # Validade de 10seg para o Cache

# Histórico comparativo de distância atual/anterior
# para determinar aproximação ou distanciamento da loc do usuário
# Lmite máximo de registros em 500
BUS_HISTORY = {}
MAX_HISTORY_SIZE = 500

# Armazena 5 velocidades p/ calcular a média
SPEED_HISTORY_SIZE = 5



def get_bus_data(line, user_lat, user_lon):
    # Permite alteração nas variáveis globais da função
    global CACHE_STORAGE, BUS_HISTORY
    
    # Limpeza de histórico após o limite.
    if len(BUS_HISTORY) > MAX_HISTORY_SIZE:
        BUS_HISTORY.clear()

    current_time = time.time()

    ## 2. LÓGICA DO CACHE: Cria chave única com base na linha e na
    ## posição do usuário e fornece dados da memória(RAM) caso um
    ## pedido igual chegue em menos de 10seg.
    cache_key = f"{line}_{round(user_lat,3)}_{round(user_lon,3)}"
    line_cache = CACHE_STORAGE.get(cache_key)
    # Cache por linha
    if line_cache and (current_time - line_cache["time"] < CACHE_TTL_SEC):
        print(f"DEBUG: [Cache] Linha {line} recuperada da memória.")
        return {
            "success": True,
            "data": line_cache["data"],
            "error": None
        }
  
    print(f"DEBUG: [API] Buscando novos dados para a linha {line}...")
    
    # Tratamento de possível erro de rede ou API
    try:
        # # Tempo máx de 30seg de espera por requisição HTTP
        response = requests.get(BUS_API, timeout = 30)
        response.raise_for_status()
        
        # Conversão de JSON (API) p/ Python
        data = response.json()

    # Encontra erros de rede e armazena na variável "e"
    # e retorna aviso
    except requests.exceptions.RequestException as e:
        # Se a API falhar retorna cache anterior
        if line_cache:
            print(f"DEBUG: [Erro] Falha na API. Usando cache antigo para a {line}.")
            return {
                "success": True,
                "data": line_cache["data"],
                "error": None
            }       
        print(f"DEBUG: [Erro] Falha na API para linha {line}: {e}")
        return {
            "success": False,
            "data": [],
            "error": str(e)
        }

    # Armazena ônibus em dicionário, evitando duplicações     
    buses = {}

    ## 3. FILTRAGEM E TRATAMENTO DE DADOS  
    for bus in data:
        # Garante que a linha do ônibus seja igual a solicitada
        # Sendo diferente, pula
        if bus.get("linha") != line:
            continue
                
        if not bus.get("latitude") or not bus.get("longitude"):
            continue
        
        # Tenta converter valores em texto para números (Float)
        try:
            lat = float(bus.get("latitude").replace(",", "."))
            lon = float(bus.get("longitude").replace(",", "."))
            speed = float(bus.get("velocidade", 0))
            
            # Elimina ônibus parados ou com velocidade inválida
            if speed < 5:
                continue
            
            # Mapeamento de identificador único do ônibus na API
            # Não havendo ID, ignora e pula
            bus_id = bus.get("ordem")
            if not bus_id:
                continue

            # Cálcular distância
            distance = calculate_distance(user_lat,user_lon, lat, lon)
            # Obtém histórico do ônibus
            bus_history = BUS_HISTORY.get(bus_id)
            # Tendo distância registrada, verifica a direção ônibus x usuário
            # Aplica tolerância de 0.05 km (~ 50 metros) p/ evitar erros de imprecisão
            previous_distance = None
            speeds = []
            # Se já existe histórico 
            if bus_history:
                previous_distance = bus_history["distance"]
                speeds = bus_history["speeds"].copy()

            # Filtro de direção: distância diminuindo
            if previous_distance is not None:
                # Ignora ônibus se afastando ( dist anterior + 50m)
                if distance > previous_distance + 0.05:
                    BUS_HISTORY[bus_id] = {
                        "distance": distance,
                        "speeds": speeds
                    }
                    continue
            
            # Adiciona velocidade atual
            speeds.append(speed) 
            # Limita histórico de velocidades
            if len(speeds) > SPEED_HISTORY_SIZE:
                speeds.pop(0)

            # Velocidade Média
            avg_speed = sum(speeds)/len(speeds)    

            # Cálcular ETA
            eta = calculate_eta(distance, avg_speed)

            BUS_HISTORY[bus_id] = {"distance": distance, "speeds": speeds}

            buses[bus_id] = {
                "bus_id": bus_id,
                "line": bus.get("linha"),
                "lat": lat,
                "lon": lon,
                "speed": speed,
                "distance_km": round(distance, 2),
                "eta_min": round(eta, 1) if eta is not None else None
                }

        # Caso ocorra erros de conversão, o registro é ignorado e o loop continua
        except ValueError:
            continue       
    # Verificação de lista vazia, caso não tenha nada no dicionário 'buses'
    if not buses:
        print(f"DEBUG: [Aviso] Nenhum ônibus encontrado para a linha {line}.")
        return {
            "success": True,
            "data": [],
            "error": None
        }

    ## 4.ORDENAÇÃO E ENTREGA: Ordenação por tempo de chegadam, limitado
    ## aos 20 mais próximos.
    
    # Transforma o dicionário em lista p/ ordenar (dici não tem ordem)
    bus_list = list(buses.values())
    # Ordena por tempo de chegada, atribuindo valor alto aos ônibus sem previsão
    bus_list.sort(key = lambda x: x["eta_min"] if x["eta_min"] is not None else float("inf"))
    # Retorna os 20 primeiros
    result = bus_list[:20] 

    # Atualização do CACHE
    CACHE_STORAGE[cache_key] = {
        "data": result,
        "time": current_time
    }

    return {
        "success": True,
        "data": result,
        "error": None
    }
