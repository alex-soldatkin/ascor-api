import os
import pandas as pd
from typing import List
from fastapi import FastAPI, HTTPException
from .models import ResponseData, ErrorResponse
from .transformers import transform_country_data
from .exceptions import DataNotFoundError, ASCORException
from utils import get_data_path  # Changed from relative to absolute import

app = FastAPI()

df_assessments = pd.read_excel(os.path.join(get_data_path(), "ASCOR_assessments_results.xlsx"))
df_assessments['Assessment date'] = pd.to_datetime(df_assessments['Assessment date'])
df_assessments['Publication date'] = pd.to_datetime(df_assessments['Publication date'])

def __is_running_on_nuvolos():
    hostname = os.getenv("HOSTNAME")
    return hostname is not None and hostname.startswith('nv-')

if __is_running_on_nuvolos():
    app = FastAPI(root_path="/proxy/8000/v2")
else:
    app = FastAPI()

@app.get("/")
async def read_root():
    return {"version": "v2"}

@app.get("/country-data/{country}/{assessment_year}")
async def get_country_data(country: str, assessment_year: int):
    """Legacy endpoint for compatibility with v1"""
    try:
        selected_row = (
            (df_assessments["Country"] == country) &
            (df_assessments['Assessment date'].dt.year == assessment_year)
        )

        data = df_assessments[selected_row]

        if data.empty:
            raise DataNotFoundError(
                message=f"No data found for country: {country} and year: {assessment_year}"
            )

        output_dict = {
            "country": country,
            "assessment_year": assessment_year
        }

        # Add areas data
        area_columns = [col for col in data.columns if col.startswith("area")]
        for col in area_columns:
            key = col.replace('area ', '').replace('.', '_')
            output_dict[key] = data[col].iloc[0]

        return output_dict

    except DataNotFoundError as e:
        raise e
    except Exception as e:
        raise ASCORException(status_code=500, message=str(e))

@app.get(
    "/country-metrics/{country}/{assessment_year}",
    response_model=ResponseData,
    responses={404: {"model": ErrorResponse}}
)
async def get_country_metrics(country: str, assessment_year: int):
    try:
        selected_row = (
            (df_assessments["Country"] == country) &
            (df_assessments['Assessment date'].dt.year == assessment_year)
        )

        data = df_assessments[selected_row]

        if data.empty:
            raise DataNotFoundError(
                message=f"No data found for country: {country} and year: {assessment_year}"
            )

        raw_data = {
            "country": country,
            "assessment_year": assessment_year
        }

        # Add data preserving original column names
        for col in data.columns:
            if col.startswith(("area", "indicator", "metric")):
                raw_data[col] = data[col].iloc[0]

        return transform_country_data(raw_data)
    except DataNotFoundError as e:
        raise e
    except Exception as e:
        raise ASCORException(status_code=500, message=str(e))
