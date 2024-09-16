// src/components/Sidebar.js
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Sidebar.css"; // Import the custom CSS

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false); // State to track sidebar visibility
  const navigate = useNavigate();

  const handleSignOut = () => {
    navigate("/");
  };

  const toggleSidebar = () => {
    setIsOpen(!isOpen); // Toggle sidebar open/close
  };

  return (
    <>
      {/* Toggle button (visible at all times) */}
      <button className="sidebar-toggle" onClick={toggleSidebar}>
        ☰
      </button>

      {/* Sidebar */}
      <div
        className={`sidebar ${isOpen ? "sidebar-open" : "sidebar-collapsed"}`}
      >
        <h2>{isOpen ? "My App" : ""}</h2>
        <ul>
          <li>
            <Link to="/dashboard">Dashboard</Link>
          </li>
          <li>
            <Link to="/expenses">Expenses</Link>
          </li>
          <li>
            <Link to="/profile">Profile</Link>
          </li>
          <li>
            <button className="signout" onClick={handleSignOut}>
              Sign Out
            </button>
          </li>
        </ul>
      </div>
    </>
  );
};

export default Sidebar;
