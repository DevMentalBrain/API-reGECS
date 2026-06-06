import asyncio
import random

from fastapi import FastAPI
from datetime import date

from app.schemas import AITurnRequest, TurnPhase
from app.logic import choose_setup, choose_turn

app = FastAPI(
  title="reGECS - O Jogador Inteligente",
  description="API do reGECS, para o PI5",
  version="0.1.0"
)

@app.get("/health")
async def health():
  return date.today()

@app.post("/move")
async def move(body: AITurnRequest):
  """
  Endpoint principal chamado pelo orquestrador de partidas.
  
  Recebe o estado completo de um turno da partida e devolve a jogada escolhida.
  """
  await asyncio.sleep(random.choice([1.0, 1.5, 2, 2.5, 3]))
  if body.turn_phase == TurnPhase.SETUP:
    return choose_setup(body.board)
  else:
    return choose_turn(body.board, int(body.your_team))