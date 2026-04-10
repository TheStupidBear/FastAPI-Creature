from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from web import explorer, creature, user, game



app = FastAPI()
app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)
app.include_router(game.router)

#разрешения
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

#главная страница
@app.get("/")
async def top(request: Request):
    return template_obj.TemplateResponse("index.html",
                                         {"request": request})


#подключаем static файлы
app.mount("/static",
 StaticFiles(directory=f"{parent_dir}/static", html=True),
 name="free")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True)