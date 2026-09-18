import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Home from "./pages/home";
import Login from "./pages/login";
import { useAuth } from "./context/AuthContext";
import "./App.css";

function ProtectedRoute({ children }) {
  const { user, isLoading } = useAuth();
  if (isLoading) return <div className="route-loading">Loading workspace...</div>;
  return user ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;