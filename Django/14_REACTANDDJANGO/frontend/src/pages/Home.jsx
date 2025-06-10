import { useState, useEffect } from "react";
import api from "../api";
import HomeNavbar from "../HomeNavbar";
import { Routes,Route } from "react-router-dom";
import { Link } from "react-router-dom";
import Notes from "./Notes";
import PostNav from "../PostNav";

export default function Home() {
  
  return (
    <div>
    <PostNav/>
    </div>
  );
}
