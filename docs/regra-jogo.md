# Objetivo

O jogo é disputado entre dois jogadores em um tabuleiro **5x5**.

Cada posição do tabuleiro representa um aluno que possui um nível acadêmico.

Os níveis possíveis são:

* 1º Ano
* 2º Ano
* 3º Ano
* Graduado

Cada jogador controla **2 professores**.

O objetivo é ser o primeiro jogador a mover um de seus professores para uma posição contendo um aluno de **4º Ano**.

A vitória acontece imediatamente após esse movimento.

---

# Configuração Inicial

## Tabuleiro

O tabuleiro possui **25 posições** organizadas em uma matriz **5x5**.

No início da partida:

* Todas as 25 posições contêm alunos de **1º Ano**.
* Não existem alunos de outros níveis.

## Posicionamento dos Professores

Cada jogador possui **2 professores**.

O posicionamento ocorre alternadamente:

1. Jogador A posiciona seu primeiro professor.
2. Jogador B posiciona seu primeiro professor.
3. Jogador A posiciona seu segundo professor.
4. Jogador B posiciona seu segundo professor.

### Regras

* Qualquer posição do tabuleiro pode ser escolhida.
* Uma posição ocupada por um professor não pode receber outro professor.
* Professores adversários não podem ocupar a mesma posição.
* Professores do mesmo jogador também não podem ocupar a mesma posição.

Após o posicionamento dos quatro professores, a partida começa.

---

# Estrutura do Turno

Os jogadores jogam alternadamente.

Em cada turno, o jogador deve executar as etapas abaixo.

## Etapa 1 – Escolher um Professor

O jogador escolhe um dos seus dois professores.

Somente o professor escolhido poderá agir naquele turno.

---

## Etapa 2 – Movimentação

O professor deve se mover para uma posição adjacente.

### Posições adjacentes

* Acima
* Abaixo
* Esquerda
* Direita
* Diagonais adjacentes

### Restrições de Movimento

O professor pode mover-se para qualquer posição adjacente cujo aluno **não seja Graduado**.

#### Permitido

* 1º Ano → 1º Ano
* 1º Ano → 2º Ano
* 2º Ano → 3º Ano
* 2º Ano → 2º Ano
* 2º Ano → 1º Ano
* 3º Ano → 1º Ano
* 3º Ano → 2º Ano
* 3º Ano → 3º Ano
* 3º Ano → 4º Ano (**ganha o jogo**)

#### Proibido

* Entrar em uma posição com aluno Graduado.

Além disso:

* O professor não pode mover-se para uma posição ocupada por outro professor.

### Condição de Vitória

Se o professor se mover para uma posição contendo um aluno de **4º Ano**:

* O jogo termina imediatamente.
* O jogador vence a partida.

A etapa de evolução não é executada após uma jogada vencedora.

---

## Etapa 3 – Evolução de Aluno

Caso não tenha ocorrido vitória, o jogador deve promover um aluno.

O aluno escolhido deve estar em uma posição adjacente ao professor que acabou de se mover.

### Posições adjacentes

* Acima
* Abaixo
* Esquerda
* Direita
* Diagonais adjacentes

### Restrições

O aluno escolhido:

* Não pode possuir um professor sobre ele.
* Não pode ser Graduado.

### Evolução

A evolução aumenta exatamente um nível acadêmico.

#### Exemplos

* 1º Ano → 2º Ano
* 2º Ano → 3º Ano
* 3º Ano → 4º Ano
* 4º Ano → Graduado

Não existe evolução além de Graduado.

---

# Alunos Graduados

Quando um aluno se torna Graduado:

* Ele permanece na mesma posição do tabuleiro.
* Não pode evoluir novamente.
* Professores não podem entrar naquela posição.

Na prática, a posição torna-se uma casa bloqueada para movimentação.

---

# Situações sem Movimento

Se o professor escolhido não possuir movimentos válidos, o jogador pode escolher seu outro professor.

Se pelo menos um dos professores possuir movimento válido, o jogador deve realizar uma jogada.

Se ambos os professores estiverem sem movimentos válidos, o jogador perde a partida.

---

# Consequências Estratégicas

## Criação de Casas de Vitória

Como todos os alunos começam no **1º Ano**, um jogador precisa evoluir alunos sucessivamente:

```text
1º Ano → 2º Ano → 3º Ano → 4º Ano

Ou no caso o adversário pode evoluir também e o jogador apenas 
aproveitar a posição.
```

para criar uma posição vencedora.

## Bloqueio de Casas de Vitória

Um aluno de **4º Ano** pode ser promovido para **Graduado** antes que o adversário alcance a posição.

Isso remove a possibilidade de vitória naquela casa.

## Formação de Barreiras

Como posições **Graduadas** bloqueiam movimentação, os jogadores podem criar barreiras e corredores dentro do tabuleiro.
