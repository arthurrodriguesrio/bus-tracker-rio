## Bus-Tracker Rio | Fullstack Project

End-to-end real-time bus monitoring and alerting system for Rio de Janeiro.

## Overview
This project is a real-time monitoring solution for Rio de Janeiro's bus fleet. It utilizes asynchronous processing to calculate proximity and notify users via email when a vehicle reaches a point of interest.

The architecture follows a clean and modular structure, separating business logic from the API and background workers to ensure scalability and maintainability.

## Project Structure

BUS-TRACKER/
├── backend/
│   ├── services/           # Business logic (Alerts, Bus Data, DB, Email)
│   │   ├── alert_service.py
│   │   ├── bus_service.py
│   │   ├── db.py
│   │   └── email_service.py
│   ├── tasks/              # Asynchronous Celery tasks
│   │   ├── alert_tasks.py
│   │   └── email_tasks.py
│   ├── utils/              # Geographic calculations (Haversine)
│   │   └── geo_utils.py
│   ├── workers/            # Background alert processing
│   │   └── alert_checker.py
│   ├── celery_app.py       # Celery configuration
│   ├── main.py             # FastAPI entry point
│   └── Dockerfile          # Backend containerization
├── frontend/
│   ├── src/
│   │   ├── components/     # UI Components (Maps, Tables, Forms)
│   │   │   ├── BusMap.jsx
│   │   │   ├── AlertForm.jsx
│   │   │   └── ...
│   │   ├── services/       # API client (Axios/Fetch)
│   │   │   └── api.js
│   │   └── App.jsx         # Main React component
│   └── Dockerfile          # Frontend containerization
├── docker-compose.yml      # Full stack orchestration (Redis, App, Web)
└── README.md


## Technical Highlights
System Architecture: Designed with Microservices principles and Separation of Concerns (SoC).

Asynchronous Pipeline: Celery + Redis handling heavy polling and ETA logic without blocking the main API.

Geolocation: Custom distance calculation and timezone handling (pytz) for high-precision alerting.

Scalability: Worker-based architecture allowing horizontal scaling of alert processing.

DevOps: Fully containerized with Docker, ensuring environment parity from dev to production.

## Technologies Used
Backend: Python 3.11, FastAPI, Pandas.

Frontend: JavaScript, React, Vite.

Messaging & Tasks: Redis, Celery & Celery Beat.

Infrastructure: Docker, Docker Compose.

## How to Run (Quick Start)
Create a .env file in the backend/ directory (refer to .env.example).

Ensure Docker is installed.

Clone the repository and run:

Bash
docker-compose up --build
Access the services:

Application: http://localhost:5173

API Documentation: http://localhost:8000/docs

##---------------------------------------------------------##

Aqui está a versão final e consolidada do seu README.md em português, mantendo todo o rigor técnico e a estrutura profissional que definimos:

## Bus-Tracker Rio | Projeto Fullstack
Sistema de monitoramento e alerta de ônibus em tempo real para o Rio de Janeiro (End-to-End).

Visão Geral
Este projeto é uma solução de monitoramento em tempo real para a frota de ônibus do Rio de Janeiro. Ele utiliza processamento assíncrono para calcular a proximidade e notificar os usuários via e-mail quando um veículo atinge um ponto de interesse.

A arquitetura segue uma estrutura limpa e modular, separando a lógica de negócio da API e dos workers de segundo plano para garantir escalabilidade e facilidade de manutenção.

Estrutura do Projeto
BUS-TRACKER/
├── backend/
│   ├── services/           # Lógica de negócio (Alertas, Dados de Ônibus, DB, Email)
│   │   ├── alert_service.py
│   │   ├── bus_service.py
│   │   ├── db.py
│   │   └── email_service.py
│   ├── tasks/              # Tarefas assíncronas com Celery
│   │   ├── alert_tasks.py
│   │   └── email_tasks.py
│   ├── utils/              # Cálculos geográficos (Haversine)
│   │   └── geo_utils.py
│   ├── workers/            # Processamento de alertas em background
│   │   └── alert_checker.py
│   ├── .env                # Variáveis de ambiente
│   ├── alerts.db           # Banco de dados SQLite
│   ├── celery_app.py       # Configuração do Celery
│   ├── main.py             # Ponto de entrada da API FastAPI
│   └── Dockerfile          # Containerização do Backend
├── frontend/
│   ├── src/
│   │   ├── components/     # Componentes de UI (Mapas, Tabelas, Formulários)
│   │   │   ├── BusMap.jsx
│   │   │   ├── AlertForm.jsx
│   │   │   └── ...
│   │   ├── services/       # Cliente de API (Axios/Fetch)
│   │   │   └── api.js
│   │   └── App.jsx         # Componente principal React
│   └── Dockerfile          # Containerização do Frontend
├── docker-compose.yml      # Orquestração full stack (Redis, App, Web)
└── README.md

Destaques Técnicos
Arquitetura do Sistema: Desenhado com princípios de Microsserviços e Separação de Preocupações (SoC).

Pipeline Assíncrono: Uso de Celery + Redis para lidar com polling pesado e lógica de ETA sem bloquear a API principal.

Geolocalização: Cálculo de distância personalizado e manipulação de fuso horário (pytz) para alertas de alta precisão.

Escalabilidade: Arquitetura baseada em Workers que permite o crescimento horizontal do processamento de alertas.

DevOps: Totalmente containerizado com Docker, garantindo paridade de ambiente do desenvolvimento à produção.

Tecnologias Utilizadas
Backend: Python 3.11, FastAPI, Pandas.

Frontend: JavaScript, React, Vite.

Mensageria & Tarefas: Redis, Celery & Celery Beat.

Infraestrutura: Docker, Docker Compose.

Como Executar (Quick Start)
Crie um arquivo .env no diretório backend/ (siga o modelo em .env.example).

Certifique-se de que o Docker está instalado.

Clone o repositório e execute:

Bash
docker-compose up --build
Acesse os serviços:

Aplicação: http://localhost:5173

Documentação da API: http://localhost:8000/docs

