import axios from 'axios';
import { 
  Property, 
  PropertySearchResult, 
  PropertyGeoJSON, 
  PropertyStats,
  SearchSuggestion,
  NearbyPropertiesResult 
} from '@/types/property';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Property API functions
export const propertyApi = {
  // Get all properties with pagination and filtering
  getProperties: async (params?: {
    page?: number;
    page_size?: number;
    property_class?: string;
    zip_code?: string;
    township_name?: string;
    community_area_name?: string;
    search?: string;
    ordering?: string;
  }) => {
    const response = await api.get('/properties/', { params });
    return response.data;
  },

  // Get property details by PIN
  getPropertyDetail: async (pin: string): Promise<Property> => {
    const response = await api.get(`/properties/${pin}/`);
    return response.data;
  },

  // Search properties
  searchProperties: async (
    query: string, 
    searchType: 'all' | 'pin' | 'address' | 'business' = 'all',
    limit: number = 50
  ): Promise<{ results: Property[] }> => {
    const response = await api.get('/properties/search/', {
      params: { q: query, type: searchType, limit }
    });
    return { results: response.data || [] };
  },

  // Get autocomplete suggestions
  getAutocompleteSuggestions: async (query: string, limit: number = 10): Promise<SearchSuggestion[]> => {
    if (query.length < 2) return [];
    const response = await api.get('/properties/autocomplete/', {
      params: { q: query, limit }
    });
    return response.data || [];
  },

  // Get nearby properties
  getNearbyProperties: async (
    lat: number, 
    lon: number, 
    radius: number = 1.0,
    limit: number = 25
  ): Promise<NearbyPropertiesResult> => {
    const response = await api.get('/properties/nearby/', {
      params: { lat, lon, radius, limit }
    });
    return response.data;
  },

  // Get properties as GeoJSON for map visualization
  getPropertiesGeoJSON: async (params?: {
    north?: number;
    south?: number;
    east?: number;
    west?: number;
    area?: string;
    class?: string;
    limit?: number;
  }): Promise<PropertyGeoJSON> => {
    const response = await api.get('/properties/geojson/', { params });
    return response.data;
  },

  // Get property school information
  getPropertySchools: async (pin: string) => {
    const response = await api.get(`/properties/${pin}/schools/`);
    return response.data;
  },

  // Get property tax information
  getPropertyTax: async (pin: string) => {
    const response = await api.get(`/properties/${pin}/tax/`);
    return response.data;
  },

  // Get property environmental information
  getPropertyEnvironmental: async (pin: string) => {
    const response = await api.get(`/properties/${pin}/environment/`);
    return response.data;
  },

  // Get database statistics
  getStats: async (): Promise<PropertyStats> => {
    const response = await api.get('/properties/stats/');
    return response.data;
  }
};

// Error handling wrapper
export const withErrorHandling = async <T>(
  apiCall: () => Promise<T>
): Promise<{ data?: T; error?: string }> => {
  try {
    const data = await apiCall();
    return { data };
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as any;
      return { 
        error: axiosError.response?.data?.message || axiosError.message || 'An error occurred' 
      };
    }
    return { error: String(error) || 'An unexpected error occurred' };
  }
};

export default api; 