// import logo from "./logo.svg";
import React, { useState } from "react";
import { Routes, Route, Link, useNavigate } from "react-router-dom";
import "./App.css";
import NavbarComp from "./Components/Navbar/Navbar";
import LoginSignup from "./Components/LoginSignup/LoginSignup";
import Footer from "./Components/Footer";
import Home from "./Components/Home";
import Booking from "./Components/BookSearch";
import ScheduleList from "./Components/ScheduleList";
import AddScheduleForm from "./Components/AddScheduleForm";

function App() {
  const navigate = useNavigate();
  const [schedules, setSchedules] = useState([]);

  const handleAddSchedule = (addedSchedule) => {
    setSchedules((prevSchedules) => [...prevSchedules, addedSchedule]);
  };
  const isLoginSignupRoute = window.location.pathname === "/";
  const renderNavbar = !isLoginSignupRoute && <NavbarComp />;

  return (
    <div id="page-wrapper" className="App">
      {/*uncomment once endpoint correctly connected with backend*/}
      {renderNavbar}
      <div id="main-content">
        {/* <NavbarComp /> */}
        <Routes>
          <Route exact path="/" element={<LoginSignup />} />
          <Route path="/home" element={<Home />} />
          <Route path="/booking" element={<Booking />} />
          <Route
            path="/schedule-list"
            element={<ScheduleList schedules={schedules} />}
          />
          <Route
            path="/add-schedule"
            element={<AddScheduleForm onAddSchedule={handleAddSchedule} />}
          />
        </Routes>
      </div>
      <Footer />
    </div>
  );
}

export default App;
