// App.js
import React, { useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import "./App.css";
import NavbarComp from "./Components/Navbar/Navbar";
import LoginSignup from "./Components/LoginSignup/LoginSignup";
import Footer from "./Components/Footer";
import Home from "./Components/Home";
import Booking from "./Components/BookSearch";
import ScheduleList from "./Components/ScheduleList";
import AddScheduleForm from "./Components/AddScheduleForm";
import SearchResults from "./Components/SearchResults";
import MyBookings from "./Components/MyBookings";
import AddBusForm from "./Components/AddBusForm";
import BusList from "./Components/BusList";

function App() {
  const navigate = useNavigate();
  const [searchDeparture, setSearchDeparture] = useState("");
  const [searchArrival, setSearchArrival] = useState("");

  const handleSearch = (departure, arrival) => {
    setSearchDeparture(departure);
    setSearchArrival(arrival);
  };

  const isLoginSignupRoute = window.location.pathname === "/";
  const renderNavbar = !isLoginSignupRoute && <NavbarComp />;

  return (
    <div id="page-wrapper" className="App">
      {renderNavbar}
      <div id="main-content">
        <Routes>
          <Route exact path="/" element={<LoginSignup />} />
          <Route path="/home" element={<Home />} />
          <Route
            path="/booking"
            element={<Booking onSearch={handleSearch} />}
          />
          <Route
            path="/schedule-list"
            element={
              <ScheduleList
                searchDeparture={searchDeparture}
                searchArrival={searchArrival}
              />
            }
          />
          <Route path="/add-schedule" element={<AddScheduleForm />} />
          <Route
            path="/search-results"
            element={
              <SearchResults
                searchDeparture={searchDeparture}
                searchArrival={searchArrival}
              />
            }
          />
          <Route path="/myBookings" element={<MyBookings />} />
          <Route path="/add-bus" element={<AddBusForm />} />
          <Route path="/bus-list" element={<BusList />} />
        </Routes>
      </div>
      <Footer />
    </div>
  );
}

export default App;
