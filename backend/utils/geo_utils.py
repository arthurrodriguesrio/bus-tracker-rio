## Geolocalização com a biblioteca geopy e o módulo distance
## através do Geodésio (WGS-84)
from geopy.distance import geodesic

## 1. Função para cálculo de distância ônibus x Usuário, com
## informações de latitude e longitude.
def calculate_distance(user_lat, user_lon, bus_lat, bus_lon):
    return geodesic((user_lat,user_lon),(bus_lat,bus_lon)).km

## 2. Função para detrminar tempo de chegada ETA (Estimative Time of Arrival)
## através da fórmula de velocidade ( V = d/t) adaptada para o tempo
## em minutos, com validação para evitar divisão por zero ou
## velocidades negativas
def calculate_eta(distance_km, speed_kmh):
    if speed_kmh <= 0:
        return None
    # Cálculo: Distância / Velocidade = Horas
    eta_hours = distance_km / speed_kmh
    # Retorno em minutos
    return eta_hours * 60

