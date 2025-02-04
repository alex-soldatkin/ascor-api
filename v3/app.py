import os
import pandas as pd
from fastapi import FastAPI
from .models import ResponseData, ErrorResponse
from .transformers import transform_country_data, melt_assessment_data
from .exceptions import DataNotFoundError, ASCORException
from utils import get_data_path

# Load and transform data
df_assessments = pd.read_excel(os.path.join(get_data_path(), "ASCOR_assessments_results.xlsx"))
df_assessments['Assessment date'] = pd.to_datetime(df_assessments['Assessment date'])
df_assessments['Publication date'] = pd.to_datetime(df_assessments['Publication date'])
melted_df = melt_assessment_data(df_assessments)

def __is_running_on_nuvolos():
    hostname = os.getenv("HOSTNAME")
    return hostname is not None and hostname.startswith('nv-')

if __is_running_on_nuvolos():
    app = FastAPI(root_path="/proxy/8000/v3")
else:
    app = FastAPI()

@app.get("/")
async def read_root():
    return {"version": "v3"}

@app.get(
    "/country-metrics/{country}/{assessment_year}",
    response_model=ResponseData,
    responses={404: {"model": ErrorResponse}}
)
async def get_country_metrics(country: str, assessment_year: int):
    try:
        filtered_data = melted_df[
            (melted_df["Country"] == country) &
            (melted_df['Assessment date'].dt.year == assessment_year)
        ]

        if filtered_data.empty:
            raise DataNotFoundError(
                message=f"No data found for country: {country} and year: {assessment_year}"
            )

        return transform_country_data(filtered_data, country, assessment_year)
    except DataNotFoundError as e:
        raise e
    except Exception as e:
        raise ASCORException(status_code=500, message=str(e))
