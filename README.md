# GeoGuard

GeoGuard is a containerized, full-stack geospatial risk assessment application designed for the insurance industry. The application converts text-based addresses into precise risk profiles, visualizing data on an interactive map and generating AI-powered Resilience Recommendations.

## Architecture

- **Frontend:** Built with Vite and React. Utilizes `react-leaflet` for interactive mapping, `chart.js` for data visualization, and custom vanilla CSS for a premium dark-mode aesthetic.
- **Backend:** High-performance REST API built with FastAPI (Python). 
- **Integrations:**
  - **Geocoding:** Converts text locations to coordinates via `geopy` and Nominatim (OpenStreetMap).
  - **Climate Engine:** Fetches coordinate-specific elevation and 10-year historic weather trends via Open-Meteo API.
  - **AI Engine:** Evaluates geographic risk proxies (elevation, rainfall, max temperature, land cover) against `gemini-1.5-pro` to synthesize dynamic recommendations.

## Setup & Local Deployment

The application is fully containerized using Docker Compose.

### Prerequisites
- Docker Engine / Docker Desktop
- A Google Gemini API Key 

### Environment Variables
Optionally, set your Gemini API key in your terminal context to enable real AI generation:
```bash
set GEMINI_API_KEY="your-api-key-here" # Windows Command Prompt
$env:GEMINI_API_KEY="your-api-key-here" # Windows PowerShell
export GEMINI_API_KEY="your-api-key-here" # Mac/Linux
```
*(If the key is omitting, the system gracefully generates mocked recommendations).*

### Running the App
1. Clone the repository and navigate into the project directory.
2. Run Docker Compose:
```bash
docker-compose up --build
```
3. Open your browser and navigate to `http://localhost:5173`.

## Custom Skill: Address-to-Risk Workflow
1. A user enters an address (e.g., "Miami, FL") in the frontend interface.
2. The FastApi Backend uses OpenStreetMap to locate the exact coordinates.
3. The API then retrieves historical rainfall metrics and localized elevation data via Open-Meteo.
4. The Gemini 1.5 Pro AI digests the collated environmental string and generates strategic recommendations (e.g. "Install backwater valves").
5. The frontend plots a 5000m heat radius over the geocoded location and populates the dashboard metrics.
