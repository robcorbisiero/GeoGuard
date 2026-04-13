import os
from google import genai
from google.genai import types

def generate_recommendation(elevation: float, climate_data: dict, land_cover: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "WARN: GEMINI_API_KEY not set. Mock Recommendation: Ensure property has backwater valves installed and clear 30m brush perimeter."

    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""
        You are an expert geospatial risk assessor for an insurance company.
        Based on the following data, provide a 2-3 sentence 'Resilience Recommendation' for a property:

        - Elevation: {elevation} meters above sea level
        - Yearly precipitation: {climate_data.get('avg_yearly_rainfall')} mm
        - Max Historical Temperature: {climate_data.get('max_temp')} °C
        - Land Cover Type: {land_cover}

        Focus on flood, heat, or wildfire risks.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"GenAI Error: {e}")
        return "Error generating recommendation. Please check API key and connectivity."
