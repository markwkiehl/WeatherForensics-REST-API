# WeatherForensics REST API

**Past Weather. Present Impact. AI-Ready Intelligence**

WeatherForensics is a Data as a Service (DaaS) that provides comprehensive historical weather data, including standard conditions and severe weather events, relative to a specified target location and timestamp. While most services focus on the "what," our proprietary engine calculates the localized impact of historical weather events—ranging from localized tornadoes to regional hurricanes—at a specific coordinate and datetime.

This repository contains information, documentation, and a sample Python client script (`rest_api_noaa_client.py`) to interact with the WeatherForensics Representational State Transfer (REST) Application Programming Interface (API).  

See also the WeatherForensics website at [WeatherForensics.dev](https://weatherforensics.dev/).

---

## 🚀 Features

* **Developer-Ready Formats:** Responses from all endpoints are delivered as clean JavaScript Object Notation (JSON) data structures, optimized for immediate human and Artificial Intelligence (AI) agent consumption.
* **Transparent Data Provenance:** Every JSON payload explicitly identifies the data content category and its authoritative source dataset.
* **Intelligent Dataset Routing:** The API automatically selects the most appropriate dataset—either the legacy National Oceanic and Atmospheric Administration (NOAA) National Centers for Environmental Information (NCEI) Integrated Surface Database (ISD) hourly dataset or the modern Global Historical Climatology Network hourly (GHCNh) dataset—based on your requested target year.
* **Precision Spatial Querying:** For standard and severe weather requests, the engine automatically identifies the closest active station to your target coordinates that contains the most robust dataset.
* **Advanced Cyclone Impact Analysis:** For tropical cyclone tracking, the API calculates the minimum distance between the storm centroid and your target, evaluating the maximum wind experienced utilizing standard 34, 50, and 64-knot wind radii models.
* **Cross-Platform Compatibility:** Fully supported across Linux, macOS, and Windows environments.

---

## 📊 Data Scope & Available Endpoints

The API provides access to standard meteorological data and severe weather tracking via the following `POST` endpoints.

**Standard Weather Endpoints:** (Sourced from NOAA NCEI)
- `/api/noaa_ncei_monthly_weather`
- `/api/noaa_ncei_daily_weather`
- `/api/noaa_ncei_hourly_weather`

**Severe Weather Endpoints:** (Sourced from NOAA NCEI Severe Weather Data Inventory (SWDI))
- `/api/noaa_swdi_nx3tvs_tornado_impact_to_location`
- `/api/noaa_swdi_supercell_storm_nx3mda_impact_to_location`
- `/api/noaa_swdi_nx3hail_impact_to_location`
- `/api/noaa_swdi_nx3structure_impact_to_location`

**Tropical Cyclone Endpoints:** (Derived from NOAA National Hurricane Center (NHC) HURDAT2)
- `/api/noaa_nhc_tropical_cyclone/impact_to_location`

---

## ⚙️ Installation & Configuration

### Prerequisites
The included sample script `rest_api_noaa_client.py` requires Python 3.7+ and the following packages:
```bash
pip install httpx asyncio python-json-logger
```

### Setup
1. Clone this repository and open `rest_api_noaa_client.py`.
2. Configure the `BASE_URL` and `API_KEY` constants at the top of the script based on your service tier.
    * **Forever Free Tier:** Leave `API_KEY = None`. Use the default `BASE_URL`: `"https://api-noaa-free-pnu3qtlxoa-uk.a.run.app"`.
    * **Pro Tier:** Enable the `BASE_URL` of "https://weatherforensics.dev/api/pro" and set `API_KEY` to your 39-character key.
    * **Enterprise Tier:** Update `BASE_URL` to your custom gateway URL and set `API_KEY` to your 39-character key.

### Usage
Execute the client script from your terminal:
```bash
python rest_api_noaa_client.py
```

---

## 📈 Service Tiers & Rate Limits

WeatherForensics is deployed on Google Cloud Run and offers predictable pricing to power your applications. All tiers include access to both the Model Context Protocol (MCP) Server and the Representational State Transfer (REST) Application Programming Interface (API).

| Tier | Price | Rate Limits & Quotas | Infrastructure |
| :--- | :--- | :--- | :--- |
| **Forever Free** | $0/mo | 10-15 Requests Per Minute (RPM), 500 Req/Day, 1 Concurrent | Shared Community Resource |
| **Pro** | $29/mo | 60 RPM, 10,000 Req/Day, 5 Concurrent | Dedicated Endpoints, Zero Cold Starts |
| **Enterprise** | $279/mo | 500+ RPM, Unlimited Concurrency | Dedicated Instance, Custom Bulk Payloads |

*Note: Free tier users do not need an API key. Excessive volume on the free tier may result in Internet Protocol (IP) throttling or severe latency. Exceeding your tier's rate limits will return a Hypertext Transfer Protocol (HTTP) `429 Too Many Requests` status code.*

---

## 💻 Example Requests & Responses

All endpoints require a JSON `POST` payload containing the target coordinates and local datetime in ISO format.
When using the Forever Free subscription tier URL (https://weatherforensics.dev/api/free), your first request may return "Error: Request timed out" due to the server cold start.


**Standard Request Payload Format**:
```json
{
    "latitude": 40.4407,
    "longitude": -76.12267,
    "local_datetime_iso": "2025-07-10T00:00:00"
}
```

**cURL**:
```bash
curl --location 'https://weatherforensics.dev/api/free/api/noaa_ncei_monthly_weather' \
--header 'Content-Type: application/json' \
--data '{
    "latitude": 40.4407,
    "longitude": -76.12267,
    "local_datetime_iso": "2025-07-10T00:00:00"
}'
```

**Postman**
```bash
postman request POST 'https://weatherforensics.dev/api/free/api/noaa_ncei_monthly_weather' \
  --header 'Content-Type: application/json' \
  --body '{"latitude":40.4407,"longitude":-76.12267,"local_datetime_iso":"2025-07-10T00:00:00"}'
```


### Monthly Weather
Target: 40.4407, -76.12267 on 10 July 2025
```json
{
    "event_type": "monthly_weather",
    "data_source": "NOAA_NCEI_Search_&_Data_Service_API",
    "target_metadata": {
        "latitude": 40.4407,
        "longitude": -76.12267,
        "datetime_local": "2025-07-10T00:00:00"
    },
    "station_metadata": {
        "distance_from_target_mi": 9.8,
        "STATION": "USW00014712",
        "LATITUDE": 40.37342,
        "LONGITUDE": -75.95924,
        "ELEVATION_ft": 331.9
    },
    "data": [
        {
            "measurement": "Precipitation",
            "value": "6.69",
            "unit": "\"",
            "category": "Precipitation"
        },
        {
            "measurement": "Maximum temperature",
            "value": "89.2",
            "unit": "°F",
            "category": "Temperature"
        }
    ]
}
```

### Daily Weather
Target: 40.4407, -76.12267 on 10 July 2025
```json
{
    "event_type": "daily_weather",
    "data_source": "NOAA_NCEI_Search_&_Data_Service_API",
    "target_metadata": {
        "latitude": 40.4407,
        "longitude": -76.12267,
        "datetime_local": "2025-07-10T00:00:00"
    },
    "station_metadata": {
        "distance_from_target_mi": 9.8,
        "STATION": "USW00014712",
        "DATE": "2025-07-10",
        "LATITUDE": 40.37342,
        "LONGITUDE": -75.95924,
        "ELEVATION_ft": 331.9
    },
    "data": [
        {
            "measurement": "Maximum temperature",
            "value": "88",
            "unit": "°F",
            "category": "Temperature"
        },
        {
            "measurement": "Fastest 5-second wind speed",
            "value": "12.1",
            "unit": "mph",
            "category": "Wind"
        }
    ]
}
```

### Hourly Weather
Target: 40.4407, -76.12267 on 10 July 2025 at 13:00:00
```json
{
    "event_type": "hourly_weather",
    "data_source": "NOAA_NCEI_Search_&_Data_Service_API",
    "target_metadata": {
        "latitude": 40.4407,
        "longitude": -76.12267,
        "datetime_local": "2025-07-10T13:00:00"
    },
    "station_metadata": {
        "distance_from_target_mi": 9.8,
        "STATION_NAME": "READING RGNL AP",
        "timestamp_utc": "2025-07-10T09:54:02+00:00",
        "STATION": "USW00014712",
        "LATITUDE": 40.3733,
        "LONGITUDE": -75.9592,
        "ELEVATION_ft": 332.0
    },
    "data": [
        {
            "measurement": "precipitation",
            "value": 0.0,
            "unit": "mm",
            "category": "Moisture"
        },
        {
            "measurement": "relative_humidity",
            "value": 71.0,
            "unit": "%",
            "category": "Moisture"
        },
        {
            "measurement": "station_level_pressure",
            "value": 1002.6,
            "unit": "hPa",
            "category": "Pressure"
        },
        {
            "measurement": "pressure_3hr_change",
            "value": 1.3,
            "unit": "hPa",
            "category": "Pressure"
        },
        {
            "measurement": "altimeter",
            "value": 1015.6,
            "unit": "hPa",
            "category": "Pressure"
        },
        {
            "measurement": "sea_level_pressure",
            "value": 1015.8,
            "unit": "hPa",
            "category": "Pressure"
        },
        {
            "measurement": "dew_point_temperature",
            "value": 20.0,
            "unit": "\u00b0C",
            "category": "Temperature"
        },
        {
            "measurement": "temperature",
            "value": 25.6,
            "unit": "\u00b0C",
            "category": "Temperature"
        },
        {
            "measurement": "wet_bulb_temperature",
            "value": 21.9,
            "unit": "\u00b0C",
            "category": "Temperature"
        },
        {
            "measurement": "visibility",
            "value": 16.093,
            "unit": "km",
            "category": "Visibility"
        },
        {
            "measurement": "wind_speed",
            "value": 2.1,
            "unit": "m/s",
            "category": "Wind"
        },
        {
            "measurement": "wind_direction",
            "value": 190.0,
            "unit": "\u00b0",
            "category": "Wind"
        }
    ]
}
```

### Tropical Cyclone Impact
Target: 26.674, -82.248 on 28 September 2022
```json
{
    "event_type": "tropical_cyclone",
    "data_source": "NOAA_NHC_HURDAT2_Database",
    "target_metadata": {
        "latitude": 26.674,
        "longitude": -82.248,
        "datetime_local": "2022-09-28T04:00:00+00:00"
    },
    "storm_metadata": {
        "storm_season": 2022,
        "count_of_tropical_cyclones": 35
    },
    "cyclone_report": {
        "STORM_NAME": "IAN (AL092022)",
        "OBSERVATION_TIMESTAMP_LOCAL": "28 Sep 2022 14:00:00",
        "DISTANCE_FROM_STORM_TRACK_CENTROID_TO_TARGET_mi": 3.5,
        "MAX_SUSTAINED_WIND_SPEED_mph": 155.4,
        "IMPACT_ANALYSIS": "CRITICAL wind impact measured"
    }
}
```

### Tornado Impact Analysis (nx3tvs)
Target: 40.7037, -89.4148 on 17 November 2013
```json
{
    "event_type": "tornado_vortex_signature",
    "data_source": "NOAA_NCEI_SWDI_NX3TVS",
    "target_metadata": {
        "latitude": 40.7037,
        "longitude": -89.4148,
        "datetime_utc": "2013-11-17T06:00:00Z"
    },
    "impact_analysis": {
        "target_cpa_miles": 1.66,
        "impact_category": "Direct Hit / Core Tornado Impact",
        "threat_level": "Extreme",
        "description": "Target is within 2 miles of the TVS track. High probability of tornadic impact.",
        "required_agent_actions": [
            "Overlay target with active NWS GIS warning polygons."
        ],
        "rankine_estimated_wind_kts": 23.5
    },
    "cpa_radar_metrics": {
        "time_utc": "2013-11-17T17:03:14Z",
        "time_to_cpa_minutes": 663.2,
        "storm_cell_id": "R2",
        "wsr_id": "KILX",
        "maximum_delta_velocity_kts": 146.0,
        "maximum_shear": 69.0,
        "azimuth_deg": 348.0,
        "range_nm": 33.0
    }
}
```

### Supercell Storm (nx3mda)
Target: 35.3412, -97.4867 on 20 May 2013
```json
{
    "event_type": "supercell_mesocyclone",
    "data_source": "NOAA_NCEI_SWDI_NX3MDA",
    "target_metadata": {
        "latitude": 35.3412,
        "longitude": -97.4867,
        "datetime_utc": "2013-05-20T05:00:00Z"
    },
    "impact_analysis": {
        "target_cpa_miles": 0.93,
        "impact_category": "Direct Hit / Core Impact",
        "threat_level": "Extreme",
        "description": "Target was within 3 miles of the mesocyclone track. High probability of tornadoes or extreme winds.",
        "dual_pol_warning": null
    },
    "cpa_radar_metrics": {
        "time_utc": "2013-05-20T20:22:57Z",
        "time_to_cpa_minutes": 923.0,
        "storm_cell_id": "496",
        "distance_from_radar_core_mi": 0.93,
        "tornado_vortex_signature": "N",
        "low_level_delta_velocity_kts": 86,
        "strength_rank": 7.0,
        "tornadic_potential": "High"
    }
}
```

### Hail Storm (nx3hail)
Target: 42.31476, -88.44616 on 27 August 2024
```json
{
    "event_type": "hail_storm",
    "data_source": "NOAA_NCEI_SWDI_NX3HAIL",
    "target_metadata": {
        "latitude": 42.31476,
        "longitude": -88.44616,
        "datetime_utc": "2024-08-27T05:00:00Z"
    },
    "impact_analysis": {
        "target_cpa_miles": 1.37,
        "impact_category": "Near Miss / Hail Impact",
        "threat_level": "High",
        "description": "Target was within 1 to 5 miles of the hail core. Severe probability: 60.0%.",
        "dual_pol_warning": null
    },
    "cpa_radar_metrics": {
        "time_utc": "2024-08-27T22:36:37Z",
        "time_to_cpa_minutes": 1056.6,
        "storm_cell_id": "C0",
        "wsr_id": "KMKE",
        "distance_from_radar_core_mi": 4.45,
        "hail_probability_pct": 100.0,
        "severe_probability_pct": 60.0,
        "max_hail_size_in": 1.5
    }
}
```

### Storm Cell Structure (nx3structure)
Target: 41.3110, -94.4650 on 21 May 2024
```json
{
    "event_type": "storm_cell_structure",
    "data_source": "NOAA_NCEI_SWDI_NX3STRUCTURE",
    "target_metadata": {
        "latitude": 41.311,
        "longitude": -94.465,
        "datetime_utc": "2024-05-21T05:00:00Z"
    },
    "impact_analysis": {
        "target_cpa_miles": 0.58,
        "impact_category": "Direct Hit / Core Impact",
        "description": "Target was within 3 miles of the storm core track. High probability of heavy precipitation, large hail, or severe wind."
    },
    "cpa_radar_metrics": {
        "time_utc": "2024-05-21T12:31:55Z",
        "time_to_cpa_minutes": 451.9,
        "storm_cell_id": "U0",
        "wsr_id": "KDMX",
        "distance_from_radar_core_mi": 73.55,
        "max_reflectivity_dbz": 55,
        "vertically_integrated_liquid_kg_m2": 15
    }
}
```


---

## 🛑 Error Handling & HTTP Status Codes

When integrating the API, you may encounter the following standard HTTP status codes:

- **`200 OK`**: The request was successful and the JavaScript Object Notation (JSON) payload is returned.
- **`400 Bad Request`**: The request payload is malformed, missing required fields (`latitude`, `longitude`, `local_datetime_iso`), or contains invalid coordinates/dates.
- **`401 Unauthorized`**: An invalid or missing API Key was provided for a Pro/Enterprise tier endpoint.
- **`429 Too Many Requests`**: You have exceeded the rate limits for your specific subscription tier. Back off and retry later.
- **`500 Internal Server Error`**: An unexpected error occurred on the server (e.g., upstream National Oceanic and Atmospheric Administration (NOAA) API timeouts).
- **`504 Gateway Timeout`**: The upstream NOAA API server is offline).

---

## ⚖️ Licensing, Attribution & Terms

When integrating the WeatherForensics Application Programming Interface (API) or Model Context Protocol (MCP) into your applications, you must comply with the following usage and attribution requirements.

*Note: The client scripts in this repository are open-sourced under the [Massachusetts Institute of Technology (MIT) License](LICENSE). Access to the WeatherForensics API and its data is strictly subject to our full [Terms of Service](https://weatherforensics.dev/tos.html).*

### 1. Usage Rights & Restrictions

* **Allowed:** You may use the data for internal analysis, commercial applications, and providing ground-truth context to Artificial Intelligence (AI) models.
* **Restricted:** You may not systematically scrape, bulk-download, resell, or redistribute the raw API/MCP responses as a competing standalone weather data service.

### 2. Required End-User Attribution

To comply with National Oceanic and Atmospheric Administration (NOAA) guidelines, any public-facing application or AI agent interface displaying our data must include the following attribution visibly to the end-user:

> "Weather data derived from NOAA National Centers for Environmental Information (NCEI) and the National Hurricane Center (NHC). This application and its data are not official NOAA products and do not represent any agency determination, view, or policy."

### 3. Acknowledgments & Disclaimers

**Data Sources:** Tropical cyclone impact analysis is derived from the HURDAT2 database *(Landsea, C. W., and J. L. Franklin, 2013)*. Our backend utilizes the `hurdat2parser` library (Copyright © 2019-2021 Kyle S. Gentry), licensed under the MIT License.

**Disclaimer:** The service is provided on an "AS IS" and "AS AVAILABLE" basis. Data should not be used as the sole basis for life-safety decisions, financial trading, or legal determinations.

---


Copyright © 2026 [Mechatronic Solutions LLC](http://mechatronicsolutionsllc.com/). All Rights Reserved. For full terms, visit [WeatherForensics.dev](https://weatherforensics.dev/).

