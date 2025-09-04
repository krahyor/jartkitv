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


# Code smell: unused variable, hardcoded magic number, and duplicate code
def calculate_discount(price):
    discount = 0.1  # Magic number
    unused_var = 123  # Unused variable
    return price * discount


@app.get("/smell")
def smell():
    # Duplicate code
    result1 = calculate_discount(100)
    result2 = calculate_discount(100)
    return {"discount1": result1, "discount2": result2}
