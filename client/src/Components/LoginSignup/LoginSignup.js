import React, { useEffect, useState } from "react";
import "./LoginSignup.css";
import { useNavigate } from "react-router-dom";

export const checkLoginStatus = (setIsLoggedIn) => {
  const userIsLoggedIn = true;
  setIsLoggedIn(userIsLoggedIn);
};

function LoginSignup() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [action, setAction] = useState("Sign Up");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  //resets form by clearing the fields
  const resetForm = () => {
    setName("");
    setEmail("");
    setPassword("");
  };
  //Signup
  const Signup = async () => {
    try {
      const response = await fetch("http://localhost:5000/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: name,
          email,
          password,
        }),
        mode: "cors",
        credentials: "include", // Ensure credentials are included
      });

      const data = await response.json();
      if (response.ok) {
        setMessage("Signup successful! Redirecting to login...");
        console.log("Signup successful:", data);
        resetForm();
        Login();
      } else {
        setMessage(`Signup failed: ${data.error}`);
        console.error("Signup error:", data.error);
        setTimeout(() => {
          setMessage(null);
          setPassword("");
        }, 2000);
      }
    } catch (error) {
      console.error("Error during signup:", error);
    }
  };

  //Login

  const Login = async () => {
    try {
      const response = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (response.ok) {
        console.log("login successful:", data);
        setIsLoggedIn(true);
        setMessage("Login successful! Redirecting...");
        setTimeout(() => {
          navigate("/home");
        }, 2000);
      } else {
        setMessage(`Login failed: ${data.error}`);
        console.error("Login error:", data.error);
        setTimeout(() => {
          setMessage(null);
          setPassword("");
        }, 2000);
      }
    } catch (error) {
      console.error("Error during login", error);
    }
  };

  return (
    <div className="login-signup-container">
      <div className="header">
        <h5
          style={{
            fontSize: "34px",
            color: "#d1c23a",
            fontWeight: "bold",
            marginTop: "15px",
          }}
        >
          Bus Connect
        </h5>
        <div className="text">{action}</div>
        <div className="underline"></div>
      </div>
      <div className="inputs">
        {action === "Login" ? null : (
          <div className="input">
            <p className="req">*</p>
            <input
              type="text"
              placeholder="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
        )}
        <div className="input">
          <p className="req">*</p>
          <input
            type="email"
            placeholder="Email: doe@gmail.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="input">
          <p className="req">*</p>
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password: Characters(Aa1)8 "
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <span
            className="password-toggle"
            onClick={() => setShowPassword(!showPassword)}
          ></span>
        </div>
      </div>
      <div className="message" style={{ color: "green", fontWeight: "bold" }}>
        {message}
      </div>

      <div className="submit-container">
        <div
          className={action === "Login" ? "submit gray" : "submit"}
          onClick={() => {
            setAction("Create an Account");
            Signup();
          }}
        >
          Sign Up
        </div>
        <div
          className={action === "Create an Account" ? "submit gray" : "submit"}
          onClick={() => {
            setAction("Login");
            Login();
          }}
        >
          Login
        </div>
      </div>
    </div>
  );
}

export default LoginSignup;
