# Auburn Gresham Property Search

A full-stack property search application focused on the 79th Street corridor in Auburn Gresham, Chicago. This system provides comprehensive property information with intuitive search capabilities and modern UI design.

## 🌟 Features

- **Smart Search**: Real-time search by PIN, address, or business name
- **Autocomplete**: Instant suggestions as you type
- **Property Details**: Comprehensive property information including coordinates, business details, and classification
- **Google Maps Integration**: Direct links to property locations
- **Responsive Design**: Modern, clean interface optimized for all devices
- **Fast API**: Django REST Framework backend with efficient data retrieval

## 🏢 Data Coverage

- **100+ properties** along the 79th Street corridor
- Real property data including PINs, addresses, business names
- Location data with precise coordinates
- Property classifications and community area information
- Auburn Gresham neighborhood focus

## 🚀 Technology Stack

### Backend
- **Django** - Python web framework
- **Django REST Framework** - API development
- **SQLite** - Database (with data loaded from CSV)
- **Python 3.8+** - Programming language

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Modern icon library
- **Radix UI** - Accessible component primitives

## 📁 Project Structure

```
auburn-gresham-property-search/
├── simple_property_api/          # Django backend
│   ├── properties/               # Property app
│   │   ├── models.py            # Property model
│   │   ├── serializers.py       # API serializers
│   │   ├── views.py             # API views
│   │   └── urls.py              # URL routing
│   ├── property_api/            # Django settings
│   ├── load_data.py             # Data import script
│   └── db.sqlite3               # SQLite database
├── property_search_app/          # Next.js frontend
│   ├── src/
│   │   ├── app/                 # App router pages
│   │   ├── components/          # React components
│   │   ├── lib/                 # Utilities & API
│   │   └── types/               # TypeScript types
│   ├── package.json             # Dependencies
│   └── tailwind.config.ts       # Tailwind configuration
├── data/                        # CSV data files
│   └── 79thProperties.csv       # Property data (100+ records)
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
# Navigate to backend directory
cd simple_property_api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django djangorestframework django-cors-headers

# Run migrations
python3 manage.py migrate

# Load property data
python3 load_data.py

# Start development server
python3 manage.py runserver
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd property_search_app

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🔧 API Endpoints

**Base URL**: `http://localhost:8000/api/v1/`

- `GET /properties/` - List all properties (paginated)
- `GET /properties/{pin}/` - Get property details by PIN
- `GET /properties/search/?q={query}&type={type}` - Search properties
  - `type`: `all`, `pin`, `address`, `business`
- `GET /properties/autocomplete/?q={query}` - Get search suggestions

### Example API Usage
```bash
# Search by address
curl "http://localhost:8000/api/v1/properties/search/?q=1201%20W%2079TH%20ST&type=address"

# Get autocomplete suggestions
curl "http://localhost:8000/api/v1/properties/autocomplete/?q=1201"

# Get property by PIN
curl "http://localhost:8000/api/v1/properties/17-16-401-001-0000/"
```

## 🎯 Usage

1. Start the backend server (Django on port 8000)
2. Start the frontend server (Next.js on port 3000)
3. Navigate to `http://localhost:3000/property-search`
4. Search for properties using:
   - Property PIN numbers
   - Street addresses
   - Business names
5. View detailed property information
6. Click "View on Map" to see location in Google Maps

## 📊 Database Schema

### Property Model
- `pin` (CharField) - Primary key, 14-digit property identifier
- `address` (CharField) - Street address
- `business` (CharField) - Business name (if applicable)
- `year` (IntegerField) - Property year
- `property_class` (CharField) - Property classification code
- `township_name` (CharField) - Township name
- `zip_code` (CharField) - ZIP code
- `latitude` (FloatField) - Latitude coordinate
- `longitude` (FloatField) - Longitude coordinate
- `community_area_name` (CharField) - Chicago community area

## 🎨 UI Features

- Clean, modern design with Tailwind CSS
- Real-time search with loading states
- Autocomplete dropdown with address suggestions
- Property details modal with comprehensive information
- Responsive layout for desktop and mobile
- Smooth animations and transitions
- Google Maps integration for location viewing

## 🔧 Development Features

- **TypeScript** for type safety
- **REST API** with Django REST Framework
- **Component-based architecture** with React
- **Tailwind CSS** for rapid styling
- **Git version control** with comprehensive history
- **Modular code structure** for maintainability

## 📈 Performance

- Fast search with efficient Django ORM queries
- Pagination for large result sets
- Optimized frontend with Next.js
- Lazy loading for improved performance
- Minimal API calls with smart caching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Property data sourced from Chicago property records
- Auburn Gresham community for inspiration
- Django and Next.js communities for excellent frameworks
- 79th Street corridor business community
