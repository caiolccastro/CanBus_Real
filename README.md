# 🚗 OBD-II Windows Dual Mode

Sistema de monitoramento de dados automotivos desenvolvido em Python para leitura de parâmetros **OBD-II**, com suporte a dois modos de operação:

* 🧪 **Simulation Mode** — simulação de um veículo para desenvolvimento e testes sem hardware.
* 🔌 **Physical Mode** — preparado para comunicação com um adaptador **ELM327 físico** via USB ou Bluetooth.

O projeto foi desenvolvido com uma arquitetura desacoplada, permitindo desenvolver e testar toda a aplicação virtualmente antes de conectar um veículo real.

---

## 📌 Sobre o projeto

O objetivo do projeto é criar uma aplicação capaz de coletar, armazenar e visualizar informações disponibilizadas pelo protocolo OBD-II.

Entre os parâmetros monitorados estão:

| PID            | Informação                              | Unidade |
| -------------- | --------------------------------------- | ------- |
| `RPM`          | Rotação do motor                        | rpm     |
| `SPEED`        | Velocidade do veículo                   | km/h    |
| `COOLANT_TEMP` | Temperatura do líquido de arrefecimento | °C      |
| `THROTTLE_POS` | Posição do acelerador                   | %       |
| `FUEL_LEVEL`   | Nível de combustível                    | %       |

O sistema utiliza uma camada de abstração para que a aplicação principal não precise saber se os dados vêm de um **carro virtual** ou de um **ELM327 físico**.

---

# 🏗️ Arquitetura

```text
                         ┌────────────────────┐
                         │     Dashboard      │
                         │       Flask        │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │    telemetry.db    │
                         │      SQLite        │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │     ObdDecoder     │
                         │   Camada comum     │
                         └─────────┬──────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
          ┌──────────────────┐          ┌──────────────────┐
          │  Simulation Mode │          │  Physical Mode   │
          │                  │          │                  │
          │  Carro virtual   │          │     ELM327       │
          └──────────────────┘          └──────────────────┘
```

Essa arquitetura permite que o sistema seja desenvolvido inicialmente sem qualquer equipamento automotivo.

Posteriormente, basta conectar o ELM327 e executar a aplicação em modo físico.

---

# 📂 Estrutura do projeto

```text
obd_windows_dual_mode/
│
├── main.py
├── obd_decoder.py
├── simulation_source.py
├── physical_source.py
├── dashboard.py
├── requirements.txt
├── README_WINDOWS.txt
└── telemetry.db
```

### `main.py`

Ponto de entrada da aplicação.

É responsável por:

* selecionar o modo de operação;
* inicializar a fonte de dados;
* iniciar a coleta;
* armazenar os dados no SQLite;
* controlar o ciclo de execução.

---

### `obd_decoder.py`

Implementa a camada de abstração entre a aplicação e a fonte de dados.

A aplicação utiliza a mesma interface independentemente de estar utilizando:

```text
SimulationSource
```

ou:

```text
PhysicalSource
```

---

### `simulation_source.py`

Responsável pela simulação de um veículo.

Gera dados dinâmicos para:

* RPM;
* velocidade;
* temperatura;
* acelerador;
* combustível.

Os valores possuem relações entre si para tornar a simulação mais próxima do comportamento de um veículo.

---

### `physical_source.py`

Responsável pela comunicação com um ELM327 físico através da biblioteca Python-OBD.

Suporta portas seriais do Windows, como:

```text
COM3
COM4
COM5
```

Também existe uma tentativa de detecção automática das portas disponíveis.

---

### `dashboard.py`

Servidor web desenvolvido com Flask.

Disponibiliza:

```text
http://127.0.0.1:5000
```

O dashboard apresenta os últimos valores registrados no banco de dados.

---

### `telemetry.db`

Banco de dados SQLite utilizado para armazenar as leituras.

Estrutura:

```text
telemetry
│
├── id
├── timestamp
├── pid
└── value
```

---

# 💻 Tecnologias utilizadas

* Python
* Flask
* SQLite
* Python-OBD
* PySerial
* Pint
* ELM327
* OBD-II

---

# ⚙️ Requisitos

* Windows 10 ou superior
* Python 3.10+
* PowerShell ou CMD

Para o modo físico:

* Adaptador ELM327 compatível
* USB ou Bluetooth
* Veículo compatível com OBD-II

> O modo de simulação não necessita de veículo ou adaptador ELM327.

---

