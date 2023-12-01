// AddScheduleForm.js
import React, { useState } from "react";

function AddScheduleForm({ onAddSchedule }) {
  const [departure, setDeparture] = useState("");
  const [arrival, setArrival] = useState("");
  const [time, setTime] = useState("");
  const [error, setError] = useState(null);

  const handleAddSchedule = async () => {
    try {
      const newSchedule = {
        departure,
        arrival,
        time,
      };

      const response = await fetch("http://localhost:5555/schedules", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newSchedule),
      });

      if (!response.ok) {
        throw new Error("Error adding schedule");
      }

      const addedSchedule = await response.json();
      onAddSchedule(addedSchedule);

      // Reset form fields
      setDeparture("");
      setArrival("");
      setTime("");
      setError(null);
    } catch (error) {
      console.error("Error adding schedule", error);
      setError("Error adding schedule. Please try again.");
    }
  };

  return (
    <div className="add-schedule-form">
      <h2>Add Schedule</h2>
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
      <label>Time:</label>
      <input
        type="text"
        value={time}
        onChange={(e) => setTime(e.target.value)}
      />
      <button onClick={handleAddSchedule}>Add Schedule</button>

      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

export default AddScheduleForm;
