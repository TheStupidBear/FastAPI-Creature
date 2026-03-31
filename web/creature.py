from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from model.creature import Creature
from service import creature as service
from data.creature import init_creature
from errors import Missing, Duplicate
from pathlib import Path


router = APIRouter(prefix="/creature")

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

#создаем таблицу
init_creature()

@router.get("")
@router.get("/")
def get_all(request: Request):
    return template_obj.TemplateResponse("list_creatures.html",
                                         {"request": request,
                                          "creatures": service.get_all()})

@router.get("/{name}")
def get_one(name) -> Creature:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

#создать существо
@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

# @router.patch("/{name}")
# def modify(name, creature: Creature) -> Creature:
#     return service.modify(name, creature)

@router.delete("/{name}")
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)