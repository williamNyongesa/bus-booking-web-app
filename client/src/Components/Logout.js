import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function LogoutButton() {
  const [logoutMessage, setLogoutMessage] = useState(null);
  const navigate = useNavigate();
  const handleLogout = async () => {
    try {
      const response = await fetch("/logout", {
        method: "GET",
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        setLogoutMessage(data.message);
        navigate("/");
      } else {
        const errorData = await response.json();
        setLogoutMessage(errorData.error);
      }
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  return (
    <div>
      <p className="logout" onClick={handleLogout}>
        Logout
      </p>
      <p>{logoutMessage}</p>
    </div>
  );
}

export default LogoutButton;
