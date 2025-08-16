# Property API Backend

A comprehensive Django REST API for Cook County property data management and analysis. This backend provides detailed property information including location data, assessments, tax districts, school districts, environmental factors, and demographic information.

## Features

### Core Property Management
- **Comprehensive Property Database**: Store and manage detailed Cook County property records with 100+ data fields
- **Property Search & Filtering**: Advanced search capabilities by PIN, address, community area, ZIP code, and more
- **Geospatial Data**: Full coordinate support with nearby property discovery
- **Assessment Information**: Property valuations, land/building assessments, and tax data
- **Administrative Districts**: Ward, township, triad, and neighborhood classifications

### Search & Discovery APIs
- **Multi-type Search**: Search by PIN, ZIP code, community area, or combined queries
- **Autocomplete**: Real-time search suggestions for PINs and community areas
- **Nearby Properties**: Find properties within specified radius using coordinates
- **Advanced Filtering**: Filter by property class, vacancy status, tax codes, and more

### Specialized Data Endpoints
- **School District Information**: Elementary, secondary, and unified school district data
- **Tax District Details**: Municipality, library, fire protection, and TIF district information
- **Environmental Data**: Flood zones, airport noise levels, and economic zones
- **GeoJSON Export**: Map-ready data format for visualization applications

### Data Import & Management
- **Bulk Data Import**: Management commands for importing property data from CSV files
- **Search Index Creation**: Automated search optimization for fast queries
- **Data Validation**: Comprehensive data cleaning and normalization during import

### Authentication & Authorization
- **JWT Authentication**: Secure API access using JSON Web Tokens
- **OAuth Support**: Client application management for third-party integrations
- **User Management**: Registration, login, password reset functionality

## API Endpoints

All endpoints are available at `http://localhost:8000/api/v1/properties/`

### Property Listing & Details

#### `GET /api/v1/properties/`
List all properties with pagination and filtering.

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Results per page (max: 100, default: 25)
- `class_code`: Filter by property class code
- `zip_code`: Filter by ZIP code
- `ward_num`: Filter by Chicago ward number
- `township_name`: Filter by township
- `chicago_community_area_name`: Filter by community area
- `vacancy_type`: Filter by vacancy status
- `search`: Search across multiple fields (PIN, address, community area, etc.)
- `ordering`: Sort by fields (pin, zip_code, ward_num)

**Example Response:**
```json
{
  "count": 1250,
  "next": "http://localhost:8000/api/v1/properties/?page=2",
  "previous": null,
  "results": [
    {
      "pin": "17-16-401-001-0000",
      "pin10": "1716401001",
      "coordinates": [-87.6298, 41.8781],
      "address_display": "123 Main St, Chicago, IL",
      "chicago_community_area_name": "LOOP",
      "zip_code": "60601",
      "ward_num": 42,
      "total_assessed_value": "125000.00",
      "class_code": "2-11"
    }
  ]
}
```

#### `GET /api/v1/properties/{pin}/`
Get detailed information for a specific property by PIN.

**Example Response:**
```json
{
  "pin": "17-16-401-001-0000",
  "coordinates": [-87.6298, 41.8781],
  "address_display": "123 Main St, Chicago, IL",
  "property_address": "123 Main St",
  "property_city": "Chicago",
  "property_state": "IL",
  "total_assessed_value": "125000.00",
  "land_assessed_value": "45000.00",
  "building_assessed_value": "80000.00",
  "square_footage_land": 5000,
  "chicago_community_area_name": "LOOP",
  "ward_num": 42,
  "nearby_properties_count": 15,
  "environmental_data": {...},
  "tax_districts": {...}
}
```

### Search Endpoints

#### `GET /api/v1/properties/search/`
Advanced property search with multiple criteria.

**Query Parameters:**
- `q`: Search query (required)
- `type`: Search type (`all`, `pin`, `zip`, `area`)
- `limit`: Maximum results (default: 50, max: 100)

**Example:**
```
GET /api/v1/properties/search/?q=60601&type=zip&limit=25
```

#### `GET /api/v1/properties/autocomplete/`
Get search suggestions for autocomplete functionality.

**Query Parameters:**
- `q`: Partial search query (min 2 characters)
- `limit`: Maximum suggestions (default: 10, max: 20)

**Example Response:**
```json
{
  "suggestions": [
    {"value": "17-16-401", "type": "pin"},
    {"value": "LOOP", "type": "area"},
    {"value": "60601", "type": "zip"}
  ]
}
```

#### `GET /api/v1/properties/nearby/`
Find properties near a specific location.

**Query Parameters:**
- `lat`: Latitude (required)
- `lon`: Longitude (required)
- `radius`: Search radius in kilometers (default: 1.0)
- `limit`: Maximum results (default: 25, max: 100)

**Example:**
```
GET /api/v1/properties/nearby/?lat=41.8781&lon=-87.6298&radius=0.5
```

### Specialized Information Endpoints

