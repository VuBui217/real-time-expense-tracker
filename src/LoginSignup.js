import React, { useState } from "react";
import "./LoginSignup.css";
import user_icon from "./Assets/person.png";
import password_icon from "./Assets/password.png";
import email_icon from "./Assets/email.png";
import axios from "axios";

const LoginSignup = () => {
  const [action, setAction] = useState("Login");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setloading] = useState(false);
  // Validate email
  const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };
  // Validate form inputs
  const validateForm = () => {
    if (!email || !password || (action === "Sign Up" && !username)) {
      alert("Please fill in all required fill.");
      return false;
    }
    if (!isValidEmail(email)) {
      alert("Please enter a valid email address.");
      return false;
    }
    return true;
  };
  // Reset form fields
  const resetForm = () => {
    setUsername("");
    setEmail("");
    setPassword("");
  };

  // Handle action 'Login' and 'Sign Up'
  const handleAction = async () => {
    if (!validateForm()) return;
    setloading(true);
    if (action === "Login") {
      try {
        //   console.log({ email, password });
        const response = await axios.post("http://127.0.0.1:5000/auth/signin", {
          email,
          password,
        });
        resetForm(); // Reset form after login
      } catch (error) {
        alert("Error: " + error.response.data.message);
      }
    } else {
      try {
        // console.log({ username, email, password });
        const response = await axios.post("http://127.0.0.1:5000/auth/signup", {
          username,
          email,
          password,
        });
        alert("User created successfully");
        resetForm(); // Reset form after signup
      } catch (error) {
        alert("Error: " + error.response.data.message);
      } finally {
        setloading(false);
      }
    }
  };
  return (
    <div className="container">
      <div className="header">
        <div className="text">{action}</div>
        <div className="underline"></div>
      </div>
      <div className="submit-container">
        <div
          className={action === "Login" ? "submit gray" : "submit"}
          onClick={() => {
            setAction("Sign Up");
          }}
        >
          Sign Up
        </div>
        <div
          className={action === "Sign Up" ? "submit gray" : "submit"}
          onClick={() => {
            setAction("Login");
          }}
        >
          Login
        </div>
      </div>
      <div className="inputs">
        {action === "Login" ? (
          <div></div>
        ) : (
          <div className="input">
            <img src={user_icon} alt="" />
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
        )}

        <div className="input">
          <img src={email_icon} alt="" />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="input">
          <img src={password_icon} alt="" />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
      </div>
      {action === "Sign Up" ? (
        <div></div>
      ) : (
        <div className="forgot-password">
          Forgot Password? <span>Click Here</span>
        </div>
      )}
      <button
        type="button"
        className="submit-button"
        onClick={handleAction}
        disabled={loading}
      >
        {loading ? "Submitting..." : "Submit"}
      </button>
    </div>
  );
};

export default LoginSignup;
