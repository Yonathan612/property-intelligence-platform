'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Search, X, MapPin, Building, Hash } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { propertyApi } from '@/lib/api';
import { SearchSuggestion, Property } from '@/types/property';
import { LoadingSpinner } from '@/components/ui/loading-spinner';

interface PropertySearchProps {
  onPropertySelect?: (property: Property) => void;
  onSearchResults?: (results: Property[]) => void;
  onClearSearch?: () => void;
  initialResults?: Property[];
  initialHasSearched?: boolean;
  placeholder?: string;
  className?: string;
}

export const PropertySearch: React.FC<PropertySearchProps> = ({
  onPropertySelect,
  onSearchResults,
  onClearSearch,
  initialResults = [],
  initialHasSearched = false,
  placeholder = "Search by PIN, address, or business name...",
  className = ""
}) => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [loading, setLoading] = useState(false);
  const [searchResults, setSearchResults] = useState<Property[]>(initialResults);
  const [hasSearched, setHasSearched] = useState(initialHasSearched);
  const inputRef = useRef<HTMLInputElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  // Update local state when initial props change
  React.useEffect(() => {
    setSearchResults(initialResults);
    setHasSearched(initialHasSearched);
  }, [initialResults, initialHasSearched]);

  // Get autocomplete suggestions
  useEffect(() => {
    const getSuggestions = async () => {
      if (query.length < 2) {
        setSuggestions([]);
        return;
      }

      // Don't show suggestions if we already have search results
      if (hasSearched && searchResults.length > 0) {
        return;
      }

      try {
        const results = await propertyApi.getAutocompleteSuggestions(query);
        setSuggestions(Array.isArray(results) ? results : []);
        setShowSuggestions(true);
      } catch (error) {
        console.error('Failed to get suggestions:', error);
        setSuggestions([]);
      }
    };

    const timeoutId = setTimeout(getSuggestions, 300);
    return () => clearTimeout(timeoutId);
  }, [query, hasSearched, searchResults.length]);

  // Handle search submission
  const handleSearch = async (searchQuery: string = query) => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    setShowSuggestions(false);
    setHasSearched(true);
    
    try {
      const result = await propertyApi.searchProperties(searchQuery);
      setSearchResults(result.results);
      
      if (onSearchResults) {
        onSearchResults(result.results);
      }
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResults([]);
      
      if (onSearchResults) {
        onSearchResults([]);
      }
    } finally {
      setLoading(false);
    }
  };

  // Handle suggestion selection
  const handleSuggestionSelect = (suggestion: SearchSuggestion) => {
    // Extract just the address from the display format "address - business"
    const address = suggestion.display.includes(' - ') 
      ? suggestion.display.split(' - ')[0] 
      : suggestion.display;
    setQuery(address);
    setShowSuggestions(false);
    handleSearch(address);
  };

  // Handle property selection from results
  const handlePropertySelect = (property: Property) => {
    if (onPropertySelect) {
      onPropertySelect(property);
    }
  };

  // Clear search
  const clearSearch = () => {
    setQuery('');
    setSearchResults([]);
    setSuggestions([]);
    setShowSuggestions(false);
    setHasSearched(false);
    if (onClearSearch) {
      onClearSearch();
    }
  };

  // Handle input change
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    
    // If user is typing and we have search results, hide them to show suggestions
    if (value !== query && hasSearched) {
      setHasSearched(false);
      setSearchResults([]);
    }
  };

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        suggestionsRef.current &&
        !suggestionsRef.current.contains(event.target as Node) &&
        !inputRef.current?.contains(event.target as Node)
      ) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Get icon for suggestion type
  const getSuggestionIcon = (type: string) => {
    switch (type) {
      case 'pin':
        return <Hash className="w-4 h-4" />;
      case 'business':
        return <Building className="w-4 h-4" />;
      case 'address':
        return <MapPin className="w-4 h-4" />;
      default:
        return <Building className="w-4 h-4" />;
    }
  };

  // Get display text for suggestion (just the address)
  const getSuggestionDisplayText = (suggestion: SearchSuggestion) => {
    // Extract just the address from the display format "address - business"
    return suggestion.display.includes(' - ') 
      ? suggestion.display.split(' - ')[0] 
      : suggestion.display;
  };

  // Get business name from suggestion for subtitle
  const getSuggestionSubtitle = (suggestion: SearchSuggestion) => {
    if (suggestion.display.includes(' - ')) {
      return suggestion.display.split(' - ')[1];
    }
    return 'Property';
  };

  return (
    <div className={`relative ${className}`}>
      {/* Search Input */}
      <div className="relative">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <Input
            ref={inputRef}
            type="text"
            value={query}
            onChange={handleInputChange}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handleSearch();
              }
            }}
            placeholder={placeholder}
            className="pl-10 pr-20"
          />
          <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex items-center space-x-1">
            {loading && <LoadingSpinner size="sm" />}
            {query && (
              <Button
                variant="ghost"
                size="sm"
                onClick={clearSearch}
                className="h-6 w-6 p-0"
              >
                <X className="w-4 h-4" />
              </Button>
            )}
            <Button
              onClick={() => handleSearch()}
              disabled={loading || !query.trim()}
              size="sm"
            >
              Search
            </Button>
          </div>
        </div>
      </div>

      {/* Autocomplete Suggestions - Only show when NOT showing search results */}
      {showSuggestions && !hasSearched && suggestions && suggestions.length > 0 && (
        <div
          ref={suggestionsRef}
          className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-60 overflow-y-auto"
        >
          {suggestions.map((suggestion, index) => (
            <div
              key={index}
              onClick={() => handleSuggestionSelect(suggestion)}
              className="flex items-center px-3 py-2 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
            >
              <div className="text-gray-400 mr-3">
                {getSuggestionIcon(suggestion.type || 'address')}
              </div>
              <div className="flex-1">
                <div className="text-sm font-medium">{getSuggestionDisplayText(suggestion)}</div>
                <div className="text-xs text-gray-500">
                  {getSuggestionSubtitle(suggestion)}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Search Results - Only show after search is performed */}
      {hasSearched && (
        <div className="mt-4 bg-white border border-gray-200 rounded-lg shadow-sm">
          <div className="p-3 border-b border-gray-200">
            <h3 className="font-semibold text-sm">
              {searchResults.length > 0 
                ? `Search Results (${searchResults.length})`
                : 'No Results Found'
              }
            </h3>
          </div>
          <div className="max-h-96 overflow-y-auto">
            {searchResults.length > 0 ? (
              searchResults.map((property) => (
                <div
                  key={property.pin}
                  onClick={() => handlePropertySelect(property)}
                  className="flex items-center justify-between p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
                >
                  <div className="flex-1">
                    <div className="font-medium text-sm">PIN: {property.pin}</div>
                    <div className="text-sm text-gray-600">
                      {property.address}
                    </div>
                    <div className="text-xs text-gray-500">
                      {property.business && `Business: ${property.business}`}
                      {property.property_class && ` • Class: ${property.property_class}`}
                      {property.community_area_name && ` • ${property.community_area_name}`}
                    </div>
                  </div>
                  <Button variant="ghost" size="sm">
                    View Details
                  </Button>
                </div>
              ))
            ) : (
              <div className="p-6 text-center text-gray-500">
                <p>No properties found matching your search.</p>
                <p className="text-sm mt-1">Try searching by PIN, address, or business name.</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}; 