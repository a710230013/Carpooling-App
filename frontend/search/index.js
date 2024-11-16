apiKey = "";

function initMap(waypoints) {
  // Initialize the map
  const bounds = new tt.LngLatBounds();
  waypoints.forEach((point) => bounds.extend(point));

  const map = tt.map({
    key: apiKey,
    container: "map",
    bounds: bounds,
    fitBoundsOptions: { padding: 30 },
  });

  // Add markers for the waypoints
  waypoints.forEach((point, index) => {
    new tt.Marker().setLngLat(point).addTo(map);
  });

  // Calculate the route
  tt.services
    .calculateRoute({
      key: apiKey,
      locations: waypoints.map((point) => point.join(",")).join(":"),
    })
    .then(function (routeData) {
      const geojson = routeData.toGeoJson();
      map.addLayer({
        id: "route",
        type: "line",
        source: {
          type: "geojson",
          data: geojson,
        },
        paint: {
          "line-color": "#4a90e2",
          "line-width": 6,
        },
      });
    });

  // Draw the path from origin to destination
  map.on("load", function () {
    tt.services
      .calculateRoute({
        key: apiKey,
        locations: waypoints.map((point) => point.join(",")).join(":"),
      })
      .then(function (routeData) {
        const geojson = routeData.toGeoJson();
        map.addLayer({
          id: "route",
          type: "line",
          source: {
            type: "geojson",
            data: geojson,
          },
          paint: {
            "line-color": "#4a90e2",
            "line-width": 6,
          },
        });
      });
  });
}

async function getData(userId, testing) {
  let data;
  if (!testing) {
    data = await fetch(`http://localhost:3000/api/users/${userId}`).then((response) => response.json());
  } else {
    data = {
      id: 1,
      name: "John Doe",
      waypoints: [
        [-79.3527797, 43.6646928],
        [-79.2793535, 43.9027947],
        [-79.494486, 43.6584463],
      ],
    };
  }

  waypoints = data.waypoints;
  await initMap(waypoints);
  document.getElementsByClassName("mapboxgl-ctrl-bottom-right")[0].remove();
}

getData(123, true);
