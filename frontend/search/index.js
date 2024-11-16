apiKey = "";

const coords = [
  [52.5, 13.4],
  [52.6, 13.5],
  [52.5, 13.6],
];

// Initialize the map
const map = tt.map({
  key: apiKey,
  container: "map",
  center: [13.4, 52.5],
  zoom: 10,
});
