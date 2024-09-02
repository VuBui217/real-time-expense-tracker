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

  // Handle action 'Login' and 'Sign Up'
  const handleAction = async () => {
    if (action === "Login") {
      try {
        const response = await axios.post("http://127.0.0.1:5000/login", {
          email,
          password,
        });
      } catch (error) {
        alert("Error: " + error.response.data.message);
      }
    } else {
      try {
        const response = await axios.post("http://127.0.0.1:5000/signup", {
          username,
          email,
          password,
        });
        alert("User created successfully");
      } catch (error) {
        alert("Error: " + error.response.data.message);
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
      <button type="button" className="submit-button" onClick={handleAction}>
        Submit
      </button>
    </div>
  );
};

export default LoginSignup;
