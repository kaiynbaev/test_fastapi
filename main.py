from db.core import ( create_tables, drop_table, get_data_ServerRequests, 
add_data_KadastrNumber, get_KadastrNumber, add_data_KadastrNumber,
get_data_ServerRequests_one )
from db.database import session_factory
from fastapi.requests import Request
from db.models import ServerRequests
from fastapi import FastAPI, Response
import asyncio
import httpx

app = FastAPI()


# Описание задания: 
# Написать сервис, который принимает запрос с указанием кадастрового номера, 
# широты и долготы, эмулирует отправку запроса на внешний сервер, 
# который может обрабатывать запрос до 60 секунд. 
# Затем должен отдавать результат запроса. 
# Считается, что внешний сервер может ответить `true` или `false`.
# Данные запроса на сервер и ответ с внешнего сервера должны быть сохранены в БД.
# Нужно написать АПИ для получения истории всех запросов/истории по кадастровому номеру.
# Сервис должен содержать следующие эндпоинты:
# "/query" - для получения запроса +
# “/result" - для отправки результата +   ---->  как я понял на доп.сервере(прописан в dopolnitelnyi_server.py) 
# "/ping" - проверка, что  сервер запустился +
# “/history” - для получения истории запросов +
# Добавить Админку. - 
# Сервис завернуть в Dockerfile.


@app.middleware("http") # для прослушивания всех http запросов
async def log_request(request: Request, call_next):
    # Проверка пути запроса
    if request.url.path.startswith("/history"):   # условие для прослушивания опред. эндпоинта
        print("Special API Request")
        for_db = ServerRequests(
            method=request.method,
            url=str(request.url),
            headers=str(request.headers),
            kadastr_number=str(request.query_params.get('kadastr_number')),
        )
        await for_db.save_to_database()
        # Вызов следующего middleware или обработчика маршрута
        response = await call_next(request)
        # Логика после обработки запроса, если необходимо
        print("After endpoint")
        return response
    else:
        # Логика для обычных запросов
        print(f"""   Request details:\n 
                    Method: {request.method}\n 
                    URL: {request.url}\n 
                    Headers: {request.headers}\n
                    request.query_params: {request.query_params}""")   
             
        # просто вывожу на консоль для проверки
        # Вызов следующего middleware или обработчика маршрута
        response = await call_next(request)

        # Логика после обработки запроса, если необходимо
        print("After endpoint")

        return response


@app.get("/query")
def get_query(kadastr_number: str): #запрос по кадастровому номеру
    get_data_ServerRequests(kadastr_number=kadastr_number)
    


@app.post("/ping")
async def check_server():
    other_server_url = "http://127.0.0.1:8001" 
    async with httpx.AsyncClient() as client:   
        response = await client.get(f"{other_server_url}")  # запрос на внешний сервер в файлике dopolnitelnyi_server.py
        if (response.text != "\"work\""):                 
            return ''' don't work''' 
        return 'work'
    
    
@app.get('/history')
def get_history(kadastr_number:str): # данные всех запросов по кадастровому запросу
    result = get_data_ServerRequests(kadastr_number)
    return f'data: {result}'


create_tables()
add_data_KadastrNumber(kadastr_number='1235126', latitude='124153', longtitude='1351364')
# также можно проверить через эндпоинты
