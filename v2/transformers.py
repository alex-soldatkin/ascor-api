from typing import Dict, Any, List
import pandas as pd
from .models import ResponseData, Metadata, Pillar, Area, Indicator, Metric

def transform_country_data(raw_data: Dict[str, Any]) -> ResponseData:
    metadata = Metadata(
        country=raw_data['country'],
        assessment_year=raw_data['assessment_year']
    )
    
    pillars = []
    
    def process_pillar(pillar_code: str, max_areas: int) -> List[Area]:
        areas = []
        for i in range(1, max_areas + 1):
            area_key = f"area {pillar_code}.{i}"
            if area_key in raw_data and raw_data[area_key]:
                area = Area(
                    name=f"{pillar_code}.{i}",
                    assessment=raw_data[area_key],
                    indicators=[]
                )
                
                # Add indicators for this area
                for indicator_key in raw_data:
                    if indicator_key.startswith(f"indicator {pillar_code}.{i}."):
                        # Extract the indicator suffix (a, b, c, etc.)
                        ind_suffix = indicator_key.split('.')[-1]
                        ind_name = f"{pillar_code}.{i}.{ind_suffix}"
                        
                        indicator = Indicator(
                            name=ind_name,
                            assessment=raw_data[indicator_key],
                            metrics=None
                        )

                        # Look for corresponding metrics
                        metric_key = f"metric {pillar_code}.{i}.{ind_suffix}.i"
                        if metric_key in raw_data and pd.notna(raw_data[metric_key]):
                            indicator.metrics = Metric(
                                name=f"{pillar_code}.{i}.{ind_suffix}.i",
                                value=str(raw_data[metric_key])
                            )
                        
                        area.indicators.append(indicator)
                
                if area.indicators or area.assessment:
                    areas.append(area)
        return areas

    # Process EP Pillar (3 areas)
    ep_areas = process_pillar("EP", 3)
    if ep_areas:
        pillars.append(Pillar(name="EP", areas=ep_areas))

    # Process CP Pillar (6 areas)
    cp_areas = process_pillar("CP", 6)
    if cp_areas:
        pillars.append(Pillar(name="CP", areas=cp_areas))

    # Process CF Pillar (4 areas)
    cf_areas = process_pillar("CF", 4)
    if cf_areas:
        pillars.append(Pillar(name="CF", areas=cf_areas))

    return ResponseData(
        metadata=metadata,
        pillars=pillars
    )
