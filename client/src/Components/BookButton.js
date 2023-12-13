// BookButton.js
import React, { useState } from "react";

const BookButton = ({ scheduleId, onBookingComplete }) => {
  const [bookingStatus, setBookingStatus] = useState(null);

  const handleBookClick = async () => {
    try {
      const response = await fetch("http://localhost:5000/bookings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ schedule_id: scheduleId }),
      });

      if (!response.ok) {
        throw new Error("Failed to create booking");
      }

      const data = await response.json();
      setBookingStatus(data.message);

      // Notify the parent component (SearchResults) about the booking completion
      onBookingComplete();
    } catch (error) {
      console.error("Error creating booking:", error.message);
      setBookingStatus("Error creating booking");
    }
  };

  return (
    <div>
      <button
        className="green-button"
        onClick={handleBookClick}
        disabled={bookingStatus}
      >
        {bookingStatus ? "Booked" : "Book Now"}
      </button>
      {bookingStatus && <p>{bookingStatus}</p>}
    </div>
  );
};

export default BookButton;
