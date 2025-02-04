from typing import Dict, Any, List
import pandas as pd
from .models import ResponseData, Metadata, Pillar, Area, Indicator, Metric

def melt_assessment_data(df: pd.DataFrame) -> pd.DataFrame:
    """Melt the wide-format assessment data into long format."""
    # Convert all column names to strings
    df.columns = df.columns.astype(str)
    
    id_vars = ['Country', 'Assessment date', 'Publication date']
    
    # Keep source columns in original format for later use
    source_columns = [col for col in df.columns if col.startswith('source')]
    sources_df = df[['Country', 'Assessment date'] + source_columns]
    
    # Filter columns for melting (excluding sources)
    value_vars = [col for col in df.columns if not col.startswith('source') and col not in id_vars]
    
    # Melt the dataframe
    melted_df = pd.melt(
        df,
        id_vars=id_vars,
        value_vars=value_vars,
        var_name='metric_path',
        value_name='value'
    )
    
    # Extract components from metric_path
    melted_df[['type', 'code']] = melted_df['metric_path'].str.extract(r'(area|indicator|metric)\s+([A-Z]{2}\.\d+(?:\.[a-z](?:\.i)?)?)')
    melted_df[['pillar', 'area', 'indicator', 'metric']] = melted_df['code'].str.extract(r'([A-Z]{2})\.(\d+)(?:\.([a-z])(?:\.([i]))?)?')
    
    # Filter out any rows where type is None
    melted_df = melted_df.dropna(subset=['type'])
    
    # Add sources to the melted dataframe
    melted_df = pd.merge(
        melted_df,
        sources_df,
        on=['Country', 'Assessment date'],
        how='left'
    )
    
    return melted_df

def transform_country_data(df: pd.DataFrame, country: str, year: int) -> ResponseData:
    """Transform melted data into ResponseData structure."""
    metadata = Metadata(
        country=country,
        assessment_year=year
    )
    
    pillars = []
    pillar_codes = ['EP', 'CP', 'CF']
    
    for pillar_code in pillar_codes:
        pillar_data = df[df['pillar'] == pillar_code]
        if pillar_data.empty:
            continue
            
        areas = []
        unique_areas = pillar_data['area'].unique()
        
        for area_num in sorted(unique_areas):
            area_data = pillar_data[pillar_data['area'] == area_num]
            area_value = None
            area_value_series = area_data[
                (area_data['type'] == 'area') &
                (area_data['pillar'] == pillar_code)
            ]['value']
            
            if not area_value_series.empty and pd.notna(area_value_series.iloc[0]):
                area_value = str(area_value_series.iloc[0])
            
            area = Area(
                name=f"{pillar_code}.{area_num}",
                assessment=area_value,
                indicators=[]
            )
            
            # Process indicators for this area
            indicators_data = area_data[area_data['type'] == 'indicator']
            for _, ind_row in indicators_data.iterrows():
                indicator_value = None
                if pd.notna(ind_row['value']):
                    indicator_value = str(ind_row['value'])
                
                # Get source for this indicator if available
                source_col = f"source indicator {pillar_code}.{area_num}.{ind_row['indicator']}"
                source_value = None
                if source_col in df.columns and pd.notna(ind_row[source_col]):
                    source_value = str(ind_row[source_col])
                
                indicator = Indicator(
                    name=f"{pillar_code}.{area_num}.{ind_row['indicator']}",
                    assessment=indicator_value,
                    metrics=[],
                    source=source_value
                )
                
                # Check for corresponding metrics
                metric_data = area_data[
                    (area_data['type'] == 'metric') &
                    (area_data['indicator'] == ind_row['indicator'])
                ]
                
                # Process all metrics for this indicator
                for _, metric_row in metric_data.iterrows():
                    if pd.notna(metric_row['value']):
                        metric = Metric(
                            name=f"{pillar_code}.{area_num}.{ind_row['indicator']}.{metric_row['metric']}",
                            value=str(metric_row['value'])
                        )
                        indicator.metrics.append(metric)
                
                # Set metrics to None if no metrics were found
                if not indicator.metrics:
                    indicator.metrics = None
                
                area.indicators.append(indicator)
            
            if area.indicators or area.assessment:
                areas.append(area)
        
        if areas:
            pillars.append(Pillar(name=pillar_code, areas=areas))
    
    return ResponseData(
        metadata=metadata,
        pillars=pillars
    )
