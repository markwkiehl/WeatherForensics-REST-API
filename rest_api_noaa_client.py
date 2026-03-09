#
#   Written by:  Mark W Kiehl
#   http://mechatronicsolutionsllc.com/
#   http://www.savvysolutions.info/savvycodesolutions/


# Define the script version in terms of Semantic Versioning (SemVer)
# when Git or other versioning systems are not employed.
__version__ = "0.0.2"
# v0.0.0    Release 2 February 2026 (rest_api_client.py)
# v0.0.1    Importing content from mcp_fastapi_noaa_client.py v0.2.2
# v0.0.2    Implement Google API Gateway


"""
WeatherForensics REST API Client

This script is a client that interacts with an RESTful API Server that has been deployed to Google Cloud Run service.

Update BASE_URL in this script with the Google Cloud Run URL for the WeatherForensics API Server. 


WeatherForensics Server Endpoints:

Endpoint                                                    HTTP Method
--------------------------------------------------------    -----------
/api/noaa_ncei_monthly_weather                              POST
/api/noaa_ncei_daily_weather                                POST
/api/noaa_ncei_hourly_weather                               POST
/api/noaa_nhc_tropical_cyclone/impact_to_location           POST
/api/noaa_swdi_nx3tvs_tornado_impact_to_location            POST
/api/noaa_swdi_supercell_storm_nx3mda_impact_to_location    POST
/api/noaa_swdi_nx3hail_impact_to_location                   POST
/api/noaa_swdi_nx3structure_impact_to_location              POST


"""

from pathlib import Path
# pip install httpx asyncio
import httpx
import asyncio
import sys

from datetime import datetime




# ---------------------------------------------------------------------------
# Configure logging

# NOTE:
# Always use logger rather than print.  At scale, you can filter the logs by .info, .warning, and .error.
# By default, print() goes to stdout. Depending on the environment, the Python root logger might be sending logs to stderr. 
# You can set an Environment Variable in Cloud Run LOG_LEVEL=WARNING. Even if the code is full of logger.info() calls, they will be discarded instantly by the logger and never sent to Google Cloud
# While Cloud Run captures both print() and logger, they are often processed by different buffers.
# Google Cloud Logging looks for a field named severity to categorize logs (Blue for Info, Orange for Warning, Red for Error). The python-json-logger uses levelname by default.

# Install with: pip install python-json-logger
import logging

# Use a named logger
logger = logging.getLogger(Path(__file__).stem)
logger.setLevel(logging.INFO)

# Setup a standard Text Handler (Not JSON)
# This is what gcloud CLI "pretty prints" best.
if not logger.handlers:
    # Cloud Run captures everything on stdout
    logHandler = logging.StreamHandler(sys.stdout)
    
    # Use a clean, classic format: [LEVEL] Message
    # This format is highly readable in both the CLI and the Console.
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    logHandler.setFormatter(formatter)
    
    logger.addHandler(logHandler)

# Prevent double-logging
logger.propagate = False

logger.info(f"'{Path(__file__).stem}.py' v{__version__}") 
# logger.info(), logger.warning(), logger.error()


# Force UTF-8 encoding for Windows consoles to handle bullet points (•)
#sys.stdout.reconfigure(encoding='utf-8')

# ----------------------------------------------------------------------
# Constants

DEBUG = False

# __file__ is /app/src/main.py
# .parent is /app/src
# .parent.parent is /app
PATH_BASE = Path(__file__).resolve().parent.parent
PATH_GCP = PATH_BASE / "gcp"
PATH_SRC = PATH_BASE / "src"
# Define the data directory: /app/data
PATH_DATA = PATH_BASE / "data"

# The Forever Free Tier clients will use the following BASE_URL:
BASE_URL = "https://api-noaa-free-pnu3qtlxoa-uk.a.run.app"
API_KEY = None

# If you are a paid subscriber, update the BASE_URL and API_KEY below with those provide to you with your subscription:
#BASE_URL = "https://gateway-id-api-####-v#-#-########.uk.gateway.dev"
#API_KEY = "your-39-character-api-key-#############"

if DEBUG: logger.info(f"BASE_URL: {BASE_URL}")

