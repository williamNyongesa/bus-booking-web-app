// Booking.js
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Booking() {
  const navigate = useNavigate();
  const [departure, setDeparture] = useState("");
  const [arrival, setArrival] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch schedule data from the Flask backend when the component mounts
    fetchData();
  }, []); // Empty dependency array to ensure it runs only once when the component mounts

  const fetchData = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/schedules"); // Update with your backend endpoint
      if (!response.ok) {
        throw new Error("Error fetching schedules");
      }

      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      setError("Error fetching data from the backend");
    }
  };

  const handleSearchClick = () => {
    // Filtering logic based on departure and arrival
    const results = searchResults.filter(
      (result) =>
        result.departure.toLowerCase().includes(departure.toLowerCase()) &&
        result.arrival.toLowerCase().includes(arrival.toLowerCase())
    );

    setSearchResults(results);

    if (results.length === 0) {
      setError("No matching schedules found.");
    } else {
      setError(null);
    }

    // navigate based on your requirements
    navigate(`/search?departure=${departure}&arrival=${arrival}`);
  };

  return (
    <div className="booking-container">
      <h2 className="title-description">Your Destination</h2>
      <label>Departure:</label>
      <input
        type="text"
        value={departure}
        onChange={(e) => setDeparture(e.target.value)}
      />
      <label>Arrival:</label>
      <input
        type="text"
        value={arrival}
        onChange={(e) => setArrival(e.target.value)}
      />
      <button onClick={handleSearchClick} className="search-button">
        SEARCH
      </button>

      {error && <p className="error-message">{error}</p>}

      {searchResults.length > 0 && (
        <div className="search-results">
          <h3>Search Results:</h3>
          <ul>
            {searchResults.map((result) => (
              <li key={result.id}>
                {result.departure} to {result.arrival} at {result.time}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Booking;
