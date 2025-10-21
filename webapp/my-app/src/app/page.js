// This directive tells Next.js that this is a client-side component.
"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Map, Marker, Overlay } from "pigeon-maps";
import './globals.css';

// --- All Data is now in this file for simplicity ---

// Placeholder Housing Data with Coordinates
const placeholderHousingData = {
  "30303": [
    { id: 1, type: 'housing', name: "Downtown Affordable Housing", address: "123 Peachtree St, Atlanta, GA 30303", phone: "404-555-1000", lat: 33.7563, lng: -84.3877 },
    { id: 2, type: 'housing', name: "Community Housing Partners", address: "456 Auburn Ave, Atlanta, GA 30303", phone: "404-555-2000", lat: 33.7548, lng: -84.3833 },
  ],
  "10001": [
    { id: 3, type: 'housing', name: "Midtown Low-Income Apartments", address: "789 8th Ave, New York, NY 10001", phone: "212-555-3000", lat: 40.7563, lng: -73.9904 },
  ]
};

// Placeholder Resource Data with Coordinates
const placeholderResources = {
  "30303": [
    { id: 4, category: "Food Assistance", name: "Fulton County SNAP Office", description: "SNAP applications and info.", address: "123 Main St, Atlanta, GA", phone: "404-555-1212", lat: 33.7537, lng: -84.3880 },
    { id: 5, category: "Utility Assistance", name: "Atlanta LIHEAP Program", description: "Energy bill assistance.", address: "456 Central Ave, Atlanta, GA", phone: "404-555-4545", lat: 33.7510, lng: -84.3900 }
  ],
  "10001": [
    { id: 6, category: "Food Assistance", name: "NYC SNAP Center - Midtown", description: "SNAP applications and info.", address: "111 W 34th St, New York, NY", phone: "212-555-1212", lat: 40.7498, lng: -73.9875 }
  ]
};

// --- Map Component (Integrated into this file) ---
function PigeonMapComponent({ locations }) {
  const [center, setCenter] = useState([37.0902, -95.7129]); // Default to center of US
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
    <div className="mb-12 rounded-lg overflow-hidden shadow-lg border border-stone-200" style={{ height: '400px', width: '100%' }}>
      <Map
        height={400} center={center} zoom={zoom}
        onBoundsChanged={({ center, zoom }) => { setCenter(center); setZoom(zoom); }}
      >
        {locations.map((loc) => (
          <Marker
            key={loc.id} width={40} anchor={[loc.lat, loc.lng]}
            color={loc.type === 'housing' ? '#008080' : '#c53030'} // Teal for housing, Red for resources
            onClick={() => setSelected(loc)}
          />
        ))}

        {selected && (
          <Overlay anchor={[selected.lat, selected.lng]} offset={[120, 70]}>
            <div className="bg-white p-3 rounded-lg shadow-xl border" style={{ minWidth: '200px' }}>
              <h4 className="font-bold text-md text-stone-800">{selected.name}</h4>
              <p className="text-sm text-stone-600">{selected.address}</p>
              <p className="text-sm text-stone-500">{selected.phone}</p>
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


// --- Main Page Component ---
export default function HomePage() {
  const [zipcode, setZipcode] = useState("");
  const [housingResults, setHousingResults] = useState([]);
  const [resourceResults, setResourceResults] = useState([]);

  const handleSearch = (e) => {
    e.preventDefault();
    const housingData = placeholderHousingData[zipcode] || [];
    setHousingResults(housingData);

    const otherResources = placeholderResources[zipcode] || [];
    setResourceResults(otherResources);
  };
  
  const allLocations = [...housingResults, ...resourceResults];

  return (
    <main className="flex min-h-screen flex-col items-center p-8 md:p-16 bg-stone-50 text-stone-800">
      <div className="w-full max-w-5xl">
        
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-stone-900 mb-3 tracking-tight">Excess</h1>
          <p className="text-lg text-stone-600 max-w-3xl mx-auto">
            Connecting underserved communities with unclaimed resources. Find housing, food, and energy support.
          </p>
        </header>

        <div className="bg-white p-6 rounded-lg shadow-md mb-12 border border-stone-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
            <form onSubmit={handleSearch} className="md:col-span-2">
              <label htmlFor="zipcode" className="block text-sm font-medium text-stone-700 mb-1">
                Find resources near you
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  name="zipcode"
                  id="zipcode"
                  value={zipcode}
                  onChange={(e) => setZipcode(e.target.value)}
                  className="block w-full rounded-md border-stone-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 sm:text-sm p-2 border"
                  placeholder="Enter your zipcode (e.g., 30303)"
                />
                <button
                  type="submit"
                  className="rounded-md bg-teal-600 px-5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-teal-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-600"
                >
                  Search
                </button>
              </div>
            </form>
            <div className="text-center md:border-l md:border-stone-200 md:pl-6">
              <p className="text-sm font-medium text-stone-700 mb-1">Need help by phone?</p>
              <a href="tel: (205)-293-8808" className="text-lg font-semibold text-teal-600 hover:text-teal-700">
                Call (205)-293-8808
              </a>
              <p className="text-xs text-stone-500 mt-1">(Voice AI available)</p>
            </div>
          </div>
        </div>

        <PigeonMapComponent locations={allLocations} />

        {housingResults.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-semibold mb-4 text-stone-800">Low-Cost Housing near "{zipcode}"</h2>
            <div className="space-y-4">
              {housingResults.map((item) => (
                <div key={item.id} className="bg-white p-4 rounded-lg shadow border border-stone-200">
                  <h3 className="font-semibold text-lg text-stone-900">{item.name}</h3>
                  <p className="text-stone-600">{item.address}</p>
                  <p className="text-sm text-stone-500 mt-1">Phone: {item.phone}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {resourceResults.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-semibold mb-4 text-stone-800">Food & Utility Resources near "{zipcode}"</h2>
            <div className="space-y-4">
              {resourceResults.map((item) => (
                <div key={item.id} className="bg-white p-4 rounded-lg shadow border-l-4 border-teal-500">
                  <span className="inline-flex items-center rounded-md bg-teal-50 px-2 py-1 text-xs font-medium text-teal-700 ring-1 ring-inset ring-teal-700/10 mb-2">
                    {item.category}
                  </span>
                  <h3 className="font-semibold text-lg text-stone-900">{item.name}</h3>
                  <p className="text-stone-600">{item.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}
        
        <div>
          <h2 className="text-2xl font-semibold text-center mb-6 text-stone-800">
            Browse Resources by Category
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <ResourceCard
              href="/housing"
              title="Housing Assistance"
              description="Find low-cost housing, rent support, and shelter information."
            />
            <ResourceCard
              href="/foodstamps"
              title="Food Stamps (SNAP)"
              description="Check eligibility and find application help for food assistance."
            />
            <ResourceCard
              href="/energy"
              title="Energy & Utilities"
              description="Get help with energy bills and find low-cost utility programs."
            />
          </div>
        </div>

      </div>
    </main>
  );
}

// --- Reusable ResourceCard component ---
function ResourceCard({ title, description, href = "#" }) {
  return (
    <Link href={href} className="block p-6 bg-white rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-transform duration-200 border-t-4 border-teal-600">
        <h3 className="text-xl font-semibold text-stone-900 mb-2">{title}</h3>
        <p className="text-stone-600">{description}</p>
        <div className="text-teal-600 font-semibold mt-4 inline-block">
          Learn more &rarr;
        </div>
    </Link>
  );
}



