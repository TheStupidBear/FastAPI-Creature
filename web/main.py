from fastapi import FastAPI
import uvicorn
from web import explorer, creature, user


app = FastAPI()
app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)

@app.get("/")
async def top():
    return "top here"

@app.get("/echo/{thing}")
async def echo(thing):
    return f"echo {thing}"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)