# 🚀 Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/obd-windows-dual-mode.git
```

Entre na pasta:

```bash
cd obd-windows-dual-mode
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente:

```powershell
.venv\Scripts\activate
```

Atualize o `pip`:

```powershell
python -m pip install --upgrade pip
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

---

# 🧪 Modo Simulação

O modo de simulação permite executar o projeto sem nenhum equipamento físico.

Execute:

```powershell
python main.py --mode simulation
```

O sistema começará a gerar dados automaticamente.

Exemplo:

```text
[2026-08-24T19:00:01] RPM                -> 1124.5
[2026-08-24T19:00:01] SPEED              -> 12.4
[2026-08-24T19:00:01] COOLANT_TEMP       -> 76.3
[2026-08-24T19:00:01] THROTTLE_POS       -> 18.2
[2026-08-24T19:00:01] FUEL_LEVEL         -> 71.9
```

O programa continuará executando até que seja pressionado:

```text
Ctrl + C
```

---

# 📊 Dashboard

Enquanto o sistema de coleta estiver executando, abra outro terminal:

```powershell
python dashboard.py
```

Depois acesse:

```text
http://127.0.0.1:5000
```

O dashboard apresenta:

```text
┌─────────────────────────────────────┐
│          OBD-II Dashboard            │
├──────────┬──────────┬───────────────┤
│   RPM    │  SPEED   │  TEMPERATURA   │
│  1850    │  42 km/h │     78 °C      │
├──────────┼──────────┼───────────────┤
│ACELERADOR│COMBUSTÍVEL│               │
│   32 %   │   71 %   │               │
└──────────┴──────────┴───────────────┘
```

Os valores são atualizados automaticamente.

---

# 🔌 Modo ELM327 físico

Depois de validar o sistema utilizando o simulador, conecte o adaptador ELM327 ao veículo.

No Windows, verifique as portas seriais disponíveis:

```powershell
python -m serial.tools.list_ports
```

Exemplo:

```text
COM3
COM5
COM7
```

Identifique qual delas corresponde ao ELM327.

Depois execute:

```powershell
python main.py --mode physical --port COM5
```

Substitua `COM5` pela porta correspondente ao seu dispositivo.

Também é possível tentar a detecção automática:

```powershell
python main.py --mode physical
```

---

# 🔄 Fluxo no modo físico

```text
             VEÍCULO
                │
                ▼
             OBD-II
                │
                ▼
             ELM327
                │
          USB / Bluetooth
                │
                ▼
          Windows COM
                │
                ▼
       Python / Python-OBD
                │
                ▼
          ObdDecoder
                │
                ▼
          SQLite Database
                │
                ▼
            Flask
                │
                ▼
            Dashboard
```

---

# 🧠 Por que utilizar dois modos?

Durante o desenvolvimento de sistemas automotivos, nem sempre existe acesso imediato a um veículo ou equipamento OBD-II.

Por isso, o projeto separa a **origem dos dados** da **aplicação**.

No desenvolvimento:

```text
SimulationSource
       ↓
ObdDecoder
       ↓
SQLite
       ↓
Dashboard
```

No veículo real:

```text
PhysicalSource
       ↓
ObdDecoder
       ↓
SQLite
       ↓
Dashboard
```

O restante da aplicação permanece praticamente igual.

---

# 🗄️ Armazenamento

As leituras são armazenadas no SQLite.

Exemplo:

```text
id | timestamp            | pid           | value
---|----------------------|---------------|------
1  | 2026-08-24 19:00:01  | RPM           | 850
2  | 2026-08-24 19:00:01  | SPEED         | 0
3  | 2026-08-24 19:00:01  | COOLANT_TEMP  | 76
4  | 2026-08-24 19:00:01  | THROTTLE_POS  | 5
```

# ⚠️ Observações

O modo físico depende da compatibilidade entre:

* veículo;
* protocolo OBD-II;
* adaptador ELM327;
* driver/conexão do Windows.

O modo de simulação existe justamente para permitir o desenvolvimento da aplicação sem depender dessas condições.

Além disso, os PIDs disponíveis podem variar de acordo com o veículo.

---

# 📚 Objetivo educacional

Este projeto tem como objetivo estudar e demonstrar:

* comunicação com dispositivos automotivos;
* protocolo OBD-II;
* Python;
* comunicação serial;
* arquitetura desacoplada;
* simulação de hardware;
* persistência de dados;
* desenvolvimento de dashboards;
* integração entre hardware e software.
