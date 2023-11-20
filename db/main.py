import asyncio
import os 
import sys
from orm import insert_data_with_orm
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from core import create_tables, insert_data, drop_table




