// src/app/components/PigeonMap.jsx
"use client";

import React, { useState, useEffect } from 'react';
import { Map, Marker, Overlay } from "pigeon-maps";

// This component receives the search results as a 'locations' prop
export default function PigeonMap({ locations }) {
  // Set a default center (e.g., Atlanta)
  const [center, setCenter] = useState([33.7490, -84.3880]);
  const [zoom, setZoom] =useState(13);
  
  // State to track which marker is clicked
  const [selected, setSelected] = useState(null);

  // When the locations prop changes (i.e., new search),
  // update the map's center to the first location.
  useEffect(() => {
    if (locations && locations.length > 0) {
      // Set center to the first location in the results
      setCenter([locations[0].lat, locations[0].lng]);
      setZoom(14); // Zoom in a bit
      setSelected(null); // Clear any selected marker
    } else {
      // If no locations, reset to default
      setCenter([33.7490, -84.3880]);
      setZoom(13);
      setSelected(null);
    }
  }, [locations]); // This effect runs whenever 'locations' changes

  // If there are no locations, don't render anything
  if (!locations || locations.length === 0) {
    return null;
  }

  return (
    // Set a height and width for the map container
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
        {/* Loop through each location and create a Marker */}
        {locations.map((loc) => (
          <Marker 
            key={loc.id} 
            width={40} // Size of the marker icon
            anchor={[loc.lat, loc.lng]} 
            color="#db4437" // A red color for the marker
            onClick={() => setSelected(loc)} // Set this as the selected location on click
          />
        ))}

        {/* If a location is selected, show an info box (Overlay) */}
        {selected && (
          <Overlay 
            anchor={[selected.lat, selected.lng]} 
            offset={[120, 70]} // Position offset for the info box
          >
            <div 
              className="bg-white p-3 rounded-lg shadow-xl border" 
              style={{ minWidth: '200px' }}
            >
              <h4 className="font-bold text-md text-gray-900">{selected.name}</h4>
              <p className="text-sm text-gray-600">{selected.address}</p>
              <p className="text-sm text-gray-500">{selected.phone}</p>
              {/* Close button */}
              <button 
                onClick={() => setSelected(null)} 
                className="text-xs font-bold text-red-600 mt-1"
              >
                Close
              </button>
            </div>
          </Overlay>
        )}
      </Map>
    </div>
  );
}