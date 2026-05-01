from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from typing import Annotated
from model.explorer import Explorer
from service import explorer as service
from data.explorer import init_explorer
from errors import Missing, Duplicate
from pathlib import Path
from web.user import get_user_depends


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

#post запрос от кнопки: Добавить исследователя
@router.post("/add", status_code=201)
def create(request: Request, get_user: get_user_depends):
    return template_obj.TemplateResponse("create_explorer.html",
                                         {"request": request})

#создать исследователя
@router.post("/create", status_code=201)
def create(request: Request, get_user: get_user_depends,
           name: Annotated[str, Form()],
           country: Annotated[str, Form()],
           description: Annotated[str, Form()]):
    try:
        service.create(Explorer(name=name, country=country,description=description, user=get_user["username"]))
        message_explorer = f"Исследователь {name} был добавлен."
        return template_obj.TemplateResponse("list_explorers.html",
                                             {"request": request,
                                              "explorers": service.get_all(),
                                              "message_creature": message_explorer})
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


#изменить исследователя
@router.post("/edit")
def modify(request: Request):
    message_explorer = f"Изменить исследователя (в разработке)."
    return template_obj.TemplateResponse("list_explorers.html",
                                         {"request": request,
                                          "explorers": service.get_all(),
                                          "message_explorer": message_explorer})

#удалить исследователя
@router.post("/delete")
def delete(request: Request):
    message_explorer = f"Удалить исследователя (в разработке)."
    return template_obj.TemplateResponse("list_explorers.html",
                                         {"request": request,
                                          "explorers": service.get_all(),
                                          "message_explorer": message_explorer})


@router.get("/{name}")
def get_one(name) -> Explorer | None:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)