# ----------------------------------------------------------------------
# Call API Server Endpoints

async def get_server_status(client: httpx.AsyncClient, verbose:bool=False) -> bool:
    """
    Checks the server status using a shared client. 
    Returns True if the server responds successfully, False otherwise.
    """
    try:
        # We check the OpenAPI spec as a heartbeat
        response = await client.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            spec = response.json()

            # Extract info dictionary
            info = spec.get("info", {})
            title = info.get("title", "Unknown")
            description = info.get("description", "No description provided")

            # Extract version and contact
            version = info.get("version", "Unknown")
            contact = info.get("contact", {})
            contact_name = contact.get("name", "Unknown")
            contact_url = contact.get("url", "No Uniform Resource Locator (URL) provided")

            if verbose:
                logger.info(f"--- Server '{title}' v{version} is ONLINE ---")
                logger.info(f"Server Description: {description}")

            # Extract available endpoint paths, HTTP methods, status codes, & query parameters.
            endpoints_to_ignore = [
                "/healthz",
                "/readyz",
                "/ready",
                "/",
            ]
            endpoints = []
            paths = spec.get("paths", {})
            for path, methods_dict in paths.items():
                if not path in endpoints_to_ignore:
                    for method, operation in methods_dict.items():
                        
                        # Extract query and path parameters
                        parameters = operation.get("parameters", [])
                        param_names = [f"{p.get('name')} ({p.get('in')})" for p in parameters]
                        
                        # Check for a required request body
                        request_body = operation.get("requestBody", {})
                        body_required = request_body.get("required", False)
                        
                        endpoints.append(f"{path} | [{method.upper()}] | "
                            f"Params: {', '.join(param_names) or 'None'} | "
                            f"Body Required: {body_required}"
                        )
            # Append \n to each item, then join with an empty string
            endpoints = "".join([f"{item}\n" for item in endpoints])

            if verbose:
                logger.info(f"Endpoints:\n{endpoints}")

                logger.info(f"Contact: {contact_name} at {contact_url}")

            return True
        return False
    except (httpx.RequestError, httpx.HTTPStatusError):
        logger.error(f"--- Server is OFFLINE at {BASE_URL} ---")
        return False


# /api/noaa_ncei_monthly_weather
async def run_get_noaa_ncei_monthly_weather(client: httpx.AsyncClient, latitude:float, longitude:float, local_datetime:datetime):
    """
    
    """
    endpoint = "/api/noaa_ncei_monthly_weather"
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"--- Executing tool endpoint {endpoint} ---")

    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "local_datetime_iso": local_datetime.isoformat(),
    }

    try:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result_data = response.json()
        print(f"Output Message: {result_data.get('message')}")
        print(f"Weather Summary: {result_data.get('weather_summary')}")
        """
        Output Message: Monthly weather for 2025-07-10 00:00:00 at 40.4407,-76.12267
        Weather Summary: {
            "target_metadata": {
                "latitude": 40.4407,
                "longitude": -76.12267,
                "datetime_local": "2025-07-10T00:00:00"
            },
            "station_metadata": {
                "station_id": "USW00014712",
                "distance_from_target_mi": null,
                "station_latitude": 40.37342,
                "station_longitude": -75.95924,
                "station_name": null,
                "latitude": 40.37342,
                "longitude": -75.95924,
                "start_date_local": "2025-07",
                "end_date_local": "2025-07"
            },
            "data": [
                {
                    "measurement": "Precipitation",
                    "value": "6.69",
                    "unit": "\"",
                    "category": "Precipitation"
                },
                {
                    "measurement": "Snowfall",
                    "value": "0.0",
                    "unit": "\"",
                    "category": "Precipitation"
                },
                {
                    "measurement": "Maximum temperature",
                    "value": "89.2",
                    "unit": "\u00b0F",
                    "category": "Temperature"
                },
                {
                    "measurement": "Average temperature",
                    "value": "80.0",
                    "unit": "\u00b0F",
                    "category": "Temperature"
                },
                {
                    "measurement": "Minimum temperature",
                    "value": "70.7",
                    "unit": "\u00b0F",
                    "category": "Temperature"
                },
                {
                    "measurement": "Direction of fastest 2-minute wind",
                    "value": "300",
                    "unit": "\u00b0",
                    "category": "Wind"
                },
                {
                    "measurement": "Direction of fastest 5-second wind",
                    "value": "300",
                    "unit": "\u00b0",
                    "category": "Wind"
                },
                {
                    "measurement": "Fastest 2-minute wind speed",
                    "value": "49.0",
                    "unit": "mph",
                    "category": "Wind"
                },
                {
                    "measurement": "Fastest 5-second wind speed",
                    "value": "63",
                    "unit": "mph",
                    "category": "Wind"
                },
                {
                    "measurement": "Average daily wind speed",
                    "value": "4.5",
                    "unit": "mph",
                    "category": "Wind"
                }
            ]
        }
        """

        logger.info("-" * 20)
    except Exception as e:
        logger.error(f"ERROR: Failed to execute tool call. Details: {e}")


