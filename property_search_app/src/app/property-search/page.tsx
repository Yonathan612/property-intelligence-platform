'use client';

import React, { useState } from 'react';
import { Property } from '@/types/property';
import { PropertySearch } from '@/components/property/PropertySearch';
import { PropertyDetails } from '@/components/property/PropertyDetails';

export default function PropertySearchPage() {
  const [selectedProperty, setSelectedProperty] = useState<Property | null>(null);
  const [searchResults, setSearchResults] = useState<Property[]>([]);
  const [hasSearched, setHasSearched] = useState(false);

  const handlePropertySelect = (property: Property) => {
    setSelectedProperty(property);
  };

  const handleSearchResults = (results: Property[]) => {
    setSearchResults(results);
    setHasSearched(true);
  };

  const goBackToResults = () => {
    setSelectedProperty(null);
    // Keep the search results visible
  };

  const clearSearch = () => {
    setSelectedProperty(null);
    setSearchResults([]);
    setHasSearched(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">
                SSA 32 Property Search
              </h1>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        
        {/* Property Details Section */}
        {selectedProperty ? (
          <div className="max-w-4xl mx-auto">
            <PropertyDetails
              property={selectedProperty}
              onClose={goBackToResults}
            />
          </div>
        ) : (
          /* Search Section */
          <div className="max-w-4xl mx-auto">
            <PropertySearch
              onPropertySelect={handlePropertySelect}
              onSearchResults={handleSearchResults}
              onClearSearch={clearSearch}
              initialResults={searchResults}
              initialHasSearched={hasSearched}
              className="w-full"
            />
          </div>
        )}
        
      </div>
    </div>
  );
} 