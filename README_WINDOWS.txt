PROJETO OBD-II - WINDOWS
========================

ARQUITETURA
-----------

O projeto possui dois modos:

1. SIMULATION
   Não precisa de carro nem ELM327.
   Gera dados dinâmicos de um carro virtual.

2. PHYSICAL
   Usa um ELM327 físico conectado via USB/Bluetooth.
   Usa python-obd.

A aplicação principal é a mesma nos dois casos.


1. INSTALAÇÃO
-------------

Abra PowerShell dentro da pasta:

    python -m venv .venv

Ative:

    .venv\Scripts\activate

Instale:

    python -m pip install --upgrade pip
    pip install -r requirements.txt


2. TESTAR O SIMULADOR
---------------------

Execute:

    python main.py --mode simulation

O programa continuará gerando dados.

Você deverá ver valores como:

    RPM
    SPEED
    COOLANT_TEMP
    THROTTLE_POS
    FUEL_LEVEL

Pare com:

    Ctrl+C

O banco será:

    telemetry.db


3. ABRIR O DASHBOARD
--------------------

Em outro PowerShell, com o ambiente ativado:

    python dashboard.py

Abra no navegador:

    http://127.0.0.1:5000

Deixe o main.py rodando para o dashboard receber dados.


4. TESTAR O ELM327 FÍSICO
--------------------------

Quando você tiver o leitor:

    python -m serial.tools.list_ports

Exemplo:

    COM5

Então:

    python main.py --mode physical --port COM5

Ou tente detectar automaticamente:

    python main.py --mode physical


5. POR QUE ESSA ARQUITETURA?
----------------------------

O dashboard e o banco não precisam saber de onde vieram os dados.

Hoje:

    SIMULADOR
       |
       v
    ObdDecoder
       |
       v
    telemetry.db
       |
       v
    Dashboard

Futuramente:

    ELM327 FÍSICO
       |
       v
    ObdDecoder
       |
       v
    telemetry.db
       |
       v
    Dashboard


6. IMPORTANTE SOBRE O ELM327 EMULATOR
--------------------------------------

Se você quiser usar o ELM327 Emulator no Windows, ele precisa
ter uma comunicação serial virtual configurada.

O erro anterior:

    could not open port 'COM3'

significa que a COM3 não existia naquele momento.

O simulador deste projeto não depende dessa porta COM.
Por isso ele é o melhor primeiro teste do sistema.


7. PRÓXIMO PASSO
----------------

Depois de validar o simulador, podemos adicionar:

- gráficos históricos;
- indicador de conexão;
- atualização em tempo real;
- RPM em gráfico;
- velocidade em gráfico;
- temperatura;
- consumo;
- códigos de falha DTC;
- botão para iniciar/parar coleta;
- seleção de porta COM pelo dashboard;
- exportação CSV;
- histórico de sessões;
- suporte a ELM327 USB e Bluetooth.