# /api/noaa_ncei_daily_weather
async def run_get_noaa_ncei_daily_weather(client: httpx.AsyncClient, latitude:float, longitude:float, local_datetime:datetime):
    """
    
    """
    endpoint = "/api/noaa_ncei_daily_weather"
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"--- Executing tool endpoint {endpoint} ---")

    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "local_datetime_iso": local_datetime.isoformat(),
    }

    try:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result_data = response.json()
        
        #print(f"\nresult_data:\n{result_data}\n")
        # {'weather_summary': 'WEATHER DATA REPORT: Daily Observation\nMetadata:\n • Target Date (local): 10 Jul 2025\n • Target Coordinates: 40.4407,-76.12267\nWeather:\n • Temperature: Low 68 °F | High 87 °F\n • Wind Velocity: 8.9 mph at 160 degrees\n • Peak Gust: 12.1 mph at 150 degrees\n', 'message': 'Daily weather for 2025-07-10 00:00:00 at 40.4407,-76.12267'}
        
        print(f"Output Message: {result_data.get('message')}")
        print(f"Weather Summary: {result_data.get('weather_summary')}")
        """
        Output Message: Daily weather for 2025-07-10 00:00:00 at 40.4407,-76.12267
        Weather Summary: {
            "target_metadata": {
                "latitude": 40.4407,
                "longitude": -76.12267,
                "datetime_local": "2025-07-10T00:00:00"
            },
            "station_metadata": {
                "station_id": "USW00014712",
                "distance_from_target_mi": 9.8,
                "station_latitude": 40.37342,
                "station_longitude": -75.95924,
                "STATION": "USW00014712",
                "DATE": "2025-07-10",
                "latitude": 40.37342,
                "longitude": -75.95924
            },
            "data": [
                {
                    "measurement": "Snowfall",
                    "value": "0.0",
                    "unit": "\"",
                    "category": "Precipitation"
                },
                {
                    "measurement": "Precipitation",
                    "value": "0.00",
                    "unit": "\"",
                    "category": "Precipitation"
                },
                {
                    "measurement": "Snow depth",
                    "value": "0.0",
                    "unit": "\"",
                    "category": "Precipitation"
                },
                {
                    "measurement": "Maximum temperature",
                    "value": "88",
                    "unit": "\u00b0F",
                    "category": "Temperature"
                },
                {
                    "measurement": "Average temperature",
                    "value": "77",
                    "unit": "\u00b0F",
                    "category": "Temperature"
                },
                {
                    "measurement": "Minimum temperature",
                    "value": "71",
                    "unit": "\u00b0F",
                    "category": "Temperature"
                },
                {
                    "measurement": "Fog, ice fog, or freezing fog",
                    "value": "    1",
                    "unit": null,
                    "category": "Weather Type"
                },
                {
                    "measurement": "Fastest 2-minute wind speed",
                    "value": "8.9",
                    "unit": "mph",
                    "category": "Wind"
                },
                {
                    "measurement": "Fastest 5-second wind speed",
                    "value": "12.1",
                    "unit": "mph",
                    "category": "Wind"
                },
                {
                    "measurement": "Direction of fastest 2-minute wind",
                    "value": "  160",
                    "unit": "\u00b0",
                    "category": "Wind"
                },
                {
                    "measurement": "Average daily wind speed",
                    "value": "2.91",
                    "unit": "mph",
                    "category": "Wind"
                },
                {
                    "measurement": "Direction of fastest 5-second wind",
                    "value": "  150",
                    "unit": "\u00b0",
                    "category": "Wind"
                }
            ]
        }

        """

        logger.info("-" * 20)
    except Exception as e:
        logger.error(f"ERROR: Failed to execute tool call. Details: {e}")


