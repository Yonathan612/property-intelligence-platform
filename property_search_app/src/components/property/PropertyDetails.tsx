'use client';

import React from 'react';
import { X, MapPin, Building, Hash, Calendar, Home, Globe } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Property } from '@/types/property';

interface PropertyDetailsProps {
  property: Property;
  onClose: () => void;
  className?: string;
}

export const PropertyDetails: React.FC<PropertyDetailsProps> = ({
  property,
  onClose,
  className = ""
}) => {
  return (
    <div className={`bg-white border border-gray-200 rounded-lg shadow-sm ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <Hash className="w-5 h-5 text-blue-600" />
          <div>
            <h2 className="text-lg font-semibold">{property.pin}</h2>
            <p className="text-sm text-gray-600">{property.address}</p>
          </div>
        </div>
        <Button variant="ghost" size="sm" onClick={onClose}>
          <X className="w-4 h-4" />
        </Button>
      </div>

      {/* Content */}
      <div className="p-4 space-y-4">
        {/* Basic Information */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Building className="w-4 h-4" />
              <span>Property Information</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">PIN</label>
                <p className="text-sm">{property.pin}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Address</label>
                <p className="text-sm">{property.address}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Business</label>
                <p className="text-sm">{property.business || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Property Class</label>
                <Badge variant="outline">{property.property_class || 'N/A'}</Badge>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Year</label>
                <p className="text-sm">{property.year || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">ZIP Code</label>
                <p className="text-sm">{property.zip_code || 'N/A'}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Location Information */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <MapPin className="w-4 h-4" />
              <span>Location</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Community Area</label>
                <p className="text-sm">{property.community_area_name || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Township</label>
                <p className="text-sm">{property.township_name || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Latitude</label>
                <p className="text-sm font-mono">{property.latitude ? property.latitude.toFixed(6) : 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Longitude</label>
                <p className="text-sm font-mono">{property.longitude ? property.longitude.toFixed(6) : 'N/A'}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Additional Information */}
        {(property.school_elementary_district_name || property.school_secondary_district_name || 
          property.tax_municipality_name || property.tax_library_district_name) && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Globe className="w-4 h-4" />
                <span>District Information</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="grid grid-cols-1 gap-3">
                {property.school_elementary_district_name && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Elementary School District</label>
                    <p className="text-sm">{property.school_elementary_district_name}</p>
                  </div>
                )}
                {property.school_secondary_district_name && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Secondary School District</label>
                    <p className="text-sm">{property.school_secondary_district_name}</p>
                  </div>
                )}
                {property.tax_municipality_name && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Municipality</label>
                    <p className="text-sm">{property.tax_municipality_name}</p>
                  </div>
                )}
                {property.tax_library_district_name && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Library District</label>
                    <p className="text-sm">{property.tax_library_district_name}</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Map View Button */}
        <div className="pt-4 border-t border-gray-200">
          <div className="flex space-x-3">
            <Button 
              variant="outline"
              className="flex-1" 
              onClick={onClose}
            >
              ← Back to Search
            </Button>
            <Button 
              className="flex-1" 
              onClick={() => {
                // Open map view with property address
                if (property.address) {
                  // Use the address for a more user-friendly map view
                  const addressQuery = encodeURIComponent(property.address);
                  window.open(
                    `https://www.google.com/maps/search/${addressQuery}`,
                    '_blank'
                  );
                } else if (property.latitude && property.longitude) {
                  // Fallback to coordinates if no address
                  window.open(
                    `https://www.google.com/maps?q=${property.latitude},${property.longitude}`,
                    '_blank'
                  );
                }
              }}
              disabled={!property.address && !property.latitude && !property.longitude}
            >
              <MapPin className="w-4 h-4 mr-2" />
              View on Map
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}; 