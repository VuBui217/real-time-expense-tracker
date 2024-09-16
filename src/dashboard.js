// src/components/Dashboard.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import Sidebar from "./Sidebar";
import "./dashboard.css";
const Dashboard = () => {
  return (
    <div className="dashboard-container">
      <Sidebar />
      <div className="content">
        <h2>Dashboard</h2>
        {/* Dashboard content goes here */}
        <p>
          This is the dashboard where you'll see the summary of your financials.
        </p>
      </div>
    </div>
  );
};

export default Dashboard;
