import datetime
from sqlalchemy import Table, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base, async_session_factory
    

class KadastrNumber(Base): # Сам кадастровый номер
    __tablename__ = 'kadastr_number'
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(nullable=False, unique=True)
    latitude: Mapped[str] = mapped_column(nullable=False, index=True)
    longtitude: Mapped[str] = mapped_column(nullable=False, index=True)
    

class ServerRequests(Base):     # Запрос по кадастровому номеру
    __tablename__ = 'requests'
    id: Mapped[int] = mapped_column(primary_key=True)
    method: Mapped[str] = mapped_column(index=True)
    url: Mapped[str] = mapped_column(index=True)
    headers: Mapped[str]
    kadastr_number: Mapped[str] = mapped_column(nullable=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    async def save_to_database(self):
        async with async_session_factory() as session:
            session.add(self)
            await session.commit()
    # Response: Mapped[str] = mapped_column(nullable=False)







# class RequestByKadastrNumber(Base):
#     __tablename__ = 'Requests_by_kadastr_number'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     Requests_by_KadastrNumber: Mapped[str] = mapped_column(ForeignKey('query_table.query'))
#     KadastrNumber: Mapped[int] = mapped_column(ForeignKey('Kadastr_Number.number'))
