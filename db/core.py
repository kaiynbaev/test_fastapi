from sqlalchemy import text, insert, select
from db.database import sync_engine, async_engine, session_factory, async_session_factory
from db.models import ServerRequests, KadastrNumber, Base
from fastapi import HTTPException, Request, Response
import httpx



def create_tables():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    
def drop_table():
    Base.metadata.drop_all(sync_engine)
        
def get_data_ServerRequests_one():
    with session_factory() as session:
        query_to_db = select(ServerRequests)
        result = session.execute(query_to_db)
        requests = result.all()
        data = [request.__dict__ for request, in requests]
        return (data)

def add_data_KadastrNumber(kadastr_number: str, latitude:str, longtitude:str):
    data = KadastrNumber(number = kadastr_number, latitude=latitude, longtitude=longtitude)
    with session_factory() as session:
        session.add(data) # данные ещё в оперативке
        session.commit()  # данные сохранились в базу данных
        
def get_KadastrNumber(kadastr_number: str ):
    with session_factory() as session:
        request = text(f'''SELECT :kadastr_number FROM kadastr_number;''')
        request = request.bindparams(kadastr_number=kadastr_number)
        result = session.execute(request)
        result = result.all()
        return print(result[0][0])  # обычный селект запрос
    
def get_data_ServerRequests(kadastr_number: str):
    with session_factory() as session:
        request = text(
                    '''SELECT * FROM requests WHERE kadastr_number=:params'''
                    )   
        request = request.bindparams(params=kadastr_number)
        print(request.compile(compile_kwargs = {'literal_binds': True}))
        res = session.execute(request)
        result = res.all()
        if result:
            # Если есть результаты, вернуть их
            return(result)
        else:
            # Если нет результатов, вернуть сообщение
            return f'No records found for kadastr_number: {kadastr_number}'
    

