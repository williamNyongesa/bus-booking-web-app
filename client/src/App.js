// import logo from "./logo.svg";
import React from "react";
import { Routes, Route, Link, useNavigate } from "react-router-dom";
import "./App.css";
import NavbarComp from "./Components/Navbar/Navbar";
import LoginSignup from "./Components/LoginSignup/LoginSignup";

function App() {
  const navigate = useNavigate();
  const isLoginSignupRoute = window.location.pathname === "/";
  const renderNavbar = !isLoginSignupRoute && <NavbarComp />;

  return (
    <div className="App">
      {renderNavbar}
      <NavbarComp />
      <Routes>
        <Route exact path="/" element={<LoginSignup />} />
      </Routes>
    </div>
  );
}

export default App;
