// AddBusForm.js
import React, { useState } from "react";
import { Form, Button, Container } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const AddBusForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    number_of_seats: "",
    cost_per_seat: "",
    route: "",
    time_of_travel: "",
  });

  const { number_of_seats, cost_per_seat, route, time_of_travel } = formData;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:5000/buses", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          number_of_seats,
          cost_per_seat,
          route,
          time_of_travel,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to add bus");
      }

      // Redirect to bus list after successful addition
      navigate("/bus-list");
    } catch (error) {
      console.error("Error adding bus:", error.message);
    }
  };

  return (
    <Container className="mt-4 add-bus-form">
      <h3>Add Bus</h3>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="number_of_seats">
          <Form.Label>Number of Seats</Form.Label>
          <Form.Control
            type="number"
            value={number_of_seats}
            onChange={handleChange}
            name="number_of_seats"
            required
          />
        </Form.Group>

        <Form.Group controlId="cost_per_seat">
          <Form.Label>Cost per Seat</Form.Label>
          <Form.Control
            type="number"
            value={cost_per_seat}
            onChange={handleChange}
            name="cost_per_seat"
            required
          />
        </Form.Group>

        <Form.Group controlId="route">
          <Form.Label>Route</Form.Label>
          <Form.Control
            type="text"
            value={route}
            onChange={handleChange}
            name="route"
            required
          />
        </Form.Group>

        <Form.Group controlId="time_of_travel">
          <Form.Label>Time of Travel</Form.Label>
          <Form.Control
            type="text"
            value={time_of_travel}
            onChange={handleChange}
            name="time_of_travel"
            required
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          Add Bus
        </Button>
      </Form>
    </Container>
  );
};

export default AddBusForm;
