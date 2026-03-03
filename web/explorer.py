from fastapi import APIRouter, HTTPException
from model.explorer import Explorer
from service import explorer as service
from data.explorer import init_explorer
from errors import Missing, Duplicate

router = APIRouter(prefix="/explorer")

#создаем таблицу
init_explorer()

@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()

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