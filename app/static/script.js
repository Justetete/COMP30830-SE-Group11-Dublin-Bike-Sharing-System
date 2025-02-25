let mapLoaded = false;
const mapElement = document.getElementById('map');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !mapLoaded) {
            // Load the Google Maps API when the map is in view
            const script = document.createElement('script');
            script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyDuYhHbAe7sJjIaVw8NL-pSHacXpH3cv1U&callback=initMap";
            script.async = true;
            script.defer = true;
            document.body.appendChild(script);

            mapLoaded = true; // Prevent loading multiple times
        }
    });
});

observer.observe(mapElement);

window.initMap = function() {
const map = new google.maps.Map(document.getElementById('map'), {
 center: { lat: 53.349805, lng: -6.26031 }, // Dublin, Ireland
 zoom: 12
});

const marker = new google.maps.Marker({
 position: { lat: 53.349805, lng: -6.26031 },
 map: map,
 title: "Dublin, Ireland"
});
}
