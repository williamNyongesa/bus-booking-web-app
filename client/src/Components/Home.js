import React from 'react';
import { useNavigate } from 'react-router-dom';

function Home({ isuser, isdriver, isadmin, role, setRole }) {
  const navigate = useNavigate();

  const handleBookHereClick = () => {
    navigate("/booking");
  };

  // Conditional rendering based on the user's role
  if (isadmin) {
    // If the user is an admin, render admin-specific content
    return (
      <div className="admin-home-container">
        <h2 className="admin-welcome-message">Welcome, Admin!</h2>
        <p className="admin-home-description">
          Manage the Bus Connect services and bookings here.
        </p>
        {/* Add admin-specific components or buttons as needed */}
      </div>
    );
  } else if (isdriver) {
    // If the user is a driver, render driver-specific content
    return (
      <div className="driver-home-container">
        <h2 className="driver-welcome-message">Welcome, Driver!</h2>
        <p className="driver-home-description">
          View your assigned routes and manage your schedule here.
        </p>
        {/* Add driver-specific components or buttons as needed */}
      </div>
    );
  }

  // If the user is not an admin or driver, render regular user content
  return (
    <div className="home-container">
      <h2 className="welcome-message">Welcome to Bus Connect!</h2>
      <p className="home-description">
        Explore our services and book your journey now.
      </p>
      <button onClick={handleBookHereClick} className="book-button">
        BOOK HERE
      </button>
    </div>
  );
}

export default Home;
