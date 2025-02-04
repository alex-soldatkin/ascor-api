from fastapi import APIRouter, HTTPException
from ..v1.models import ResponseData, ErrorResponse
from .transformers import transform_country_data
from .exceptions import DataNotFoundError, ASCORException

router = APIRouter()

@router.get(
    "/v1/country-metrics/{country}/{assessment_year}",
    response_model=ResponseData,
    responses={404: {"model": ErrorResponse}}
)
async def get_country_metrics(country: str, assessment_year: int):
    try:
        # Here you would typically fetch data from your database
        # For this example, we'll create dummy data
        raw_data = {
            "country": country,
            "assessment_year": assessment_year,
            "EP_1": "Partial",
            "EP_2": "Yes",
            "EP_3": "No",
            "CP_1": "Partial",
            "CP_2": "Yes",
            "CP_3": "No",
            "CP_4": "Partial",
            "CP_5": "Yes",
            "CP_6": "No",
            "CF_1": "Partial",
            "CF_2": "Yes",
            "CF_3": "No",
            "CF_4": "Partial"
        }
        
        return transform_country_data(raw_data)
    except DataNotFoundError as e:
        raise e
    except Exception as e:
        raise ASCORException(status_code=500, message=str(e))
