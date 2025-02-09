from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud

router = APIRouter()

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = "a88dcb6f-aedc-47fc-a2b5-38f1cfdb9046"


@router.get("temperature/", response_model=list[schemas.Temperature])
async def get_all_temperature(db: AsyncSession = Depends(get_db), city_id: Optional[int] = None):
    return await crud.get_temperature_list(db=db, city_id=city_id)


@router.post("/temperature/", response_model=schemas.TemperatureCreate)
async def create_new_temperature(
        new_temperature: schemas.TemperatureCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_temperature(db=db, temperature=new_temperature)


@router.get("temperature/update")
@router.get("temperature/{temperature_id}", response_model=schemas.Temperature)
async def get_temperature(temperature_id: int, db: AsyncSession = Depends(get_db)):
    new_temperature = await crud.get_temperature_by_id(db=db, temperature_id=temperature_id)
    if not new_temperature:
        raise HTTPException(status_code=404, detail="Temperature not found")

    return new_temperature


@router.put("temperature/{temperature_id}", response_model=schemas.Temperature)
async def temperature_update_data(
        temperature_id: int,
        new_temperature: schemas.TemperatureCreate,
        db: AsyncSession = Depends(get_db)
):
    update_data = await crud.update_temperature(db=db, temperature_id=temperature_id, temperature=new_temperature)
    if not update_data:
        raise HTTPException(status_code=404, detail="Temperature not found")

    return update_data


@router.delete("/temperature/{temperature_id}", response_model=schemas.Temperature)
async def delete_temperature(temperature_id: int, db: AsyncSession = Depends(get_db)):
    db_temperature = await crud.delete_temperature(db=db, temperature_id=temperature_id)
    if not db_temperature:
        raise HTTPException(status_code=404, detail="Temperature not found")

    return db_temperature
