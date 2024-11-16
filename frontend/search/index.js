apiKey = "rNABltQ9BhEQlHEL4si3TgBX4J7WRZ8I+";

function initMap(waypoints, mapId) {
  // Initialize the map
  const bounds = new tt.LngLatBounds();
  waypoints.forEach((point) => bounds.extend(point));

  const map = tt.map({
    key: apiKey,
    container: mapId,
    bounds: bounds,
    fitBoundsOptions: { padding: 35 },
  });

  // Add markers for the waypoints
  waypoints.forEach((point, index) => {
    let color = "black";
    let markerOptions = { color: color };
    if (index === 0) {
      color = "blue";
      markerOptions = { element: document.createElement("div") };
      markerOptions.element.style.backgroundColor = color;
      markerOptions.element.style.width = "10px";
      markerOptions.element.style.height = "10px";
      markerOptions.element.style.borderRadius = "50%";
    } else if (index === waypoints.length - 1) {
      color = "red";
      markerOptions = { color: color };
    }
    new tt.Marker(markerOptions).setLngLat(point).addTo(map);
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

      // Get estimated time
      const estimatedTime = routeData.routes[0].summary.travelTimeInSeconds / 60; // Convert seconds to minutes
      document.getElementById(mapId + "min").innerText = `Estimated Time: ${Math.round(estimatedTime)} minutes`;
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
  if (!testing) {
    data = await fetch(`http://localhost:5000/getUser/${userId}`).then((response) => response.json());
    console.log(data);
    return;
  } else {
    data = {
      id: 1,
      name: "John Doe",
      waypoints: [
        [42.9849, -81.2453],
        [43.9849, -81.3453],
        [43.4643, -81.3204],
        [43.4643, -81.5304],
      ],
    };

    data = {
      driver: {
        user_id: "24e5b87f-2809-45eb-98d6-a6312b549527",
        name: "Walter Nguyen",
        gender: "Male",
        driver_rider: "Driver",
        start_location: "45.4215,-75.6972",
        destination_location: "43.7001,-79.4163",
        time_of_travel: "8:49",
        max_detour_distance: "6",
        non_smoking: "FALSE",
        same_gender: "TRUE",
        no_free_seats: "4",
      },
      riders: [
        {
          user_id: "55e6c0f7-aca0-45d2-9bed-7874783b5903",
          name: "Russell Stephens",
          gender: "Male",
          driver_rider: "Rider",
          start_location: "42.9976,-82.3078",
          destination_location: "42.9976,-82.3078",
          time_of_travel: "18:44",
          max_detour_distance: "5",
          non_smoking: "TRUE",
          same_gender: "TRUE",
          no_of_persons: "1",
        },
        {
          user_id: "281bd0c7-a92a-448a-a923-d3f6f5234b31",
          name: "Christopher Petersen",
          gender: "Male",
          driver_rider: "Rider",
          start_location: "42.9849,-81.2453",
          destination_location: "43.7001,-79.4163",
          time_of_travel: "7:04",
          max_detour_distance: "8",
          non_smoking: "FALSE",
          same_gender: "TRUE",
          no_of_persons: "2",
        },
        {
          user_id: "521a5d60-45e1-417a-9558-b273562ee201",
          name: "Teresa Barnes",
          gender: "Female",
          driver_rider: "Rider",
          start_location: "43.7001,-79.4163",
          destination_location: "42.9976,-82.3078",
          time_of_travel: "7:55",
          max_detour_distance: "15",
          non_smoking: "TRUE",
          same_gender: "FALSE",
          no_of_persons: "2",
        },
      ],
    };
  }

  if (!data) {
    alert("User not found");
    return;
  }

  data.waypoints = data.waypoints.map((point) => [point[1], point[0]]);

  const card = document.getElementById("card");
  card.innerHTML = `
    <div class="card mt-4 bg-dark text-white">
      <div class="card-header bg-secondary">Driver Map/User Map</div>
      <div class="card-body">
        <div class="row">
          <div class="col-md-7">
            <h5 class="card-title" style="font-family: 'Arial', sans-serif">
              Thank you for helping us cut down carbon emissions! 🍃<br />Here is your carbon-friendly commute map.
            </h5>
            <br />
            
            
            <br />
            <p id="startTime" class="card-text">Start the Journey at ??</p>
            <p id="stop1" class="card-text">First Stop:</p>
            <p id="stop2" class="card-text">Second Stop:</p>
            <p id="stop3" class="card-text">Third Stop:</p>
            <p id="final" class="card-text">Final Destination:</p>
          </div>
          <div class="col-md-5">
            <h5>Old Directions</h5>
            <h6 id="mapmin" class="card-title" style="color: #ffcc00">Estimated Time: ?? minutes</h6>
            <div style="width: 100%; height: 200px" id="map"></div>
            <h5 class="mt-4">New Directions</h5>
            <h6 id="map2min" class="card-title" style="color: #ffcc00">Estimated Time: ?? minutes</h6>
            <div style="width: 100%; height: 200px" id="map2"></div>
          </div>
        </div>
      </div>
    </div>
  `;

  await initMap(data.waypoints, "map2");
  document.getElementsByClassName("mapboxgl-ctrl-bottom-right")[0].remove();

  await initMap([data.waypoints[0], data.waypoints[data.waypoints.length - 1]], "map");
  document.getElementsByClassName("mapboxgl-ctrl-bottom-right")[0].remove();
}

function search() {
  let userId = document.getElementById("search").value;
  getData(userId, false);
}
