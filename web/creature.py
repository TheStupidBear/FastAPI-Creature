from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from typing import Annotated, Optional
from model.creature import Creature
from service import creature as service
from data.creature import init_creature
from errors import Missing
from pathlib import Path
from web.user import get_user_depends



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

#post запрос от кнопки: Добавить существо
@router.post("/add", status_code=201)
def create(request: Request, get_user: get_user_depends):
    return template_obj.TemplateResponse("create_creature.html",
                                         {"request": request})

#создать существо
@router.post("/create", status_code=201)
def create(request: Request, get_user: get_user_depends,
           name: Annotated[str, Form()],
           country: Annotated[str, Form()],
           description: Annotated[str, Form()],
           area: Annotated[Optional[str], Form()] = "*",
           aka: Annotated[Optional[str], Form()] = "*"):
    service.create(Creature(name=name, country=country,
    description=description, area=area, aka=aka, user=get_user["username"]))
    message_creature = f"Существо {name} было добавлено."
    return template_obj.TemplateResponse("list_creatures.html",
                                         {"request": request,
                                          "creatures": service.get_all(),
                                          "message_creature": message_creature})

#изменить существо
@router.post("/edit")
def modify():
    return f"Изменить существо"

#удалить существо
@router.post("/delete")
def delete():
    return f"Удалить существо"
    # try:
    #     return service.delete(name)
    # except Missing as exc:
    #     raise HTTPException(status_code=404, detail=exc.msg)

@router.get("/{name}")
def get_one(name) -> Creature:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


