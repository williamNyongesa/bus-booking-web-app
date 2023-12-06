import React, { useEffect, useState } from "react";
import ScheduleList from "./ScheduleList";

const DriverDashboard = () => {
  const [schedules, setSchedules] = useState([]);

  useEffect(() => {
    // Fetch schedules for the driver dashboard
    const fetchSchedules = async () => {
      try {
        const response = await fetch("http://localhost:5000/driver-schedules");
        const data = await response.json();
        if (response.ok) {
          setSchedules(data);
        } else {
          console.error("Error fetching driver schedules:", data.error);
        }
      } catch (error) {
        console.error("Error fetching driver schedules:", error);
      }
    };

    fetchSchedules();
  }, []);

  return (
    <div>
      <h2>Welcome to Driver Dashboard</h2>
      <h3>Schedule List</h3>
      <ScheduleList schedules={schedules} />{" "}
      {/* Render the ScheduleList component */}
    </div>
  );
};

export default DriverDashboard;
