"""A basic bare main file for an api using fastapi"""
# pylint: disable=unused-argument
from app.core.mcq_generator import MCQGenerator
from app.data.sample_graph import generate_graph
from app.models import MCQ
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    'https://main.d1vo05ddg5t68j.amplifyapp.com',
    'http://main.d1vo05ddg5t68j.amplifyapp.com',
    'http://localhost:8000',
    'https://localhost:8000',
    'http://localhost:3000',
    'https://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/live')
async def live(request: Request) -> dict:
    """
    Basic live test for api

    Returns:
        dict: empty response
    """
    return {}


@app.get('/', responses={200: {'model': MCQ}})
@limiter.limit('5/second')
async def root(request: Request) -> MCQ:
    """
    Basic mcq generated at api root

    Returns:
        dict: json response
    """
    graph = generate_graph()
    mcq = MCQGenerator(graph)
    output = mcq.generate()
    return output
