import { initMap } from "./map.js";

let mapLoaded = false; // Flag to track whether the Google Maps API has been loaded
const mapElement = document.getElementById('map');

/**
 * Creates an Intersection Observer to detect when the map element is visible in the viewport.
 * If the map enters the viewport and has not been loaded yet, the function dynamically loads
 * the Google Maps JavaScript API.
 */
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !mapLoaded) { // Check if the map is visible and has not been loaded
            // Dynamically create and append the Google Maps API script
            const script = document.createElement('script');
            script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyDuYhHbAe7sJjIaVw8NL-pSHacXpH3cv1U&callback=initMap';
            script.async = true; // Load asynchronously to avoid blocking rendering
            script.defer = true; // Defer execution until the page has fully loaded
            document.body.appendChild(script);

            // Prevent multiple script injections
            mapLoaded = true;
        }
    });
});

// Start observing the map element to trigger the API loading when it comes into view
observer.observe(mapElement);

/**
 * Exposes the `initMap` function globally so that it can be called as a callback 
 * by the Google Maps API after the script loads.
 */
window.initMap = initMap;

