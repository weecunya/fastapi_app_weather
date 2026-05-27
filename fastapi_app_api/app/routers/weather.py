
from fastapi import APIRouter, Depends

from app.api_client import client
from app.dependencies import rate_limit

router = APIRouter(prefix="/weather", tags=["weather"])
cash_dict = {}

@router.get('/')
def home_page():
    return {'status': 'ok'}

@router.get("/city",dependencies=[Depends(rate_limit)])
async def give_weather(city_name:str):
    try:
        if not city_name in cash_dict.keys():
            response = await client.get_weather(city_name)
            cash_dict[city_name] = response
            return {'result': response}
        else:
            response = cash_dict[city_name]
            return {'result': response}
    finally:
        if len(cash_dict.keys()) > 5:
            cash_dict.clear()
        print(len(cash_dict.keys()))