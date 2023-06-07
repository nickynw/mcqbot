"""A basic bare main file for an api using fastapi"""
# pylint: disable=unused-argument

from app.core.mcq_generator import MCQGenerator
from app.data.sample_graph import generate_graph
from app.models import MCQ
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get('/live')
async def live(request: Request) -> dict:
    """
    Basic live test for api

    Returns:
        dict: empty response
    """
    return {}


@app.get('/')
@limiter.limit('5/second')
async def root(request: Request, response_model=MCQ) -> MCQ:
    """
    Basic mcq generated at api root

    Returns:
        dict: json response
    """
    graph = generate_graph()
    mcq = MCQGenerator(graph)
    output = mcq.generate()
    return output
