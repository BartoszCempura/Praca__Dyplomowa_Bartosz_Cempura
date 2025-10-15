import { useState, useEffect } from 'react'
import './App.css'
import {Navbar, Menu, Products} from "./components/"
import axios from 'axios'
import { Routes, Route, useParams } from "react-router-dom";

function App() {
  return (
    <>
      <Navbar />
      <Menu />
      <Routes>
        <Route path="/:categorySlug" element={<ProductsBasedOnURL />} />
      </Routes>
    </>
  );
}

function ProductsBasedOnURL() {
  const { categorySlug } = useParams();
  return <Products categorySlug={categorySlug} />;
}

export default App;
