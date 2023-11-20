from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import random
import asyncio

server = FastAPI()
origins = [
    "http://localhost:8000",
]
server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"]
)

async def result():
    await asyncio.sleep(5)     # Эмуляция получения запроса
    return random.choice([True, False])    # Считается, что внешний сервер может ответить `true` или `false`.

@server.get('/')
async def main():
    return f'work'    # чтобы узнать работает сервер или нет

@server.get('/result')
async def async_result():
    result_value = await result() #ждём
    return (result_value)