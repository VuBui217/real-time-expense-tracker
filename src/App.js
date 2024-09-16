// App.js
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoginSignup from "./LoginSignup";
import Dashboard from "./dashboard";
import Expenses from "./expenses"; // Import the Expenses component

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginSignup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/expenses" element={<Expenses />} />{" "}
        {/* Add the Expenses route */}
      </Routes>
    </Router>
  );
}

export default App;
