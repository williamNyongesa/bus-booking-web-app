// import logo from "./logo.svg";
import React, { useEffect } from "react";
import { Routes, Route, Link, useNavigate } from "react-router-dom";
import "./App.css";
import NavbarComp from "./Components/Navbar/Navbar";
import LoginSignup from "./Components/LoginSignup/LoginSignup";
import Footer from "./Components/Footer";
import Home from "./Components/Home";
import Booking from "./Components/BookSearch";
import ScheduleList from "./Components/ScheduleList";
import AddScheduleForm from "./Components/AddScheduleForm";
import DriverDashboard from "./Components/DriverDashboard";
import AdminDashboardComp from "./Components/AdminDashboard.js";
import { useState } from "react";
import { UserProvider, useUser } from "./Components/USerContext";
import { Navbar } from "react-bootstrap";

function App() {
  const navigate = useNavigate();
  const { user } = useUser();
  const [isuser, setIsuser] = useState(false)
  const [isdriver, setIsdriver] = useState(false)
  const [isadmin, setIsadmin] = useState(false)
  const [role, setRole]=useState('')


  const isLoginSignupRoute = window.location.pathname === "/";
  const renderNavbar = !isLoginSignupRoute && <NavbarComp isadmin={isadmin} isuser={isuser} isdriver={isdriver} role={role}  />;

  // State to hold the user role
  const [userRole, setUserRole] = useState(null);

  // Update user role when the user context changes
  useEffect(() => {
    if (user && user.role) {
      setUserRole(user.role);
    } else {
      setUserRole(null);
    }
  }, [user]);

  // Conditionally render the AddScheduleForm based on the user's role
  const renderAddScheduleForm = userRole === "admin" && (
    <Route path="/add-schedule" element={<AddScheduleForm />} />
  );
  return (
    <UserProvider>
      <div id="page-wrapper" className="App">
        {/*uncomment once endpoint correctly connected with backend*/}
        {renderNavbar}
        <div id="main-content">
          {/* <NavbarComp /> */}
          <Routes>
            <Route exact path="/" element={<LoginSignup isuser={isuser} isadmin={isadmin} setIsadmin={setIsadmin} setIsdriver={setIsdriver} setIsuser={setIsuser} isdriver={isdriver} role={role} setRole={setRole} />} />
            <Route path="/home" element={<Home isadmin={isadmin} isuser={isuser} isdriver={isdriver} role={role}  />} />
            <Route path="/booking" element={<Booking />} />
            <Route path="/schedule-list" element={<ScheduleList />} />
            <Route path="/add-schedule" element={<AddScheduleForm isdriver={isdriver} />} />
            {renderAddScheduleForm}
            <Route path="/admin-dashboard" element={<AdminDashboardComp />} />
            <Route path="/driver-dashboard" element={<DriverDashboard/>} />
          </Routes>
        </div>
        <Footer />
      </div>
    </UserProvider>
  );
}

export default App;
