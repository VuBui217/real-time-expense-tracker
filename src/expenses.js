import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import ExpensesModal from "./ExpensesModal";
import Sidebar from "./Sidebar";
import "./expenses.css";

const Expenses = () => {
  const [expenses, setExpenses] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTransaction, setSelectedTransaction] = useState(null);

  // Add state variables for form inputs
  const [amount, setAmount] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");

  // Helper function to get the token
  const getToken = () => {
    return localStorage.getItem("token");
  };

  // Fetch expenses with the token in the Authorization header
  const fetchExpenses = useCallback(async () => {
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
      setExpenses(response.data.Data); // Assuming your response contains the list of expenses in the "Data" field
    } catch (error) {
      console.error("Error fetching expenses:", error);
      alert("Failed to fetch expenses. Please try again.");
    }
  }, []); // Empty dependency array ensures this runs only once

  useEffect(() => {
    fetchExpenses();
  }, [fetchExpenses]); // Add fetchExpenses as a dependency

  const handleSaveExpense = async (event) => {
    if (!event) {
      console.error("Event object is undefined.");
      return;
    }
    event.preventDefault();  // Prevent the form from refreshing the page

    const token = localStorage.getItem("token");
    if (!token) {
      alert("No token found. Please log in.");
      return;
    }

    // Validate input data
    if (!amount || isNaN(amount) || !description || !category) {
      alert("Please fill in all fields with valid data.");
      return;
    }

    // Create the expenseData object
    const expenseData = {
      amount: parseFloat(amount),  // Ensure amount is a number
      description,
      category,
    };

    console.log("Expense data to be sent:", expenseData);  // Debug print

    try {
      let response;
      if (selectedTransaction) {
        // Edit existing expense (PUT request)
        response = await axios.put(
          `http://127.0.0.1:5000/auth/expenses/${selectedTransaction.id}`, // Use selectedTransaction's id
          JSON.stringify(expenseData), // Send the expense data in JSON format
          {
            headers: {
              Authorization: `Bearer ${token}`,  // Include the token in the request
              'Content-Type': 'application/json',  // Ensure the content type is set correctly
            },
          }
        );
        console.log("Expense updated successfully", response.data);
        alert("Expense updated successfully");
      } else {
        // Add new expense (POST request)
        response = await axios.post(
          "http://127.0.0.1:5000/auth/expenses",
          expenseData,  // Send the expense data directly
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          }
        );
        console.log("Expense added successfully", response.data);
        alert("Expense added successfully");
      }

      fetchExpenses(); // Refresh the expense list after adding/updating
      setIsModalOpen(false); // Close the modal
    } catch (error) {
      console.error("Error saving expense:", error);  // Log the error
      if (error.response) {
        console.error("Error response data:", error.response.data);  // Log the response data
        alert("Failed to save expense: " + (error.response.data.error || error.message));
      } else {
        alert("Failed to save expense. Please try again.");
      }
    }
  };

  // Handle adding a new expense (opens the modal)
  const handleAddClick = () => {
    setSelectedTransaction(null); // Reset selected transaction
    setAmount(""); // Reset amount input
    setDescription(""); // Reset description input
    setCategory(""); // Reset category input
    setIsModalOpen(true); // Open modal for adding
  };

  // Handle editing an expense (opens the modal with the selected transaction)
  const handleEditClick = (transaction) => {
    setSelectedTransaction(transaction); // Set the selected transaction for editing
    setAmount(transaction.amount); // Set the current amount for editing
    setDescription(transaction.description); // Set the current description for editing
    setCategory(transaction.category); // Set the current category for editing
    setIsModalOpen(true); // Open modal for editing
  };

  // Define the handleDeleteClick function
  const handleDeleteClick = async (expenseId) => {
    const token = getToken();
    if (!token) {
      alert("No token found. Please log in.");
      return;
    }

    try {
      await axios.delete(`http://127.0.0.1:5000/auth/expenses/${expenseId}`, {
        headers: {
          Authorization: `Bearer ${token}`, // Include the token in the request
        },
      });
      alert("Expense deleted successfully");
      fetchExpenses(); // Refresh the list after deletion
    } catch (error) {
      console.error("Error deleting expense:", error);
      alert("Failed to delete expense. Please try again.");
    }
  };

  return (
    <div className="expenses-container">
      <Sidebar />
      <div className="content">
        <h2>Expenses</h2>
        <button onClick={handleAddClick}>Add Expenses</button>

        {/* Transaction List */}
        <div>
          <h3>All Expenses</h3>
          <ul>
            {expenses.map((expense) => (
              <li key={expense.id}>
                {expense.description} - ${expense.amount} - {expense.category}{" "}
                <button onClick={() => handleEditClick(expense)}>Edit</button>{" "}
                <button onClick={() => handleDeleteClick(expense.id)}>
                  Delete
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
      {/* Modal for Adding/Editing Transaction */}
      <ExpensesModal
        isOpen={isModalOpen}
        onRequestClose={() => setIsModalOpen(false)}
        transaction={selectedTransaction}
        onSave={handleSaveExpense} // Pass the save function to the modal
        amount={amount}
        setAmount={setAmount}
        description={description}
        setDescription={setDescription}
        category={category}
        setCategory={setCategory}
      />
    </div>
  );
};

export default Expenses;