# /api/noaa_ncei_hourly_weather
async def run_get_noaa_ncei_hourly_weather(client: httpx.AsyncClient, latitude:float, longitude:float, local_datetime:datetime):
    """
    Get hourly weather from the NOAA NCEI API endpoint.
    Automatically switches between datasets global-historical-climatology-network-hourly & global-hourly based on the transition data of 1 Jan 2025. 
    """
    endpoint = "/api/noaa_ncei_hourly_weather"
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"--- Executing tool endpoint {endpoint} ---")

    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "local_datetime_iso": local_datetime.isoformat(),
    }

    try:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result_data = response.json()
        print(f"Output Message: {result_data.get('message')}")
        print(f"Weather Summary: {result_data.get('weather_summary')}")

        """
        """

    except Exception as e:
        logger.error(f"ERROR: Failed to execute tool call. Details: {e}")


# /api/noaa_nhc_tropical_cyclone/impact_to_location
async def run_get_noaa_nhc_cyclone_impact_to_location(client: httpx.AsyncClient, latitude:float, longitude:float, local_datetime:datetime):
    """
    
    """
    endpoint = "/api/noaa_nhc_tropical_cyclone/impact_to_location"
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"--- Executing tool endpoint {endpoint} ---")

    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "local_datetime_iso": local_datetime.isoformat(),
    }

    try:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result_data = response.json()
        
        if DEBUG: print(f"\nresult_data:\n{result_data}\n")
        # {'weather_summary': 'DATA REPORT: Tropical Cyclone Impact Analysis\nTarget:\n • Date: 28 Sep 2022\n • Coordinates: 26.674,-82.248\nTropical Cyclone Analysis:\n • Storm Name (ID): IAN (AL092022)\n • Observation datetime (local): 28 Sep 2022 14:00:00\n • Distance from storm track centroid to target: 3.5 miles\n • Max 1-minute sustained wind speed at target (gusts will be higher): 155.4 mph\nImpact Analysis:\n • CRITICAL wind impact measured.', 'message': 'Weather conditions from NOAA NHC for tropical cyclone impact at 26.674,-82.248 in 2022:\n'}
        
        print(f"Output Message: {result_data.get('message')}")
        print(f"Weather Summary: {result_data.get('weather_summary')}")
        """
        Output Message: Weather conditions from NOAA NHC for tropical cyclone impact at 26.674,-82.248 in 2022:

        Weather Summary: DATA REPORT: Tropical Cyclone Impact Analysis
        Target:
        • Date: 28 Sep 2022
        • Coordinates: 26.674,-82.248
        Tropical Cyclone Analysis:
        • Storm Name (ID): IAN (AL092022)
        • Observation datetime (local): 28 Sep 2022 14:00:00
        • Distance from storm track centroid to target: 3.5 miles
        • Max 1-minute sustained wind speed at target (gusts will be higher): 155.4 mph
        Impact Analysis:
        • CRITICAL wind impact measured.
        """

        logger.info("-" * 20)
    except Exception as e:
        logger.error(f"ERROR: Failed to execute tool call. Details: {e}")


