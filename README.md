# API-reGECS

API do jogador inteligente reGECS desenvolvida em Python.

O sistema implementa uma Inteligência Artificial baseada em Minimax com poda Alpha-Beta para tomada de decisão em partidas de um jogo de estratégia disputado em um tabuleiro 5x5. A IA é responsável por analisar o estado atual da partida, gerar todas as jogadas válidas, simular cenários futuros, avaliar posições estratégicas e selecionar a melhor ação possível a cada turno.

## Principais Características

- Gera movimentos válidos para professores.
- Simulação de estados futuros através de cópias independentes do jogo.
- Busca utilizando Minimax.
- Otimização da busca utilizando poda Alpha-Beta.
- Heurística personalizada para avaliação de estados.
- Identificação de vitórias imediatas.
- Avaliação de mobilidade e controle do tabuleiro.
- Análise de proximidade de professores em relação às casas de vitória.
- Estratégia de posicionamento inicial baseada no controle da região central.

## Arquitetura da IA

A tomada de decisão segue o seguinte fluxo:

Estado Atual do Jogo
        ↓
Identificação dos Professores
        ↓
Geração de Movimentos Possíveis
        ↓
Simulação das Jogadas
        ↓
Minimax + Alpha-Beta
        ↓
Avaliação Heurística
        ↓
Escolha da Melhor Jogada

## Estratégia Utilizada

A IA considera que ambos os jogadores realizam sempre a melhor jogada possível.

Durante a busca são analisados cenários futuros até uma profundidade 2. Cada estado gerado é avaliado por uma função heurística que leva em consideração:

- Vitória ou derrota imediata.
- Possibilidade de vitória no próximo turno.
- Quantidade de movimentos disponíveis.
- Casas de nível 2, 3 e 4 presentes no tabuleiro.
- Distância dos professores aliados até casas vencedoras.
- Distância dos professores adversários até casas vencedoras.
- Potencial estratégico de cada posição.

A partir dessas informações, a IA seleciona a jogada com a maior pontuação estimada.

## Tecnologias Utilizadas

- Python 3
- FastAPI
- Pydantic
- Uvicorn

## Objetivo

Desenvolver um agente inteligente capaz de tomar decisões estratégicas em tempo real, maximizando suas chances de vitória através da análise de estados futuros e da avaliação de posições vantajosas no tabuleiro.