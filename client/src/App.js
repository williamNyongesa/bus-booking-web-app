// import logo from "./logo.svg";
import React from "react";
import { Routes, Route, Link, useNavigate } from "react-router-dom";
import "./App.css";
import NavbarComp from "./Components/Navbar/Navbar";
import LoginSignup from "./Components/LoginSignup/LoginSignup";
import Footer from "./Components/Footer";
import Home from "./Components/Home";

function App() {
  const navigate = useNavigate();
  const isLoginSignupRoute = window.location.pathname === "/";
  const renderNavbar = !isLoginSignupRoute && <NavbarComp />;

  return (
    <div id="page-wrapper" className="App">
      {/* {renderNavbar}  uncomment once endpoint correctly connected with backend */}
      <div id="main-content">
        <NavbarComp />
        <Routes>
          <Route exact path="/" element={<LoginSignup />} />
          <Route path="/home" element={<Home />} />
        </Routes>
      </div>
      <Footer />
    </div>
  );
}

export default App;
