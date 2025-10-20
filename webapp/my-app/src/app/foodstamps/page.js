// This directive tells Next.js that this is a client-side component.
"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Map, Marker, Overlay } from "pigeon-maps";
import './globals.css';

// --- Placeholder Resource Data with Coordinates ---
// In a real app, this would be in a shared file.
const placeholderResources = {
  "30303": [
    { id: 4, category: "Food Assistance", name: "Fulton County SNAP Office", description: "SNAP applications and info.", address: "123 Main St, Atlanta, GA", phone: "404-555-1212", lat: 33.7537, lng: -84.3880 },
    { id: 5, category: "Utility Assistance", name: "Atlanta LIHEAP Program", description: "Energy bill assistance.", address: "456 Central Ave, Atlanta, GA", phone: "404-555-4545", lat: 33.7510, lng: -84.3900 },
    { id: 3, category: "Food Assistance", name: "Community Food Bank", description: "Offers weekly food pantry services.", address: "789 Pine St, Atlanta, GA", phone: "404-555-7878", lat: 33.7589, lng: -84.3838 }
  ],
  "10001": [
    { id: 6, category: "Food Assistance", name: "NYC SNAP Center - Midtown", description: "SNAP applications and info.", address: "111 W 34th St, New York, NY", phone: "212-555-1212", lat: 40.7498, lng: -73.9875 },
    { id: 7, category: "Utility Assistance", name: "NY HEAP Office", description: "Energy bill assistance.", address: "222 8th Ave, New York, NY", phone: "212-555-4545", lat: 40.7449, lng: -73.9982 }
  ]
};

// --- Map Component (Integrated for simplicity) ---
function ResourceMap({ locations }) {
  const [center, setCenter] = useState([37.0902, -95.7129]); // Default: Center of US
  const [zoom, setZoom] = useState(4);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    if (locations && locations.length > 0) {
      setCenter([locations[0].lat, locations[0].lng]);
      setZoom(14);
      setSelected(null);
    }
  }, [locations]);

  if (!locations || locations.length === 0) {
    return null;
  }

  return (
    <div className="mb-12 rounded-lg overflow-hidden shadow-lg" style={{ height: '400px', width: '100%' }}>
      <Map
        height={400} center={center} zoom={zoom}
        onBoundsChanged={({ center, zoom }) => { setCenter(center); setZoom(zoom); }}
      >
        {locations.map((loc) => (
          <Marker
            key={loc.id} width={40} anchor={[loc.lat, loc.lng]}
            color={'#db4437'} // Red marker for food/resources
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

// --- Main Food Stamps Page Component ---
export default function FoodStampsPage() {
  const [zipcode, setZipcode] = useState("");
  const [snapResults, setSnapResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = (e) => {
    e.preventDefault();
    setHasSearched(true);
    const allResources = placeholderResources[zipcode] || [];
    const foodResources = allResources.filter(res => res.category === "Food Assistance");
    setSnapResults(foodResources);
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-8 md:p-16 bg-gray-50">
      <div className="w-full max-w-5xl">
        
        <div className="mb-8">
            <Link href="/" className="text-indigo-600 hover:text-indigo-800 font-semibold">
                &larr; Back to Dashboard
            </Link>
        </div>

        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-3">Food Assistance (SNAP)</h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Find SNAP / food stamp programs and enrollment offices near you.
          </p>
        </header>

        <div className="bg-white p-6 rounded-lg shadow-md mb-12">
          <form onSubmit={handleSearch}>
            <label htmlFor="zipcode" className="block text-sm font-medium text-gray-700 mb-1">Enter your zipcode</label>
            <div className="flex gap-2">
              <input
                type="text" id="zipcode" value={zipcode}
                onChange={(e) => setZipcode(e.target.value)}
                placeholder="e.g., 30303"
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
              />
              <button type="submit" className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500">
                Search
              </button>
            </div>
          </form>
        </div>

        <ResourceMap locations={snapResults} />

        {hasSearched && snapResults.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-semibold mb-4">SNAP / Food Assistance near "{zipcode}"</h2>
            <div className="space-y-4">
              {snapResults.map((item) => (
                <div key={item.id} className="bg-white p-4 rounded-lg shadow border-l-4 border-green-500">
                  <h3 className="font-semibold text-lg text-gray-900">{item.name}</h3>
                  <p className="text-gray-600">{item.description}</p>
                  <p className="text-sm text-gray-500 mt-1">{item.address}</p>
                  <p className="text-sm text-gray-500">Phone: {item.phone}</p>
                  <a href={item.website} target="_blank" rel="noopener noreferrer" className="text-sm text-green-600 hover:text-green-800 font-medium">
                    Visit Website &rarr;
                  </a>
                </div>
              ))}
            </div>
          </div>
        )}

        {hasSearched && snapResults.length === 0 && (
          <p className="text-gray-500 text-center mt-4">No food assistance resources found for "{zipcode}".</p>
        )}
      </div>
    </main>
  );
}
