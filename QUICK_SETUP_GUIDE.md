# Chicago Property Search - Quick Setup Guide

## 🚀 **Get Started in 5 Minutes**

This guide will help you set up and run the Chicago Property Search application.

### **Prerequisites**
- Node.js 18+ 
- Python 3.8+
- Mapbox account (free tier available)

---

## **Step 1: Setup Backend API**

### **1.1 Navigate to Backend Directory**
```bash
cd property_api
```

### **1.2 Install Python Dependencies**
```bash
pip install -r requirements.txt
```

### **1.3 Setup Database**
```bash
python manage.py migrate
```

### **1.4 Import Property Data**
```bash
python manage.py import_property_data --csv-path ../data/common_county_data_complete.csv --clear
```

### **1.5 Run Backend Server**
```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/v1/`

---

## **Step 2: Setup Frontend Application**

### **2.1 Navigate to Frontend Directory**
```bash
cd property_search_app
```

### **2.2 Install Dependencies**
```bash
npm install
```

### **2.3 Setup Environment Variables**
Create `.env.local` file:
```bash
# Copy the example file
cp env.example .env.local
```

Edit `.env.local` with your Mapbox token:
```env
NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN=your_mapbox_token_here
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_DEFAULT_MAP_CENTER_LAT=41.8781
NEXT_PUBLIC_DEFAULT_MAP_CENTER_LNG=-87.6298
NEXT_PUBLIC_DEFAULT_MAP_ZOOM=12
```

### **2.4 Run Frontend Development Server**
```bash
npm run dev
```

The application will be available at: `http://localhost:3000/`

---

## **Step 3: Get Your Mapbox Token**

1. **Sign up** at [mapbox.com](https://mapbox.com)
2. **Go to Account** → **Access Tokens**
3. **Copy your default token** or create a new one
4. **Add to your `.env.local`** file

---

## **🎯 Testing the Application**

### **Search Examples**
Try these searches to test functionality:

1. **PIN Search**: `20293180300000`
2. **Community Area**: `Auburn Gresham`
3. **ZIP Code**: `60620`

### **API Testing**
Test the backend API directly:
```bash
# Get all properties
curl http://localhost:8000/api/v1/properties/

# Search properties
curl "http://localhost:8000/api/v1/properties/search/?q=Auburn"

# Get property details
curl http://localhost:8000/api/v1/properties/20293180300000/
```

---

## **🔧 Troubleshooting**

### **Backend Issues**
- **Import fails**: Check CSV file path is correct
- **Database errors**: Try `python manage.py migrate --run-syncdb`
- **Port conflicts**: Change port with `python manage.py runserver 8001`

### **Frontend Issues**
- **Map not loading**: Verify Mapbox token in `.env.local`
- **API errors**: Ensure backend is running on port 8000
- **Dependencies**: Try `rm -rf node_modules package-lock.json && npm install`

### **Data Issues**
- **No search results**: Verify data import completed successfully
- **Check database**: `python manage.py shell` then `from core.property.models import Property; print(Property.objects.count())`

---

## **📊 Data Overview**

The application includes comprehensive Chicago property data:

- **169 properties** from Cook County
- **100+ data fields** per property including:
  - Location and coordinates
  - School districts
  - Tax information  
  - Environmental data
  - Economic zones
  - Census information

---

## **🔗 API Endpoints**

Key endpoints available:

- `GET /api/v1/properties/` - List properties
- `GET /api/v1/properties/search/?q={query}` - Search
- `GET /api/v1/properties/{pin}/` - Property details
- `GET /api/v1/properties/geojson/` - Map data
- `GET /api/v1/properties/nearby/?lat={lat}&lon={lon}` - Nearby properties

---

## **🚀 Production Deployment**

### **Frontend (Vercel/Netlify)**
```bash
npm run build
```

### **Backend (Railway/Heroku)**
- Update `ALLOWED_HOSTS` in settings
- Configure production database
- Set environment variables

---

**Need help?** Check the main README.md for detailed information. 