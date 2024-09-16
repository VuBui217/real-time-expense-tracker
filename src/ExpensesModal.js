// src/components/ExpensesModal.js
import React, { useState } from "react";
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    const expenseData = {
      amount,
      description,
      category, // Include the selected category
    };

    if (transaction) {
      // Update transaction
      await axios.put(
        `http://127.0.0.1:5000/expenses/${transaction.id}`,
        expenseData
      );
    } else {
      // Create new transaction
      await axios.post("http://127.0.0.1:5000/expenses", expenseData);
    }

    onSave(); // Call parent function to refresh transaction list
    onRequestClose(); // Close modal
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
