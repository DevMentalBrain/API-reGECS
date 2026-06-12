# Projeto Integrador 5 (API)

Esse repositório contém um servidor backend de alta performance desenvolvido em **Go**,
projetado para atuar como um jogador inteligente em um jogo de tabuleiro baseado nas mecânicas de *Santorini*.

O motor faz uso de uma variante paralela e altamente otimizada do algoritmo **Monte Carlo Tree Search (MCTS)**,
alcançando marcas superiores a **250.000 simulações completas em menos de 4.3 segundos** em ambientes multi-core,
operando com alocação quase nula na Heap de memória.

## 🚀 Principais Características e Diferenciais

* **Paralelismo:** Distribuição das frentes de simulação via *Goroutines* e sem gargalos de concorrência.
* **Física com Zero-Allocation:** O estado do jogo (`State`) foi reduzido a estruturas compactas e tipos primitivos de tamanho fixo (`int8`), sendo processado integralmente na *Stack* de memória, o que neutraliza a necessidade do Garbage Collector interromper a execução.
* **Tabelas de Pesquisa Estática (LUTs):** Mapeamento pré-computado em tempo de inicialização (`init()`) de todas as casas adjacentes válidas e conversões de nomes em arrays fixos, reduzindo o custo de validação de movimentos e construções para tempo constante $O(1)$.
* **Mappers e DTOs:** Arquitetura desacoplada inspirada no *Adapter Pattern*. O motor em Go opera de forma cega utilizando *Generics*, enquanto um pacote de tradução limpa e traduz o JSON enviado pelo orquestrador externo, isolando a física interna do jogo.
* **Infraestrutura Nativa e Enxuta:** Uso exclusivo da biblioteca padrão `net/http` do Go para fornecer os endpoints `/move` e `/health`, garantindo a menor latência de rede possível e zero dependências de terceiros.

## 📁 Estrutura do Projeto

```text
├── api/            # Camada de Entrada (handlers, DTOs e mappers)
├── game/           # O Coração do Jogo (regras, tabuleiro e constantes específicas)
├── mcts/           # O Cérebro Abstrato (implementação do algoritmo)
├── main.go         # Inicializador do Servidor HTTP
└── REPORT.md       # Documento Técnico e Análise de Estratégia
```

## 🛠️ Como Executar o Projeto

### Pré-requisitos

* [Go 1.22 ou superior](https://go.dev/doc/install) instalado.

### 1. Compilação

Para gerar o binário de produção:

```bash
go build -o server .
```

### 2. Executando o Servidor

Inicie o motor executando o binário gerado (ou via `go run main.go` para desenvolvimento):

```bash
./server
```

O servidor nativo subirá instantaneamente ouvindo a porta `:8080`.

## 📈 Endpoints Disponíveis

* **`GET /health`**: Retorna um status `200 OK` com o texto `READY`.
* **`POST /move`**: Recebe o estado atualizado da partida em formato de matriz e retorna a decisão tática calculada pela IA contendo qual professor mover, o destino e onde posicionar a mentoria.

## 📑 Detalhes Arquiteturais e Análise Estratégica

Para mais detalhes sobre o projeto e sobre os motivos de termos preferido Go em vez de outras linguagens, acesse o documento abaixo:

👉 **[Consulte o REPORT.md completo aqui](https://www.google.com/search?q=./REPORT.md)**