# /api/noaa_swdi_nx3tvs_tornado_impact_to_location
async def run_get_noaa_swdi_nx3tvs_tornado_impact_to_location(client: httpx.AsyncClient, latitude:float, longitude:float, local_datetime:datetime):
    """
    Returns a report on any tornado impact to a specified location and year using data from NOAA NCEI Severe Weather Data Inventory (SWDI) API.
    """
    endpoint = "/api/noaa_swdi_nx3tvs_tornado_impact_to_location"
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"--- Executing tool endpoint {endpoint} ---")

    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "local_datetime_iso": local_datetime.isoformat(),
    }

    try:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result_data = response.json()
        
        #print(f"\nresult_data:\n{result_data}\n")
         
        print(f"Output Message: {result_data.get('message')}")
        print(f"Weather Summary: {result_data.get('weather_summary')}")
        """
        Output Message: Weather conditions from NOAA NCEI Severe Weather Data Inventory (SWDI) at 40.7037,-89.4148 on 17 Nov 2013:

        Weather Summary: DATA REPORT: Severe Weather Impact Analysis
        Target:
        • Date: 2013-11-17 06:00:00+00:00
        • Coordinates: 40.7037,-89.4148
        Severe Weather Analysis:
        • Impact Type: Significant Wind Event
        • Timestamp: 16:58:31 UTC
        • Minimum Distance: 3.30 miles
        • Peak Gust at Target: 65.9 mph
        • Storm Dynamics: Moving E at 56.4 mph
        • Intensity: Radar Shear of 69
        """

        logger.info("-" * 20)
    except Exception as e:
        logger.error(f"ERROR: Failed to execute tool call. Details: {e}")
        # Note: logger.exception() forces Python to print the full traceback, identifying exactly which line failed and why (Timeout vs. Encoding), even if the exception message is empty.
        logger.exception(f"ERROR: Failed to execute tool call. Details: {e}")


# /api/noaa_swdi_supercell_storm_nx3mda_impact_to_location
async def run_get_noaa_swdi_supercell_storm_nx3mda_impact_to_location(client: httpx.AsyncClient, latitude:float, longitude:float, local_datetime:datetime):
    """
    Returns a report on any supercell storm (nx3mda) impact to a specified specified location (latitude,longitude) and local date using data from NOAA NCEI Severe Weather Data Inventory (SWDI) API.
    
    NEXRAD Level-3 Mesocyclone Signatures  (A rotating updraft within a convective storm, typically a supercell thunderstorm).
    """
    endpoint = "/api/noaa_swdi_supercell_storm_nx3mda_impact_to_location"
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"--- Executing tool endpoint {endpoint} ---")

    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "local_datetime_iso": local_datetime.isoformat(),
    }

    try:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result_data = response.json()
        
        #print(f"\nresult_data:\n{result_data}\n")
         
        print(f"Output Message: {result_data.get('message')}")
        print(f"Weather Summary: {result_data.get('weather_summary')}")
        """
        """

        logger.info("-" * 20)
    except Exception as e:
        logger.error(f"ERROR: Failed to execute tool call. Details: {e}")
        # Note: logger.exception() forces Python to print the full traceback, identifying exactly which line failed and why (Timeout vs. Encoding), even if the exception message is empty.
        logger.exception(f"ERROR: Failed to execute tool call. Details: {e}")


# /api/noaa_swdi_nx3hail_impact_to_location
async def run_get_noaa_swdi_nx3hail_impact_to_location(client: httpx.AsyncClient, latitude:float, longitude:float, local_datetime:datetime):
    """
    Returns a report on any hail (nx3hail) impact to a specified specified location (latitude,longitude) and local date using data from NOAA NCEI SWDI API.
    
    nx3hail:        NEXRAD Level-3 Hail Signatures
    nx3hail predicts hail probability and maximum size.
    """
    endpoint = "/api/noaa_swdi_nx3hail_impact_to_location"
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"--- Executing tool endpoint {endpoint} ---")

    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "local_datetime_iso": local_datetime.isoformat(),
    }

    try:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result_data = response.json()
        
        #print(f"\nresult_data:\n{result_data}\n")
         
        print(f"Output Message: {result_data.get('message')}")
        print(f"Weather Summary: {result_data.get('weather_summary')}")
        """
        """

        logger.info("-" * 20)
    except Exception as e:
        logger.error(f"ERROR: Failed to execute tool call. Details: {e}")
        # Note: logger.exception() forces Python to print the full traceback, identifying exactly which line failed and why (Timeout vs. Encoding), even if the exception message is empty.
        logger.exception(f"ERROR: Failed to execute tool call. Details: {e}")


