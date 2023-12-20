// BusList.js
import React, { useState, useEffect } from "react";
import { Table, Container } from "react-bootstrap";

const BusList = () => {
  const [buses, setBuses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBuses = async () => {
      try {
        setLoading(true);

        const response = await fetch("http://localhost:5000/buses", {
          method: "GET",
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to fetch buses");
        }

        const data = await response.json();
        setBuses(data);
      } catch (error) {
        console.error("Error fetching buses:", error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchBuses();
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <Container className="mt-4 bus-list">
      <h3>List of Buses</h3>
      {buses.length === 0 ? (
        <p>No buses available.</p>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Number of Seats</th>
              <th>Cost per Seat</th>
              <th>Route</th>
              <th>Time of Travel</th>
            </tr>
          </thead>
          <tbody>
            {buses.map((bus) => (
              <tr key={bus.id}>
                <td>{bus.number_of_seats}</td>
                <td>{bus.cost_per_seat}</td>
                <td>{bus.route}</td>
                <td>{bus.time_of_travel}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </Container>
  );
};

export default BusList;
