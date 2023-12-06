import React, { useEffect, useState } from "react";
import ScheduleList from "./ScheduleList"; // Import ScheduleList component
import AddScheduleForm from "./AddScheduleForm"; // Import AddScheduleForm component

const AdminDashboardComp = () => {
  const [schedules, setSchedules] = useState([]);
  const [userRole, setUserRole] = useState("");
  const [adminDetails, setAdminDetails] = useState(null); // State to store admin details

  useEffect(() => {
    // Fetch user information including role and admin details
    const fetchUserInfo = async () => {
      try {
        const response = await fetch("http://localhost:5000/session", {
          credentials: "include", // Include credentials (cookies) in the request
        });

        const data = await response.json();

        if (response.ok) {
          setUserRole(data.role);

          // Fetch admin details if the user is an admin
          if (data.role === "admin") {
            const adminDetailsResponse = await fetch(
              "http://localhost:5000/admin-details",
              {
                credentials: "include", // Include credentials (cookies) in the request
              }
            );

            const adminDetailsData = await adminDetailsResponse.json();

            if (adminDetailsResponse.ok) {
              setAdminDetails(adminDetailsData);
            console.log(adminDetailsData)
            } else {
              console.error(
                "Error fetching admin details:",
                adminDetailsData.error
              );
            }
          }
        } else {
          console.error("Error fetching user information:", data.error);
        }
      } catch (error) {
        console.error("Error fetching user information:", error);
      }
    };

    fetchUserInfo();
  }, []);

  return (
    <div>
      <h2>Welcome to Admin Dashboard</h2>
      
        <>
          <div>
            {/* Render admin pre-login details here */}
            {adminDetails && (
              <div>
                <p>Admin Information:</p>
                <p>Name: {adminDetails.name}</p>
                <p>Email: {adminDetails.email}</p>
                {/* Add other admin details as needed */}
              </div>
            )}
          </div>
          <AddScheduleForm /> {/* Render only for admin */}
        </>
      
      <h3>Schedule List</h3>
      <ScheduleList schedules={schedules} />{" "}
      {/* Render the ScheduleList component */}
    </div>
  );
};

export default AdminDashboardComp;
