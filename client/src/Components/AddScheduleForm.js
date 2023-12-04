import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Updated import
import { Button, Form, Container } from "react-bootstrap";

const AddScheduleForm = ({ onAddSchedule }) => {
  const [departurePlace, setDeparturePlace] = useState("");
  const [arrivalPlace, setArrivalPlace] = useState("");
  const [departureTime, setDepartureTime] = useState("");
  const [price, setPrice] = useState("");
  const [busId, setBusId] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newSchedule = {
      departure_place: departurePlace,
      arrival_place: arrivalPlace,
      departure_time: new Date(`2000-01-01T${departureTime}:00`),
      price: price,
      bus_id: busId,
    };

    // Send the new schedule to the backend
    try {
      const response = await fetch("http://localhost:5000/add-schedule", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newSchedule),
        credentials: "include",
      });

      console.log("Response status:", response.status);

      if (!response.ok) {
        throw new Error("Failed to add schedule");
      }

      // Clear the form fields if posting is successful
      setDeparturePlace("");
      setArrivalPlace("");
      setDepartureTime("");
      setPrice("");
      setBusId("");

      // Redirect to the schedule list page
      navigate("/schedule-list"); // Updated usage
    } catch (error) {
      console.error("Error adding schedule:", error.message);
      // Handle error (show an error message, etc.)
    }
  };

  return (
    <Container className="mt-4 add-schedule-container">
      <h2 className="add-schedule-title">Add Bus Schedule</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3 ">
          <Form.Label className="place-label">Departure Place:</Form.Label>
          <Form.Control
            type="text"
            value={departurePlace}
            onChange={(e) => setDeparturePlace(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label className="place-label">Arrival Place:</Form.Label>
          <Form.Control
            type="text"
            value={arrivalPlace}
            onChange={(e) => setArrivalPlace(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label className="place-label">Departure Time:</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter time in HH:mm format"
            value={departureTime}
            onChange={(e) => setDepartureTime(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label className="place-label">Price:</Form.Label>
          <Form.Control
            type="text"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label className="place-label">Bus ID:</Form.Label>
          <Form.Control
            type="text"
            value={busId}
            onChange={(e) => setBusId(e.target.value)}
            required
          />
        </Form.Group>

        <Button className="add-schedule" type="submit">
          Add Schedule
        </Button>
      </Form>
    </Container>
  );
};

export default AddScheduleForm;
