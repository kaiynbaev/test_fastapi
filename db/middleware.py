import logging
from db.models import ServerRequests
from main import app
from fastapi import Request


@app.middleware("http")
async def log_request(request: Request, call_next):
    
    for_db = ServerRequests(
        method=request.method,
        url=str(request.url),
        headers=str(request.headers),
        body=await request.body(),
    )
    for_db.save_to_database()
    
    
    print("Request details:")
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Headers: {request.headers}")
    print(f"Query parameters: {request.query_params}")
    print(f"Path parameters: {request.path_params}")
    print(f"Request body: {await request.body()}")
    

    # Передача управления следующему middleware или обработчику маршрута
    response = await call_next(request)

    # Логика после обработки запроса, если необходимо
    print("After endpoint")

    return response

    
