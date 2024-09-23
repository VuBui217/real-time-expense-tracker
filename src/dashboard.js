// src/components/Dashboard.js
import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import Sidebar from "./Sidebar";
import "./dashboard.css";

const Dashboard = () => {
  const [totalSum, setTotalSum] = useState(0); // State to store total expenses
  const [expenses, setExpenses] = useState([]); // Optional: If you want to display individual expenses

  // Helper function to get the token from localStorage
  const getToken = () => {
    return localStorage.getItem("token");
  };

  // Fetch expenses data
  const fetchExpensesData = useCallback(async () => {
    const token = getToken();
    if (!token) {
      alert("No token found. Please log in.");
      return;
    }

    try {
      const response = await axios.get("http://127.0.0.1:5000/auth/expenses", {
        headers: {
          Authorization: `Bearer ${token}`, // Include token in the request
        },
      });

      setExpenses(response.data.Data); // Set the list of expenses if needed
      setTotalSum(response.data.sum);   // Set the total sum from the response
    } catch (error) {
      console.error("Error fetching expenses:", error);
      alert("Failed to fetch expenses data. Please try again.");
    }
  }, []); // Use useCallback to memoize fetchExpensesData

  // Fetch data when component mounts
  useEffect(() => {
    fetchExpensesData();
  }, [fetchExpensesData]); // Add fetchExpensesData as a dependency

  return (
    <div className="dashboard-container">
      <Sidebar />
      <div className="content">
        <h2>Dashboard</h2>
        <p>This is the dashboard where you'll see the summary of your financials.</p>

        {/* Display Total Expenses */}
        <div className="total-expenses">
          <h3>Total Expenses: ${totalSum}</h3> {/* Display the total sum here */}
        </div>

        {/* Optional: Display list of expenses */}
        <div className="expenses-list">
          <h3>All Expenses</h3>
          <ul>
            {expenses.map((expense) => (
              <li key={expense.id}>
                {expense.description} - ${expense.amount}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;


