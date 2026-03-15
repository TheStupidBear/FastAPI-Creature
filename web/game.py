from pathlib import Path
from fastapi import APIRouter, Body, Request
from fastapi.templating import Jinja2Templates
from service import game as service

router = APIRouter(prefix="/game")

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

# Первоначальный запрос на игру
@router.get("")
def game_start(request: Request):
    name = service.get_word()
    return template_obj.TemplateResponse("game.html",
        {"request": request, "word": name})

# Последующие игровые запросы
@router.post("")
async def game_step(word: str = Body(), guess: str = Body()):
    score = service.get_score(word, guess)
    return score