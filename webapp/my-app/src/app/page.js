// This directive tells Next.js that this is a client-side component,
// which is required because we use state (useState) for the input form.
"use client";

import React, { useState } from 'react';
import './globals.css';
import { placeholderResources } from './data/placeholderResources'; // <-- This import is correct

// --- Placeholder Data ---
const placeholderHousingData = {
  "30303": [
    { id: 1, name: "Downtown Affordable Housing", address: "123 Peachtree St, Atlanta, GA 30303", phone: "404-555-1000" },
    { id: 2, name: "Community Housing Partners", address: "456 Auburn Ave, Atlanta, GA 30303", phone: "404-555-2000" },
  ],
  "10001": [
    { id: 3, name: "Midtown Low-Income Apartments", address: "789 8th Ave, New York, NY 10001", phone: "212-555-3000" },
  ]
};
// -------------------------


export default function HomePage() {
  // State to hold the user's zipcode input
  const [zipcode, setZipcode] = useState("");
  
  // State to hold the *housing* search results
  const [housingResults, setHousingResults] = useState([]); // <-- MODIFIED (renamed from 'results')

  // State to hold the *other* resource results
  const [resourceResults, setResourceResults] = useState([]); // <-- ADDED

  /**
   * Handles the form submission when the user clicks "Search"
   */
  const handleSearch = (e) => {
    e.preventDefault(); // Prevent the form from reloading the page
    
    // --- 1. Search for Housing ---
    const housingData = placeholderHousingData[zipcode] || [];
    setHousingResults(housingData); // <-- MODIFIED (use new state)

    // --- 2. Search for Other Resources ---
    const otherResources = placeholderResources[zipcode] || []; // <-- ADDED
    setResourceResults(otherResources); // <-- ADDED
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-8 md:p-16 bg-gray-50">
      <div className="w-full max-w-5xl">
        
        {/* 1. App Description (No Change) */}
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-3">
            Resource Connect
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Connecting underserved communities with unclaimed resources. We help you find low-cost housing, food assistance, and energy support, all in one place.
          </p>
        </header>

        {/* 2. Zipcode Input and Call Section (No Change) */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-12">
          {/* ... your form and call button code ... */}
           {/* Zipcode Form */}
           <form onSubmit={handleSearch} className="md:col-span-2">
              <label htmlFor="zipcode" className="block text-sm font-medium text-gray-700 mb-1">
                Find resources near you
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  name="zipcode"
                  id="zipcode"
                  value={zipcode}
                  onChange={(e) => setZipcode(e.target.value)}
                  className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                  placeholder="Enter your zipcode"
                />
                <button
                  type="submit"
                  className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  Search
                </button>
              </div>
            </form>

            {/* Accessibility / Call Option */}
            <div className="text-center md:border-l md:border-gray-200 md:pl-6">
              <p className="text-sm font-medium text-gray-700 mb-1">
                Need help by phone?
              </p>
              {/* This is a clickable phone link */}
              <a 
                href="tel: (205)-293-8808" 
                className="text-lg font-semibold text-indigo-600 hover:text-indigo-500"
              >
                Call (205)-293-8808
              </a>
              <p className="text-xs text-gray-500 mt-1">(Voice AI available)</p>
            </div>
        </div>

        {/* 3. Housing Results Section (MODIFIED) */}
        {/* This section only appears if the 'housingResults' array has items in it */}
        {housingResults.length > 0 && ( // <-- MODIFIED (use new state)
          <div className="mb-12">
            <h2 className="text-2xl font-semibold mb-4">
              Low-Cost Housing near "{zipcode}"
            </h2>
            <div className="space-y-4">
              {housingResults.map((item) => ( // <-- MODIFIED (use new state)
                <div key={item.id} className="bg-white p-4 rounded-lg shadow">
                  <h3 className="font-semibold text-lg text-gray-900">{item.name}</h3>
                  <p className="text-gray-600">{item.address}</p>
                  <p className="text-sm text-gray-500 mt-1">Phone: {item.phone}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 4. Other Resources Section (ADDED) */}
        {resourceResults.length > 0 && ( // <-- ADDED
          <div className="mb-12">
            <h2 className="text-2xl font-semibold mb-4">
              Food & Utility Resources near "{zipcode}"
            </h2>
            <div className="space-y-4">
              {resourceResults.map((item) => (
                <div key={item.id} className="bg-white p-4 rounded-lg shadow border-l-4 border-indigo-500">
                  {/* Category Tag */}
                  <span className="inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-xs font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10 mb-2">
                    {item.category}
                  </span>
                  <h3 className="font-semibold text-lg text-gray-900">{item.name}</h3>
                  <p className="text-gray-600">{item.description}</p>
                  <p className="text-sm text-gray-500 mt-2">{item.address}</p>
                  <p className="text-sm text-gray-500">Phone: {item.phone}</p>
                  <a 
                    href={item.website} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="text-sm text-indigo-600 hover:text-indigo-500 font-medium"
                  >
                    Visit Website &rarr;
                  </a>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 5. Static Resource Cards (No Change) */}
        <div>
          <h2 className="text-2xl font-semibold text-center mb-6">
            Browse Resources by Category
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* ... your ResourceCard components ... */}
            <ResourceCard
              title="Housing Assistance"
              description="Find low-cost housing, rent support, and shelter information."
            />
            
            <ResourceCard
              title="Food Stamps (SNAP)"
              description="Check eligibility and find application help for food assistance."
            />
            
            <ResourceCard
              title="Energy & Utilities"
              description="Get help with energy bills and find low-cost utility programs."
            />
          </div>
        </div>

      </div>
    </main>
  );
}

/**
 * A reusable component for the resource cards
 */
function ResourceCard({ title, description }) {
  // ... (No change to this component) ...
  return (
    <div className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
      <a 
        href="#" 
        className="text-indigo-600 hover:text-indigo-500 font-semibold mt-4 inline-block"
      >
        Learn more &rarr;
      </a>
    </div>
  );
}