import React from "react";
import { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";
import Notes from "./pages/Notes";
import HomeNavbar from "./HomeNavbar";
import CreateNote from "./pages/CreateNote";
import PostNav from "./PostNav";
import { Logout } from "./PostNav";
import Footer from "./Footer";


function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />      
        <Route path="/logout" element={<Logout />} />      
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route element ={<HomeNavbar/>} >
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        
        <Route path='/createNote' element ={<CreateNote/>} />
        
         <Route
        path="/notes"
        element={
          <ProtectedRoute>
            <Notes />
          </ProtectedRoute>
        }
      />
       
        </Route>
         <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
    <Footer/>
    </>
  );
}

export default App;
