import React from "react";
import Button from "react-bootstrap/Button";
import bus_icon from "../Images/bus.png";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import "./Navbar.css";
// import LogoutButton from "../Logout";

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
            <Nav.Link href="#/">Home</Nav.Link>
            <Nav.Link href="/schedule">Schedule</Nav.Link>
            <Nav.Link href="/maintenance">Maintenance</Nav.Link>
            <Button style={{ height: "35px" }} variant="outline-dark" href="/">
              Logout
              {/* <LogoutButton /> */}
            </Button>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavbarComp;
