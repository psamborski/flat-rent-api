from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Dummy flat rent API."}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
