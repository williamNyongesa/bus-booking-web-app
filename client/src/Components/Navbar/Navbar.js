import React from "react";
import Button from "react-bootstrap/Button";
import bus_icon from "../Images/bus.png";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import "./Navbar.css";
import LogoutButton from "../Logout";

function NavbarComp() {
  return (
    <Navbar collapseOnSelect expand="lg" className="custom-navbar">
      <Container>
        <Navbar.Brand href="/" className="bus-connect">
          <img src={bus_icon} alt="busicon" className="bus-icon" />
          Bus Connect
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            {/* <Nav.Link href="#/">Home</Nav.Link>
            <Nav.Link href="/other">Other</Nav.Link>
            <Nav.Link href="/other">Other</Nav.Link> */}
          </Nav>
          <Nav>
            <Nav.Link href="/home">Home</Nav.Link>
            <Nav.Link href="/schedule-list">Schedules</Nav.Link>
            <Nav.Link href="/myBookings">My Bookings</Nav.Link>
            <Nav.Link href="/bus-list">Buses</Nav.Link>
            <NavDropdown title="Maintenance" id="basic-nav-dropdown">
              <NavDropdown.Item href="/add-schedule">
                Add Schedule
              </NavDropdown.Item>
              <NavDropdown.Item href="/add-bus">Add Bus</NavDropdown.Item>
            </NavDropdown>
            <Button style={{ height: "35px" }} variant="outline-dark" href="/">
              <LogoutButton />
            </Button>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavbarComp;
