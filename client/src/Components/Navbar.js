import React from "react";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import "./Navbar.css";
import LogoutButton from "../Logout";

function Navbar() {
  return (
    <Navbar collapseOnSelect expand="lg" className="custom-navbar">
      <Container>
        <Navbar.Brand href="/">Bus Connect</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="#/">Home</Nav.Link>
            <Nav.Link href="/other">Other</Nav.Link>
            <Nav.Link href="/other">Other</Nav.Link>
          </Nav>
          <Nav>
            <Button style={{ height: "50px" }} variant="outline-dark" href="/">
              <LogoutButton />
            </Button>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Navbar;