#### `GET /api/v1/properties/{pin}/schools/`
Get school district information for a property.

**Example Response:**
```json
{
  "pin": "17-16-401-001-0000",
  "school_elementary_district_name": "Chicago Public Schools District 299",
  "school_secondary_district_name": "Chicago Public Schools District 299",
  "school_unified_district_name": null,
  "school_school_year": "2023-2024"
}
```

#### `GET /api/v1/properties/{pin}/tax/`
Get tax district information for a property.

#### `GET /api/v1/properties/{pin}/environment/`
Get environmental and economic zone information for a property.

### Map Data Endpoints

#### `GET /api/v1/properties/geojson/`
Get properties in GeoJSON format for map visualization.

**Query Parameters:**
- `north`, `south`, `east`, `west`: Bounding box coordinates
- `area`: Filter by community area name
- `class`: Filter by property class code
- `limit`: Maximum features (default: 500, max: 1000)

**Example Response:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-87.6298, 41.8781]
      },
      "properties": {
        "pin": "17-16-401-001-0000",
        "community_area": "LOOP",
        "zip_code": "60601",
        "popup_content": "PIN: 17-16-401-001-0000<br/>Area: LOOP<br/>ZIP: 60601"
      }
    }
  ]
}
```

### Statistics Endpoint

#### `GET /api/v1/properties/stats/`
Get summary statistics about the property database.

**Example Response:**
```json
{
  "total_properties": 125000,
  "community_areas": 77,
  "zip_codes": 65,
  "wards": 50,
  "property_classes": 25,
  "top_community_areas": [
    {"chicago_community_area_name": "LOOP", "count": 5000},
    {"chicago_community_area_name": "NEAR NORTH SIDE", "count": 4500}
  ]
}
```

## Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip and virtualenv

### Installation

1. Clone the repository
2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

or on Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/property_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Set up the database

```bash
# Create PostgreSQL database
createdb property_db

# Run migrations
python manage.py migrate
```

6. Create a superuser

```bash
python manage.py createsuperuser
```

7. Import property data (optional)

```bash
# Import Cook County data
python manage.py import_property_data --csv-path data/common_county_data_complete.csv

# Import SSA 32 specific data
python manage.py import_ssa32_data data/SSA32_Properties.csv
```

8. Run the server

```bash
python manage.py runserver
```

### Docker Setup

Alternatively, use Docker for easy setup:

```bash
docker-compose up --build
```

This will start:
- Django application on port 8000
- PostgreSQL database on port 5432
- Redis for caching on port 6379

## Data Import Commands

The API includes powerful management commands for importing property data from CSV files.

### Import Cook County Data

```bash
python manage.py import_property_data [options]
```

**Options:**
- `--csv-path`: Path to CSV file (default: `data/common_county_data_complete.csv`)
- `--batch-size`: Records per batch (default: 50)
- `--clear`: Clear existing data before import

**Example:**
```bash
python manage.py import_property_data \
  --csv-path /path/to/property_data.csv \
  --batch-size 100 \
  --clear
```

**Expected CSV Columns:**
- `pin`, `pin10`, `year`, `class`, `row_id`
- `lon`, `lat`, `x_3435`, `y_3435`, `zip_code`
- `triad_name`, `triad_code`, `township_name`, `township_code`
- `chicago_community_area_name`, `ward_num`
- Environmental fields: `env_flood_fema_sfha`, `env_airport_noise_dnl`
- Tax district fields: `tax_municipality_name`, etc.
- School district fields: `school_elementary_district_name`, etc.

### Import SSA 32 Properties

```bash
python manage.py import_ssa32_data <csv_file> [--clear]
```

**Example:**
```bash
python manage.py import_ssa32_data data/SSA32_Properties.csv --clear
```

**Expected CSV Columns:**
- `pin`, `tax_year`, `class`, `longitude`, `latitude`
- `property_address`, `property_city`, `property_state`, `property_zip`
- `total_assessed_value`, `land_assessed_value`, `building_assessed_value`
- `vacancy_type`, `taxpayer_id`, `mailing_name`, `mailing_address`
- `ward_number`, `tax_district_code`

### Data Processing Features

Both import commands include:
- **Data Validation**: Automatic cleaning and normalization of values
- **Error Handling**: Skip invalid records and continue processing
- **Search Index Creation**: Automatic generation of search indices
- **Batch Processing**: Memory-efficient processing of large datasets
- **Progress Reporting**: Real-time import status updates

## Usage

### Base URL
All API endpoints are available at: `http://localhost:8000/api/v1/`

### Authentication

#### User Registration
```bash
curl -X POST http://localhost:8000/auth/registration/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password1": "securepassword123",
    "password2": "securepassword123"
  }'
```

#### User Login
```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "pk": 1,
    "email": "user@example.com"
  }
}
```

#### Making Authenticated Requests
Include the access token in the Authorization header:

```bash
curl -X GET http://localhost:8000/api/v1/properties/ \
  -H "Authorization: Bearer your_access_token"
```

