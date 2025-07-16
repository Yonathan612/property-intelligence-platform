# Chicago Property Search & Interactive Map

An interactive web application that allows users to search for specific property information using addresses or Property Identification Numbers (PINs) with rich geographic and administrative data.

## Project Overview

This application combines a Next.js frontend with a Django REST API backend to provide comprehensive property information for Chicago area properties. Users can search by address, PIN, or click on map locations to view detailed property data including tax information, school districts, flood zones, and more.

## Features

- **Interactive Map**: Mapbox-powered map with property visualization
- **Address Search**: Search properties by address with autocomplete
- **PIN Lookup**: Search using Property Identification Numbers
- **Comprehensive Data**: Access to 100+ data fields per property including:
  - Tax information and districts
  - School districts (elementary, secondary, unified)
  - Census and demographic data
  - Environmental data (flood zones, noise contours)
  - Economic zones and TIF districts
  - Community areas and wards

## Files Overview

### Core Application Files
- `property_search_app/` - Main Next.js frontend application
- `property_api/` - Django backend API for data processing
- `data/common_county_data_complete.csv` - Primary property dataset (169 records)

### Data Structure
The CSV contains comprehensive property information with 100+ columns including:
- **Location**: PIN, coordinates (lat/lon), ZIP codes
- **Administrative**: Townships, wards, community areas
- **Schools**: Elementary, secondary, and unified districts
- **Tax Districts**: Municipality, library, park, fire protection
- **Environmental**: Flood zones, airport noise, enterprise zones
- **Census**: Block groups, tracts, congressional districts

### Legacy Components
- `Map-draft-master/` - Original map prototype (Mapbox implementation)
- `backend-master/` - Django backend template
- `frontend-master/` - Next.js frontend template

## Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Mapbox API key

### Installation
1. **Frontend Setup**:
   ```bash
   cd property_search_app
   npm install
   npm run dev
   ```

2. **Backend Setup**:
   ```bash
   cd property_api
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Environment Variables**:
   - Create `.env` with Mapbox token
   - Configure database settings

## Usage

1. **Search by Address**: Enter full or partial address in search bar
2. **Search by PIN**: Enter 14-digit Property Identification Number
3. **Map Interaction**: Click on map markers to view property details
4. **Filter & Sort**: Use sidebar filters for property types, tax codes, etc.

## Data Sources

- **Primary**: Cook County Property Data (2025)
- **License**: Public domain
- **Coverage**: Chicago metropolitan area
- **Updates**: Annual refresh

## Architecture

### Frontend (Next.js + TypeScript)
- Interactive map with Mapbox GL JS
- Property search and filtering
- Responsive design with Tailwind CSS
- Real-time data visualization

### Backend (Django REST Framework)
- RESTful API for property data
- CSV data processing and indexing
- Search optimization and caching
- User authentication (optional)

### Data Processing
- CSV parsing and validation
- Geospatial indexing for map performance
- Search algorithm optimization

## API Endpoints

- `GET /api/properties/` - List all properties
- `GET /api/properties/search/?q={query}` - Search by address/PIN
- `GET /api/properties/{pin}/` - Get specific property details
- `GET /api/properties/nearby/?lat={lat}&lon={lon}` - Find nearby properties

## File Naming Conventions

- **Scripts**: `process_property_data.py`, `import_csv_data.py`
- **Components**: `PropertySearch.tsx`, `InteractiveMap.tsx`
- **API Views**: `property_search_views.py`, `map_data_views.py`
- **Data Files**: `common_county_data_complete.csv`

## Development Workflow

1. **Feature Development**: Create branch from `main`
2. **Testing**: Run tests for both frontend and backend
3. **Code Review**: PR review process
4. **Deployment**: Automated deployment pipeline

## Contributing

1. Follow naming conventions outlined above
2. Add tests for new features
3. Update documentation
4. Ensure responsive design

## Technical Details

### Performance Optimization
- CSV data indexed in backend database
- Map markers clustered for performance
- Lazy loading for property details
- Caching for frequently accessed data

### Security Considerations
- API rate limiting
- Input validation and sanitization
- Optional user authentication
- CORS configuration

## Results Summary

The application provides instant access to comprehensive property information for Chicago area properties, combining geographic visualization with detailed administrative and environmental data. Users can efficiently search, explore, and analyze property data through an intuitive interface.

---

*Built with Next.js, Django, Mapbox, and comprehensive Chicago property data* 