"""A basic bare main file for an api using fastapi"""
from fastapi import FastAPI

from app.utils.mcq_generator import MCQGenerator
from app.data.neurograph import create_graph

app = FastAPI()


@app.get('/live')
async def live() -> dict:
    """
    Basic live test for api

    Returns:
        dict: empty response
    """
    return {}


# Define rate limits
@app.get('/')
async def root() -> dict:
    """
    Basic mcq generated at api root

    Returns:
        dict: json response
    """
    graph = create_graph()
    mcq = MCQGenerator(graph)
    output = mcq.generate()
    return output
