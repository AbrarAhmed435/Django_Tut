// Import required modules and hooks
import { Navigate } from "react-router-dom"; // For redirecting unauthenticated users
import { jwtDecode } from "jwt-decode"; // To decode JWT and read expiration time
import api from "../api"; // Custom Axios instance with auth interceptor
import { REFRESH_TOKEN, ACCESS_TOKEN } from "../constant"; // Local storage keys
import { useState, useEffect } from "react"; // React state and lifecycle hook

function ProtectedRoute({ children }) {
  // State to track if the user is authorized (true/false/null)
  const [isAuthorized, setIsAuthorized] = useState(null);

  // useEffect to run authentication logic once when the component mounts
  useEffect(() => {
    auth().catch(() => setIsAuthorized(false)); // If auth() fails, set to false
  }, []);

  // Function to refresh the access token using the refresh token
  const refreshToken = async () => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN); // Get refresh token from localStorage
    try {
      const res = await api.post("/api/token/refresh/", {
        refresh: refreshToken,
      });
      if (res.status === 200) {
        // Store the new access token in localStorage
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        setIsAuthorized(true); // Mark user as authorized
      } else {
        setIsAuthorized(false); // If response isn't 200, fail auth
      }
    } catch {
      console.log(error); // Log any error
      setIsAuthorized(false); // Mark user as unauthorized
    }
  };

  // Main function to validate access token or trigger refresh
  const auth = async () => {
    const token = localStorage.getItem(ACCESS_TOKEN); // Get access token
    if (!token) {
      setIsAuthorized(false); // No token means unauthorized
      return;
    }
    const decoded = jwtDecode(token); // Decode token to extract `exp`
    const tokenExpiration = decoded.exp; // Expiry timestamp in seconds
    const now = Date.now() / 1000; // Current time in seconds

    if (tokenExpiration < now) {
      // Token expired, try to refresh
      await refreshToken();
    } else {
      setIsAuthorized(true); // Token valid, allow access
    }
  };

  // While auth is being checked, show loading
  if (isAuthorized === null) {
    return <div>Loading...</div>;
  }

  // If authorized, render child components; otherwise, redirect to login
  return isAuthorized ? children : <Navigate to="/login" />;
}

export default ProtectedRoute;
