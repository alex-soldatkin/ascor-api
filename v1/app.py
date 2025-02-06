import os
import pandas as pd

from fastapi import FastAPI, HTTPException
df_assessments = pd.read_excel("./data/TPI ASCOR data - 13012025/ASCOR_assessments_results.xlsx")
df_assessments['Assessment date'] = pd.to_datetime(df_assessments['Assessment date'])
df_assessments['Publication date'] = pd.to_datetime(df_assessments['Publication date'])

def __is_running_on_nuvolos():
    """
    If we are running this script from Nuvolos Cloud, 
    there will be an environment variable called HOSTNAME
    which starts with 'nv-'
    """

    hostname = os.getenv("HOSTNAME")
    return hostname is not None and hostname.startswith('nv-')

if __is_running_on_nuvolos():
    # Nuvolos alters the URL of the API (likely for security reasons)
    # Instead of https://A-BIG-IP-ADDRESS:8000/
    # The API is actually served at https://A-BIG-IP-ADDRESS/proxy/8000/
    app = FastAPI(root_path="/proxy/8000/")
else:
    # No need to set up anything else if running this on local machine
    app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/v1/country-data/{country}/{assessment_year}")
async def get_country_data(country: str, assessment_year: int):

#    # Silly non-data-driven response for now
#     return {"message": f"You requested data for {country} in {assessment_year}. Eventually, we will return the data here."}
    """
    Get the data for a specific country and assessment year. 
    """
    # First validate inputs
    if not country or not assessment_year:
        raise HTTPException(
            status_code=400,
            detail="Both country and year must be provided"
        )

    try:
        # Check if country exists first
        if country not in df_assessments['Country'].unique():
            raise HTTPException(
                status_code=404,
                detail=f"Country '{country}' not found in dataset"
            )
        
        # Check if year exists for this country
        country_years = df_assessments[df_assessments['Country'] == country]['Assessment date'].dt.year.unique()
        if assessment_year not in country_years:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for country '{country}' in year {assessment_year}"
            )

        # Filter the data
        mask = (df_assessments['Country'] == country) & (df_assessments['Assessment date'].dt.year == assessment_year)
        data = df_assessments[mask]

        if data.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for country '{country}' in year {assessment_year}"
            )

        # Get area columns
        area_columns = [col for col in df_assessments.columns if col.startswith('area')]
        if not area_columns:
            raise HTTPException(
                status_code=500,
                detail="No area columns found in dataset"
            )

        # Create result DataFrame
        result = data[area_columns].copy()
        if len(result) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No area data found for country '{country}' in year {assessment_year}"
            )

        # Add metadata and clean up
        result['country'] = country
        result['assessment_year'] = assessment_year
        result = result.fillna('')
        result.rename(columns=lambda x: x.replace('area ', ''), inplace=True)

        # Get first row safely
        if len(result) > 0:
            return result.iloc[0].to_dict()
        else:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for country '{country}' in year {assessment_year}"
            )

    except HTTPException:
        raise
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for country '{country}' in year {assessment_year}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )