export interface Property {
  pin: string;
  address?: string; // Legacy field
  business?: string; // Legacy field
  year: number;
  property_class?: string; // Legacy field
  township_name: string;
  zip_code: string;
  latitude: number;
  longitude: number;
  community_area_name?: string; // Legacy field
  
  // Core fields for backward compatibility
  coordinates?: [number, number];
  pin10?: string;
  address_display?: string;
  class_code?: string;
  ward_num?: number;
  chicago_community_area_name?: string;
  
  // SSA 32 Property Information
  property_address?: string;
  property_city?: string;
  property_state?: string;
  square_footage_land?: number;
  
  // Assessment Information
  total_assessed_value?: string;
  land_assessed_value?: string;
  building_assessed_value?: string;
  
  // Property Status
  vacancy_type?: string;
  assessor_office_link?: string;
  
  // Taxpayer Information
  taxpayer_id?: string;
  mailing_name?: string;
  mailing_address?: string;
  mailing_city?: string;
  mailing_state?: string;
  mailing_zip?: string;
  
  // Location data
  x_3435?: number;
  y_3435?: number;
  
  // Administrative divisions
  triad_name?: string;
  triad_code?: number;
  township_code?: number;
  nbhd_code?: string;
  tax_code?: string;
  
  // School districts
  school_elementary_district_name?: string;
  school_secondary_district_name?: string;
  school_unified_district_name?: string;
  school_school_year?: string;
  school_data_year?: number;
  
  // Tax districts
  tax_municipality_name?: string;
  tax_school_elementary_district_name?: string;
  tax_school_secondary_district_name?: string;
  tax_community_college_district_name?: string;
  tax_fire_protection_district_name?: string;
  tax_library_district_name?: string;
  tax_park_district_name?: string;
  tax_tif_district_name?: string;
  tax_data_year?: number;
  
  // Environmental data
  env_flood_fema_sfha?: boolean;
  env_flood_fs_factor?: number;
  env_flood_fs_risk_direction?: string;
  env_ohare_noise_contour_no_buffer_bool?: boolean;
  env_ohare_noise_contour_half_mile_buffer_bool?: boolean;
  env_airport_noise_dnl?: number;
  
  // Economic zones
  econ_enterprise_zone_num?: string;
  econ_qualified_opportunity_zone_num?: string;
  
  // Accessibility scores
  access_cmap_walk_nta_score?: number;
  access_cmap_walk_total_score?: number;
  access_cmap_walk_data_year?: number;
  
  // Timestamps
  created_at?: string;
  updated_at?: string;
}

export interface PropertySearchResult {
  count: number;
  results: Property[];
  query: string;
  search_type: string;
}

export interface PropertyGeoJSON {
  type: "FeatureCollection";
  features: PropertyFeature[];
}

export interface PropertyFeature {
  type: "Feature";
  geometry: {
    type: "Point";
    coordinates: [number, number];
  };
  properties: {
    pin: string;
    community_area?: string;
    zip_code?: string;
    class_code?: string;
    ward?: number;
    popup_content: string;
  };
}

export interface PropertyStats {
  total_properties: number;
  community_areas: number;
  zip_codes: number;
  wards: number;
  property_classes: number;
  top_community_areas: Array<{
    chicago_community_area_name: string;
    count: number;
  }>;
}

export interface SearchSuggestion {
  pin: string;
  display: string;
  type?: "pin" | "address" | "business";
  subtitle?: string;
}

export interface NearbyPropertiesResult {
  count: number;
  center: [number, number];
  radius_km: number;
  results: Property[];
} 