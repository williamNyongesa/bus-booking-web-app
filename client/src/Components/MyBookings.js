// MyBookings.js
import React, { useEffect, useState } from "react";
import { Container, Table } from "react-bootstrap";

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    const fetchUserBookings = async () => {
      try {
        const response = await fetch("http://localhost:5000/user-bookings", {
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to fetch user bookings");
        }

        const data = await response.json();
        setBookings(data);
      } catch (error) {
        console.error("Error fetching user bookings:", error.message);
      }
    };

    fetchUserBookings();
  }, []);

  return (
    <Container className="mt-4 my-bookings">
      <h3>Your Bookings:</h3>
      {bookings.length === 0 ? (
        <p>No bookings found.</p>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Departure Place</th>
              <th>Arrival Place</th>
              <th>Departure Time</th>
            </tr>
          </thead>
          <tbody>
            {bookings.map((booking) => (
              <tr key={booking.id}>
                <td>{booking.departure_place}</td>
                <td>{booking.arrival_place}</td>
                <td>{new Date(booking.departure_time).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </Container>
  );
};

export default MyBookings;
