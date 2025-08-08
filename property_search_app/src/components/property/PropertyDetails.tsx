'use client';

import React from 'react';
import { X, MapPin, Building, Hash, Calendar, Home, Globe, DollarSign, Users, FileText } from 'lucide-react';
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
            <p className="text-base font-medium text-gray-800">{property.property_address || 'No address available'}</p>
            {property.property_city && property.property_state && (
              <p className="text-sm text-gray-600">{property.property_city}, {property.property_state} {property.zip_code ? Math.floor(Number(property.zip_code)) : ''}</p>
            )}
          </div>
        </div>
        <Button variant="ghost" size="sm" onClick={onClose}>
          <X className="w-4 h-4" />
        </Button>
      </div>

      {/* Content */}
      <div className="p-4 space-y-4 max-h-[70vh] overflow-y-auto">
        {/* Property Information */}
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
                <p className="text-sm font-mono">{property.pin}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Property Class</label>
                <Badge variant="outline">{property.class_code || 'N/A'}</Badge>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Tax Year</label>
                <p className="text-sm">{property.year || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Ward Number</label>
                <p className="text-sm">{property.ward_num || 'N/A'}</p>
              </div>
            </div>
            
            {property.square_footage_land && (
              <div>
                <label className="text-sm font-medium text-gray-500">Land Square Footage</label>
                <p className="text-sm">{Number(property.square_footage_land).toLocaleString()} sq ft</p>
              </div>
            )}
            
            {property.vacancy_type && (
              <div>
                <label className="text-sm font-medium text-gray-500">Vacancy Status</label>
                <Badge 
                  variant={
                    property.vacancy_type === 'NO STATUS' ? 'default' : 
                    property.vacancy_type === 'VACANT LAND' ? 'destructive' : 
                    'secondary'
                  }
                >
                  {property.vacancy_type}
                </Badge>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Assessment Information */}
        {(property.total_assessed_value || property.land_assessed_value || property.building_assessed_value) && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <DollarSign className="w-4 h-4" />
                <span>Assessment Values</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {property.total_assessed_value && (
                <div>
                  <label className="text-sm font-medium text-gray-500">Total Assessed Value</label>
                  <p className="text-lg font-semibold text-green-600">${Number(property.total_assessed_value).toLocaleString()}</p>
                </div>
              )}
              
              {(property.land_assessed_value || property.building_assessed_value) && (
                <div className="grid grid-cols-2 gap-4">
                  {property.land_assessed_value && (
                    <div>
                      <label className="text-sm font-medium text-gray-500">Land Value</label>
                      <p className="text-sm">${Number(property.land_assessed_value).toLocaleString()}</p>
                    </div>
                  )}
                  {property.building_assessed_value && (
                    <div>
                      <label className="text-sm font-medium text-gray-500">Building Value</label>
                      <p className="text-sm">${Number(property.building_assessed_value).toLocaleString()}</p>
                    </div>
                  )}
                </div>
              )}
              
              {property.tax_code && (
                <div>
                  <label className="text-sm font-medium text-gray-500">Tax District Code</label>
                  <p className="text-sm font-mono">{property.tax_code}</p>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Owner/Taxpayer Information */}
        {(property.mailing_name || property.taxpayer_id || property.mailing_address) && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Users className="w-4 h-4" />
                <span>Owner/Taxpayer Information</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 gap-4">
                {property.mailing_name && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Owner/Taxpayer Name</label>
                    <p className="text-sm font-medium">{property.mailing_name}</p>
                  </div>
                )}
                
                {property.taxpayer_id && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Taxpayer ID</label>
                    <p className="text-sm font-mono">{property.taxpayer_id}</p>
                  </div>
                )}
              </div>
              
              {property.mailing_address && (
                <div>
                  <label className="text-sm font-medium text-gray-500">Mailing Address</label>
                  <div className="text-sm bg-gray-50 p-3 rounded border">
                    <p className="font-medium">{property.mailing_address}</p>
                    {property.mailing_city && property.mailing_state && (
                      <p className="text-gray-600">{property.mailing_city}, {property.mailing_state} {property.mailing_zip ? Math.floor(Number(property.mailing_zip)) : ''}</p>
                    )}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        )}

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
                <label className="text-sm font-medium text-gray-500">Latitude</label>
                <p className="text-sm font-mono">
                  {property.coordinates && property.coordinates.length >= 2 
                    ? property.coordinates[1].toFixed(6) 
                    : property.latitude?.toFixed(6) || 'N/A'}
                </p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Longitude</label>
                <p className="text-sm font-mono">
                  {property.coordinates && property.coordinates.length >= 2 
                    ? property.coordinates[0].toFixed(6) 
                    : property.longitude?.toFixed(6) || 'N/A'}
                </p>
              </div>
            </div>
            
            {/* Google Maps Button */}
            {property.property_address && (
              <div className="mt-3">
                <button
                  onClick={() => {
                    const addressParts = [
                      property.property_address,
                      property.property_city,
                      property.property_state,
                      property.zip_code ? Math.floor(Number(property.zip_code)).toString() : null
                    ].filter(part => part && part.trim());
                    
                    const fullAddress = addressParts.join(', ');
                    const encodedAddress = encodeURIComponent(fullAddress);
                    const url = `https://www.google.com/maps/search/${encodedAddress}`;
                    window.open(url, '_blank');
                  }}
                  className="inline-flex items-center space-x-2 px-3 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors"
                >
                  <MapPin className="w-4 h-4" />
                  <span>View on Google Maps</span>
                </button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Official Records */}
        {property.assessor_office_link && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <FileText className="w-4 h-4" />
                <span>Official Records</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <label className="text-sm font-medium text-gray-500">Cook County Assessor</label>
                <a 
                  href={property.assessor_office_link} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="mt-2 inline-flex items-center space-x-2 px-4 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 transition-colors"
                >
                  <Globe className="w-4 h-4" />
                  <span>View Official Assessor Record</span>
                </a>
              </div>
              
              <div className="text-xs text-gray-500 bg-blue-50 p-2 rounded">
                <p><strong>Note:</strong> This link takes you to the official Cook County Assessor's office page for this property, where you can find additional details, appeals history, and official documentation.</p>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};