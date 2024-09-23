import React, { useState, useEffect } from "react";
import Modal from "react-modal";
import axios from "axios";
import "./ExpensesModal.css"; // Import the CSS file

Modal.setAppElement("#root"); // For accessibility

const ExpensesModal = ({ isOpen, onRequestClose, transaction, onSave }) => {
  const [amount, setAmount] = useState(transaction ? transaction.amount : "");
  const [description, setDescription] = useState(
    transaction ? transaction.description : ""
  );
  const [category, setCategory] = useState(
    transaction ? transaction.category : ""
  ); // Add category state

  // Update the form fields if the transaction changes
  useEffect(() => {
    if (transaction) {
      setAmount(transaction.amount);
      setDescription(transaction.description);
      setCategory(transaction.category);
    } else {
      setAmount("");
      setDescription("");
      setCategory("");
    }
  }, [transaction]);

  const handleSubmit = async (event) => {
    event.preventDefault();  // Prevent the form from refreshing the page
    
    const token = localStorage.getItem("token");  // Retrieve the token from localStorage
  
    if (!token) {
      alert("No token found. Please log in.");
      return;
    }
  
    // Construct the expense data from the form inputs
    const expenseData = {
      amount: parseFloat(amount),  // Ensure amount is a number
      description,
      category
    };
  
    console.log("Expense data to be sent:", expenseData);  // Debug print
  
    try {
      let response;
      if (transaction) {
        // Edit existing expense (PUT request)
        response = await axios.put(
          `http://127.0.0.1:5000/auth/expenses/${transaction.id}`, // Use transaction's id
          JSON.stringify(expenseData), // Send the expense data in JSON format
          {
            headers: {
              Authorization: `Bearer ${token}`,  // Include the token in the request
              'Content-Type': 'application/json' // Ensure the content type is set correctly
            }
          }
        );
        console.log("Expense updated successfully", response.data);  // Success response
        alert("Expense updated successfully");
      } else {
        // Add new expense (POST request)
        response = await axios.post(
          "http://127.0.0.1:5000/auth/expenses",
          JSON.stringify(expenseData),
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          }
        );
        console.log("Expense added successfully", response.data);  // Success response
        alert("Expense added successfully");
      }
  
      // Call the onSave function to refresh the expenses list
      if (onSave) onSave();
  
      // Close the modal after saving
      onRequestClose();
    } catch (error) {
      if (error.response) {
        console.error("Error response:", error.response);  // Log any errors from the response
        alert("Error: " + (error.response.data.Message || error.message));
      } else {
        console.error("Error request:", error);  // Log the request error
        alert("Error submitting expense. Please try again.");
      }
    }
  };
  
  

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      contentLabel="Transaction Modal"
      className="modal-content" // Add a class for styling the content
      overlayClassName="modal-overlay" // Overlay styling for better visibility
    >
      <h2>{transaction ? "Edit Transaction" : "Add Expense"}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Amount</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Description</label>
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Category</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)} // Handle category selection
            required
          >
            <option value="">Select Category</option> {/* Placeholder */}
            <option value="Groceries">Groceries</option>
            <option value="Utilities">Utilities</option>
            <option value="Transportation">Transportation</option>
            <option value="Entertainment">Entertainment</option>
            <option value="Rent">Rent</option>
            <option value="Miscellaneous">Miscellaneous</option>
          </select>
        </div>
        <button type="submit">{transaction ? "Update" : "Add"} Expense</button>
      </form>
    </Modal>
  );
};

export default ExpensesModal;

