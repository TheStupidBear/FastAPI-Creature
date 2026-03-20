from fastapi import FastAPI, Form, Request
import uvicorn
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from web import explorer, creature, user
from service import explorer as service_explorer
from service import creature as service_creature



app = FastAPI()
app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)
# app.include_router(game.router)

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

@app.get("/")
async def top():
    return "top here"

@app.get("/echo/{thing}")
async def echo(thing):
    return f"echo {thing}"

@app.get("/list")
def explorer_list(request: Request):
    return template_obj.TemplateResponse("list.html",
    {"request": request,
    "explorers": service_explorer.get_all(),
    "creatures": service_creature.get_all()})

@app.post("/who2")
def greet2(name: str = Form()):
 return f"Hello, {name}?"

app.mount("/static",
 StaticFiles(directory=f"{parent_dir}/static", html=True),
 name="free")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)