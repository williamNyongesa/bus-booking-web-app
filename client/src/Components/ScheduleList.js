// ScheduleList.js
import React, { useState, useEffect } from "react";
import { Container, Table, Button, Modal, Form } from "react-bootstrap";

const ScheduleList = ({ searchDeparture, searchArrival }) => {
  const [schedules, setSchedules] = useState([]);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editedSchedule, setEditedSchedule] = useState({});
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deletedSchedule, setDeletedSchedule] = useState({});

  useEffect(() => {
    // Fetch the schedule list from the backend on component mount
    const fetchSchedules = async () => {
      try {
        const response = await fetch("http://localhost:5000/add-schedule", {
          method: "GET",
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to fetch schedules");
        }

        const data = await response.json();
        setSchedules(data);
      } catch (error) {
        console.error("Error fetching schedules:", error.message);
      }
    };

    fetchSchedules();
  }, []); // Empty dependency array ensures the effect runs only once on mount

  const handleEdit = (schedule) => {
    setEditedSchedule(schedule);
    setShowEditModal(true);
  };

  const handleDelete = (schedule) => {
    setDeletedSchedule(schedule);
    setShowDeleteModal(true);
  };

  const handleCloseEditModal = () => {
    setEditedSchedule({});
    setShowEditModal(false);
  };

  const handleCloseDeleteModal = () => {
    setDeletedSchedule({});
    setShowDeleteModal(false);
  };

  const handleSaveEdit = async () => {
    try {
      const response = await fetch("http://localhost:5000/edit-schedule", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(editedSchedule),
      });

      if (!response.ok) {
        throw new Error("Failed to edit schedule");
      }

      const updatedSchedulesResponse = await fetch(
        "http://localhost:5000/add-schedule"
      );

      if (!updatedSchedulesResponse.ok) {
        throw new Error("Failed to fetch updated schedules");
      }

      const updatedSchedules = await updatedSchedulesResponse.json();
      setSchedules(updatedSchedules);
      handleCloseEditModal();
    } catch (error) {
      console.error("Error editing or fetching schedule:", error.message);
    }
  };

  const handleConfirmDelete = async () => {
    try {
      const response = await fetch("http://localhost:5000/delete-schedule", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: deletedSchedule.id }),
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Failed to delete schedule");
      }

      const updatedSchedulesResponse = await fetch(
        "http://localhost:5000/add-schedule"
      );

      if (!updatedSchedulesResponse.ok) {
        throw new Error("Failed to fetch updated schedules");
      }

      const updatedSchedules = await updatedSchedulesResponse.json();
      setSchedules(updatedSchedules);
      handleCloseDeleteModal();
    } catch (error) {
      console.error("Error deleting or fetching schedule:", error.message);
    }
  };

  // Filter schedules based on search criteria
  const filteredSchedules = schedules.filter(
    (schedule) =>
      schedule.departure_place
        .toLowerCase()
        .includes(searchDeparture.toLowerCase()) &&
      schedule.arrival_place.toLowerCase().includes(searchArrival.toLowerCase())
  );

  return (
    <Container className="mt-4 schedule-list-container">
      <h2>Schedule List</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Departure Place</th>
            <th>Arrival Place</th>
            <th>Departure Time</th>
            <th>Price</th>
            <th>Bus ID</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredSchedules.map((schedule, index) => (
            <tr key={schedule.id}>
              <td>{schedule.departure_place}</td>
              <td>{schedule.arrival_place}</td>
              <td>{schedule.departure_time}</td>
              <td>{schedule.price}</td>
              <td>{schedule.bus_id}</td>
              <td>
                <Button
                  variant="info"
                  size="sm"
                  className="ml-2"
                  onClick={() => handleEdit(schedule)}
                >
                  Edit
                </Button>
                <Button
                  variant="danger"
                  size="sm"
                  className="ml-2"
                  onClick={() => handleDelete(schedule)}
                >
                  Delete
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      {/* Edit Schedule Modal */}
      <Modal show={showEditModal} onHide={handleCloseEditModal}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Schedule</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Departure Time:</Form.Label>
              <Form.Control
                type="text"
                value={editedSchedule.departure_time || ""}
                onChange={(e) =>
                  setEditedSchedule({
                    ...editedSchedule,
                    departure_time: e.target.value,
                  })
                }
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Arrival Time:</Form.Label>
              <Form.Control
                type="text"
                value={editedSchedule.arrival_time}
                onChange={(e) =>
                  setEditedSchedule({
                    ...editedSchedule,
                    arrival_time: e.target.value,
                  })
                }
                required
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseEditModal}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSaveEdit}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Delete Schedule Modal */}
      <Modal show={showDeleteModal} onHide={handleCloseDeleteModal}>
        <Modal.Header closeButton>
          <Modal.Title>Delete Schedule</Modal.Title>
        </Modal.Header>
        <Modal.Body>Are you sure you want to delete this schedule?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseDeleteModal}>
            Cancel
          </Button>
          <Button variant="danger" onClick={handleConfirmDelete}>
            Confirm Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default ScheduleList;
