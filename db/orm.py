from database import sync_engine, async_engine, session_factory
from models import MetaData, QueryTable

def insert_data_with_orm(data_from_user):
    if data_from_user is not None :   
        data = QueryTable(query = data_from_user) 
        with session_factory() as session:
            session.add(data)
            session.commit()
            print (type(data_from_user))

