"""A basic bare main file for an api using fastapi"""
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root() -> dict:
    """Basic test root for fastapi

    Returns:
        dict: json response
    """
    return {'message': 'Hello World'}