# /api/noaa_swdi_nx3structure_impact_to_location
async def run_get_noaa_swdi_nx3structure_impact_to_location(client: httpx.AsyncClient, latitude:float, longitude:float, local_datetime:datetime):
    """
    Returns a report on any nx3structure impact to a specified specified location (latitude,longitude) and local date using data from NOAA NCEI SWDI API.
    
    nx3structure:   NEXRAD Level-3 Storm Structure
    nx3structure tells you how massive and water-loaded the storm hitting a target is.  Impacts in terms of heavy rainfall, flash flooding, and storm intensity are assessed.

    """
    endpoint = "/api/noaa_swdi_nx3structure_impact_to_location"
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"--- Executing tool endpoint {endpoint} ---")

    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "local_datetime_iso": local_datetime.isoformat(),
    }

    try:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result_data = response.json()
        
        if DEBUG: print(f"\nresult_data:\n{result_data}\n")
         
        print(f"Output Message: {result_data.get('message')}")
        print(f"Weather Summary: {result_data.get('weather_summary')}")
        """
        """

        logger.info("-" * 20)
    except Exception as e:
        logger.error(f"ERROR: Failed to execute tool call. Details: {e}")
        # Note: logger.exception() forces Python to print the full traceback, identifying exactly which line failed and why (Timeout vs. Encoding), even if the exception message is empty.
        logger.exception(f"ERROR: Failed to execute tool call. Details: {e}")


async def main():
    # Initialize the client once to enable connection pooling
    async with httpx.AsyncClient(timeout=360.0, params={"key": API_KEY}) as client:
        # Pass the shared client to all functions

        # Check if the REST API server is up
        server_online = await get_server_status(client, verbose=False)
        if server_online: 
            logger.info(f"The server is ONLINE  {BASE_URL}")
        else:
            raise Exception(f"The REST API server is offline OR your API Gateway Key is invalid !  {BASE_URL}")
        
        # Test run_get_noaa_ncei_monthly_weather()
        # Monthly weather at 40.4407,-76.12267 on 10 July 2025
        #await run_get_noaa_ncei_monthly_weather(client, 40.4407, -76.12267, datetime(2025, 7, 10))

        # Test run_get_noaa_ncei_daily_weather()
        # Daily weather at 40.4407,-76.12267 on 10 July 2025
        await run_get_noaa_ncei_daily_weather(client, 40.4407, -76.12267, datetime(2025, 7, 10))

        # Test run_get_noaa_ncei_hourly_weather()
        # Hourly weather at 40.4407,-76.12267 on 10 July 2025 at 1 pm (local)
        await run_get_noaa_ncei_hourly_weather(client, 40.4407, -76.12267, datetime(2025, 7, 10, 13, 0, 0))

        # Test get_noaa_nhc_cyclone_impact_to_location()
        # Tropical cyclone at 26.674,-82.248 on 28 September 2022
        await run_get_noaa_nhc_cyclone_impact_to_location(client, 26.674, -82.248, datetime(2022, 9, 28))

        # Test run_get_noaa_swdi_nx3tvs_tornado_impact_to_location()
        # Tornado at 40.7037,-89.4148 on 17 November 2013
        await run_get_noaa_swdi_nx3tvs_tornado_impact_to_location(client, 40.7037, -89.4148, datetime(2013, 11, 17))

        # Test run_get_noaa_swdi_supercell_storm_nx3mda_impact_to_location
        # Supercell storm at 35.3412,-97.4867 on 20 May 2013
        #await run_get_noaa_swdi_supercell_storm_nx3mda_impact_to_location(client, 35.3412, -97.4867, datetime(2013,5,20))

        # Test run_get_noaa_swdi_nx3hail_impact_to_location
        # Hail at 42.31476,-88.44616 on 27 August 2024
        #await run_get_noaa_swdi_nx3hail_impact_to_location(client, 42.31476, -88.44616, datetime(2024, 8, 27))

        # Test run_get_noaa_swdi_nx3structure_impact_to_location
        # Storm at 41.3110,-94.4650 on 21 May 2024
        await run_get_noaa_swdi_nx3structure_impact_to_location(client, 41.3110, -94.4650, datetime(2024,5,21))


if __name__ == "__main__":
    asyncio.run(main())
