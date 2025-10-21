// This directive tells Next.js that this is a client-side component.
"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Map, Marker, Overlay } from "pigeon-maps";
import '../globals.css';

// --- Placeholder Housing Data with Coordinates ---
// This contains only the housing data needed for this page.
const placeholderHousingData = {
  "30303": [
    { id: 1, type: 'housing', name: "Downtown Affordable Housing", address: "123 Peachtree St, Atlanta, GA 30303", phone: "404-555-1000", lat: 33.7563, lng: -84.3877 },
    { id: 2, type: 'housing', name: "Community Housing Partners", address: "456 Auburn Ave, Atlanta, GA 30303", phone: "404-555-2000", lat: 33.7548, lng: -84.3833 },
  ],
  "10001": [
    { id: 3, type: 'housing', name: "Midtown Low-Income Apartments", address: "789 8th Ave, New York, NY 10001", phone: "212-555-3000", lat: 40.7563, lng: -73.9904 },
  ]
};

// --- Map Component (Integrated for simplicity) ---
function HousingMap({ locations }) {
  const [center, setCenter] = useState([37.0902, -95.7129]); // Default: Center of US
  const [zoom, setZoom] = useState(4);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    // When new locations are found, center the map on the first result
    if (locations && locations.length > 0) {
      setCenter([locations[0].lat, locations[0].lng]);
      setZoom(14);
      setSelected(null); // Clear any previously selected marker
    }
  }, [locations]);

  // Don't render the map component if there are no locations to show
  if (!locations || locations.length === 0) {
    return null;
  }

  return (
    <div className="mb-12 rounded-lg overflow-hidden shadow-lg" style={{ height: '400px', width: '100%' }}>
      <Map
        height={400}
        center={center}
        zoom={zoom}
        onBoundsChanged={({ center, zoom }) => {
          setCenter(center);
          setZoom(zoom);
        }}
      >
        {locations.map((loc) => (
          <Marker
            key={loc.id}
            width={40}
            anchor={[loc.lat, loc.lng]}
            color={'#1a73e8'} // Blue marker for housing
            onClick={() => setSelected(loc)}
          />
        ))}

        {selected && (
          <Overlay anchor={[selected.lat, selected.lng]} offset={[120, 70]}>
            <div className="bg-white p-3 rounded-lg shadow-xl border" style={{ minWidth: '200px' }}>
              <h4 className="font-bold text-md text-gray-900">{selected.name}</h4>
              <p className="text-sm text-gray-600">{selected.address}</p>
              <p className="text-sm text-gray-500">{selected.phone}</p>
              <button onClick={() => setSelected(null)} className="text-xs font-bold text-red-600 mt-1">
                Close
              </button>
            </div>
          </Overlay>
        )}
      </Map>
    </div>
  );
}

// --- Main Housing Page Component ---
export default function HousingPage() {
  const [zipcode, setZipcode] = useState("");
  const [housingResults, setHousingResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false); // Track if a search has been made

  // Handle the form submission
  const handleSearch = (e) => {
    e.preventDefault();
    setHasSearched(true); // Mark that a search was performed
    const data = placeholderHousingData[zipcode] || [];
    setHousingResults(data);
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-8 md:p-16 bg-gray-50">
      <div className="w-full max-w-5xl">
        
        {/* Navigation Link to go back home */}
        <div className="mb-8">
            <Link href="/" className="text-indigo-600 hover:text-indigo-800 font-semibold">
                &larr; Back to Dashboard
            </Link>
        </div>

        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-3">
            Housing Assistance
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Find low-cost housing, rent support, and shelter information near you.
          </p>
        </header>

        {/* Zipcode Form */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-12">
          <form onSubmit={handleSearch}>
            <label htmlFor="zipcode" className="block text-sm font-medium text-gray-700 mb-1">
              Enter your zipcode
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                name="zipcode"
                id="zipcode"
                value={zipcode}
                onChange={(e) => setZipcode(e.target.value)}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                placeholder="e.g., 30303"
              />
              <button
                type="submit"
                className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Search
              </button>
            </div>
          </form>
        </div>

        {/* Map Display */}
        <HousingMap locations={housingResults} />

        {/* Housing Results List */}
        {hasSearched && housingResults.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-semibold mb-4">
              Low-Cost Housing near "{zipcode}"
            </h2>
            <div className="space-y-4">
              {housingResults.map((item) => (
                <div key={item.id} className="bg-white p-4 rounded-lg shadow">
                  <h3 className="font-semibold text-lg text-gray-900">{item.name}</h3>
                  <p className="text-gray-600">{item.address}</p>
                  <p className="text-sm text-gray-500 mt-1">Phone: {item.phone}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* No Results Message */}
        {hasSearched && housingResults.length === 0 && (
          <p className="text-gray-500 text-center mt-4">No housing resources found for "{zipcode}".</p>
        )}
      </div>
    </main>
  );
}
