function findBestRoute() {
    let source = document.getElementById("source").value;
    let destination = document.getElementById("destination").value;

    if (!source || !destination) {
        alert("Please enter both source and destination.");
        return;
    }

    fetch(`/find_best_route?source=${encodeURIComponent(source)}&destination=${encodeURIComponent(destination)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            document.getElementById("route-info").innerHTML = `<a href="${data.route_link}" target="_blank">Open Route in Google Maps</a>`;
            document.getElementById("aqi-info").innerText = `AQI at Destination: ${data.aqi}`;
            document.getElementById("transport-info").innerText = `Recommended Transport: ${data.transport_recommendation}`;
            document.getElementById("coin-info").innerText = data.coins;

            // Display route on Google Maps
            displayRouteOnMap(source, destination);
        })
        .catch(error => console.error("Error fetching route:", error));
}

function displayRouteOnMap(source, destination) {
    let map = new google.maps.Map(document.getElementById("map"), {
        zoom: 7,
        center: { lat: 20.5937, lng: 78.9629 } // Default to India
    });

    let directionsService = new google.maps.DirectionsService();
    let directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    directionsService.route(
        {
            origin: source,
            destination: destination,
            travelMode: "DRIVING"
        },
        function (response, status) {
            if (status === "OK") {
                directionsRenderer.setDirections(response);
            } else {
                console.error("Error fetching directions: " + status);
            }
        }
    );
}
