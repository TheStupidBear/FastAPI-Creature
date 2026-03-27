from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from model.explorer import Explorer
from service import explorer as service
from data.explorer import init_explorer
from errors import Missing, Duplicate
from pathlib import Path


router = APIRouter(prefix="/explorer")

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

#создаем таблицу
init_explorer()

@router.get("")
@router.get("/")
def get_all(request: Request):
    return template_obj.TemplateResponse("list_explorers.html",
                                         {"request": request,
                                          "explorers": service.get_all()})

@router.get("/{name}")
def get_one(name) -> Explorer | None:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

#создать исследователя
@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(explorer: Explorer) -> Explorer:
    try:
        return service.create(explorer)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

# @router.patch("/")
# def modify(explorer: Explorer) -> Explorer:
#     return service.modify(explorer)

@router.delete("/{name}")
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)