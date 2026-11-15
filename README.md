# GeoGuard — geospatial data prototype

An exploratory full-stack application that geocodes an address, retrieves elevation and historical weather, and displays a map with an optional generated recommendation.

**Status:** portfolio prototype. This is not a validated insurance risk model. Elevation and weather summaries are inputs to a demonstration, not evidence of a property's flood, wildfire, or insurability rating.

## What is implemented

- React/Vite frontend with Leaflet maps and charts.
- FastAPI POST /api/assess-risk endpoint.
- Nominatim geocoding and Open-Meteo elevation/archive requests.
- Approximately one year of weather records ending roughly one year before the request date. The code does not retrieve ten years of trends.
- Optional Google GenAI recommendation; the code configures gemini-2.5-flash. Without a key, the response explicitly labels its recommendation as mock output.
- Six offline regression tests for unavailable climate data versus valid zero measurements.

## Run locally

Requires Git and Docker with Compose. External geocoding/weather requests require internet access. A Gemini key is optional and may incur provider charges when used.

```bash
git clone https://github.com/robcorbisiero/GeoGuard.git
cd GeoGuard
docker compose up --build
```

Open http://localhost:5173 and API documentation at http://localhost:8000/docs. To enable generated recommendations, set GEMINI_API_KEY privately in your shell before starting Compose. Never put a real key in Git or frontend configuration.

## Run the tested part without cloud credentials

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install requests==2.32.5
python -m unittest discover -s tests -v
```

The tests mock HTTP responses and cover HTTP failures, timeouts, absent measurements, real sea-level elevation, and real zero rainfall. CI runs this suite. They do not validate live provider availability, model quality, frontend interactions, or the whole Docker stack.

## Engineering correction

Weather-service failures previously returned 0.0 elevation or zero-valued climate data. Those values could reach the recommendation path as if they were measured. Requests now have a timeout, reject HTTP errors, and return unavailable data on failure; the API's existing error branch handles that state.

## Limits and next work

There is no authentication, production rate limiting, calibrated risk scoring, or provider-contract test. The map radius is a visual aid, not a computed hazard boundary. Climate results are not a future climate projection. Dependencies and container startup need an end-to-end refresh before presenting this as a deployed product. Use synthetic locations and treat recommendations as illustrative.

**Portfolio context:** the [infrastructure homelab](https://github.com/robcorbisiero/enterprise-infrastructure-homelab) contains a separate evidence-based IT administration walkthrough.
