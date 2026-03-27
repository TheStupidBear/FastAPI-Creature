from fastapi import FastAPI, Form, Request
import uvicorn
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from web import explorer, creature, user, game



app = FastAPI()
app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)
app.include_router(game.router)

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

#главная страница
@app.get("/")
async def top(request: Request):
    return template_obj.TemplateResponse("index.html",
                                         {"request": request})

@app.post("/who2")
def greet2(name: str = Form()):
 return f"Hello, {name}?"

#подключаем static файлы
app.mount("/static",
 StaticFiles(directory=f"{parent_dir}/static", html=True),
 name="free")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)