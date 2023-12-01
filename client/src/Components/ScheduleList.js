// ScheduleList.js
import React, { useState, useEffect } from "react";

function ScheduleList() {
  const [schedules, setSchedules] = useState([]);

  useEffect(() => {
    // Fetch schedule data from the backend when the component mounts
    fetchData();
  }, []); // Empty dependency array to ensure it runs only once when the component mounts

  const fetchData = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/schedules"); // Update with your backend endpoint
      if (!response.ok) {
        throw new Error("Error fetching schedules");
      }

      const data = await response.json();
      setSchedules(data);
    } catch (error) {
      console.error("Error fetching data from the backend", error);
    }
  };

  return (
    <div className="schedule-list">
      <h2>Schedule List</h2>
      <ul>
        {schedules.map((schedule) => (
          <li key={schedule.id}>
            {schedule.departure} to {schedule.arrival} at {schedule.time}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ScheduleList;
