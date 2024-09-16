// src/components/Expenses.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import ExpensesModal from "./ExpensesModal";
import Sidebar from "./Sidebar";
import "./expenses.css";
const Expenses = () => {
  const [expenses, setExpenses] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTransaction, setSelectedTransaction] = useState(null);

  useEffect(() => {
    fetchExpenses();
  }, []);

  const fetchExpenses = async () => {
    const response = await axios.get("http://127.0.0.1:5000/expenses");
    setExpenses(response.data);
  };

  const handleAddClick = () => {
    setSelectedTransaction(null); // Reset selected transaction
    setIsModalOpen(true); // Open modal for adding
  };

  const handleEditClick = (transaction) => {
    setSelectedTransaction(transaction); // Set the selected transaction for editing
    setIsModalOpen(true); // Open modal for editing
  };

  const handleDeleteClick = async (transactionId) => {
    await axios.delete(`http://127.0.0.1:5000/expenses/${transactionId}`);
    fetchExpenses(); // Refresh list after deletion
  };

  return (
    <div className="expenses-container">
      <Sidebar />
      <div className="content">
        <h2>Expenses</h2>
        <button onClick={handleAddClick}>Add Transaction</button>

        {/* Transaction List */}
        <div>
          <h3>All Transactions</h3>
          <ul>
            {expenses.map((expense) => (
              <li key={expense.id}>
                {expense.description} - ${expense.amount}{" "}
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
        onSave={fetchExpenses} // Refresh list after save
      />
    </div>
  );
};

export default Expenses;
