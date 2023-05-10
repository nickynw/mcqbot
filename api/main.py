"""A basic bare main file for an api using fastapi"""
# pylint: disable=unused-argument

from api.data.graph_database import new_graph
from api.models import MCQ
from api.utils.mcq_generator import MCQGenerator
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
api = FastAPI()
api.state.limiter = limiter
api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@api.get('/live')
async def live(request: Request) -> dict:
    """
    Basic live test for api

    Returns:
        dict: empty response
    """
    return {}


@api.get('/')
@limiter.limit('5/second')
async def root(request: Request, response_model=MCQ) -> MCQ:
    """
    Basic mcq generated at api root

    Returns:
        dict: json response
    """
    graph = new_graph()
    mcq = MCQGenerator(graph)
    output = mcq.generate()
    return output
