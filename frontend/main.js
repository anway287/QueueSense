const places = [
    {
      id: "dmv_midtown",
      name: "DMV Midtown",
      lat: 40.754,
      lon: -73.984
    },
    {
      id: "nyc_coffee_1",
      name: "Joe's Coffee NYC",
      lat: 40.73061,
      lon: -73.935242
    },
    {
      id: "urgentcare_parkave",
      name: "Park Ave Urgent Care",
      lat: 40.741895,
      lon: -73.989308
    }
  ];
  
  
  const map = L.map('map').setView([40.754, -73.984], 13);
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18
  }).addTo(map);
  
  places.forEach(async place => {
    try {
      const res = await fetch(`http://localhost:8000/predict?place_id=${place.id}`);
      const data = await res.json();
  
      const waitTime = data.predicted_wait_minutes ?? "N/A";
  
      L.marker([place.lat, place.lon])
        .addTo(map)
        .bindPopup(`<b>${place.name}</b><br>Predicted Wait: <strong>${waitTime} mins</strong>`);
    } catch (err) {
      console.error("Error fetching prediction for", place.id, err);
    }
  });
  