### Example API Usage

#### Search for Properties in a ZIP Code
```bash
curl "http://localhost:8000/api/v1/properties/search/?q=60601&type=zip&limit=10"
```

#### Get Property Details
```bash
curl "http://localhost:8000/api/v1/properties/17-16-401-001-0000/"
```

#### Find Nearby Properties
```bash
curl "http://localhost:8000/api/v1/properties/nearby/?lat=41.8781&lon=-87.6298&radius=0.5"
```

#### Get Properties for Map Visualization
```bash
curl "http://localhost:8000/api/v1/properties/geojson/?north=41.9&south=41.8&east=-87.6&west=-87.7&limit=100"
```

#### Filter Properties by Community Area
```bash
curl "http://localhost:8000/api/v1/properties/?chicago_community_area_name=LOOP&page_size=50"
```

### Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` to:
- Manage user accounts and permissions
- Create OAuth client applications
- View and edit property data
- Monitor system statistics

### OAuth Client Applications

To create a new client application for third-party integrations:

1. Go to the admin panel (`/admin/`)
2. Navigate to "Applications" under "DJANGO OAUTH TOOLKIT"
3. Click "Add Application"
4. Set the application type and authorization grant type
5. The `Client ID` and `Client Secret` will be generated automatically

## Property Data Model

The Property model contains comprehensive information about Cook County properties:

### Core Identifiers
- `pin`: Property Identification Number (full format)
- `pin10`: 10-digit PIN format
- `year`: Tax year
- `class_code`: Property class code
- `row_id`: Unique row identifier

### Location Data
- `longitude`, `latitude`: Geographic coordinates
- `x_3435`, `y_3435`: Illinois State Plane coordinates
- `zip_code`: ZIP code
- `property_address`, `property_city`, `property_state`: Physical address

### Assessment Information
- `total_assessed_value`: Total property assessment
- `land_assessed_value`: Land portion assessment
- `building_assessed_value`: Building portion assessment
- `square_footage_land`: Land square footage

### Administrative Districts
- `triad_name`, `triad_code`: Cook County triad information
- `township_name`, `township_code`: Township details
- `nbhd_code`: Neighborhood code
- `ward_num`: Chicago ward number
- `chicago_community_area_name`, `chicago_community_area_num`: Community area

### School Districts
- `school_elementary_district_name`, `school_elementary_district_geoid`
- `school_secondary_district_name`, `school_secondary_district_geoid`
- `school_unified_district_name`, `school_unified_district_geoid`

### Tax Districts
- `tax_municipality_name`, `tax_municipality_num`
- `tax_school_elementary_district_name`, `tax_school_secondary_district_name`
- `tax_community_college_district_name`
- `tax_fire_protection_district_name`
- `tax_library_district_name`, `tax_park_district_name`
- `tax_tif_district_name`, `tax_tif_district_num`

### Environmental Data
- `env_flood_fema_sfha`: FEMA Special Flood Hazard Area status
- `env_flood_fs_factor`: Flood factor score
- `env_ohare_noise_contour_no_buffer_bool`: O'Hare noise contour
- `env_airport_noise_dnl`: Airport noise level in DNL

### Economic Zones
- `econ_enterprise_zone_num`: Enterprise zone designation
- `econ_qualified_opportunity_zone_num`: Opportunity zone status

### Accessibility & Demographics
- `access_cmap_walk_id`: CMAP walkability ID
- `access_cmap_walk_nta_score`, `access_cmap_walk_total_score`: Walk scores
- `census_block_group_geoid`, `census_tract_geoid`: Census identifiers

### Taxpayer Information
- `taxpayer_id`: Taxpayer identifier
- `mailing_name`: Taxpayer name
- `mailing_address`, `mailing_city`, `mailing_state`, `mailing_zip`: Mailing address
- `vacancy_type`: Property vacancy status

## Performance & Optimization

### Database Indexes
The API includes optimized database indexes for:
- PIN lookups (primary and 10-digit formats)
- Geographic queries (latitude/longitude)
- Administrative divisions (community area, ward, township)
- ZIP code searches

### Pagination
All list endpoints support pagination with configurable page sizes to handle large datasets efficiently.

### Search Optimization
- Full-text search indices for fast property lookups
- Specialized autocomplete functionality
- Geographic bounding box queries for map applications

## Development

### Requirements
- Django 5.1.2
- Django REST Framework 3.15.2
- PostgreSQL with PostGIS (recommended for geographic queries)
- Redis (for caching)
- Pandas (for data import)

### Testing
```bash
python manage.py test
```

### Code Quality
The project follows Django best practices:
- Model validation and constraints
- Serializer-based API responses
- Proper error handling and status codes
- Comprehensive logging

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

If you find a bug or security vulnerability, please don't hesitate to create an issue or a pull request. Any contributions are welcome!

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Built by

This project was built by [Brandon Kong](https://github.com/brandon-kong).

