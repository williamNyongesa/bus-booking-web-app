import React from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  const handleBookHereClick = () => {
    navigate("/booking");
  };

  return (
    <div className="home-container">
      <h2>Welcome to Bus Connect!</h2>
      <p>Explore our services and book your journey now.</p>
      <button onClick={handleBookHereClick} className="book-button">
        BOOK HERE
      </button>
    </div>
  );
}

export default Home;
