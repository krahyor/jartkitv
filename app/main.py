from fastapi import FastAPI
from .utils import add

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/add")
def add_numbers(a: int, b: int):
    return {"result": add(a, b)}


@app.get("/add_number")
def add_number(a: int, b: int):
    return {"result": add(a, b)}
