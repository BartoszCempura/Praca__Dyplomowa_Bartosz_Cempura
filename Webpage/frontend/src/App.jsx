import './App.css'
import {Navbar, Menu, Products, Home, ProductDetails} from "./components/"
import { Routes, Route, useParams } from "react-router-dom";

function App() {
  return (
    <>
      <Navbar />
      <Menu />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/:categorySlug" element={<ProductsBasedOnURL />} />
        <Route path="/:categorySlug/:productSlug" element={<ProductDetails />} />
      </Routes>
    </>
  );
}

function ProductsBasedOnURL() {
  const { categorySlug } = useParams();
  return <Products categorySlug={categorySlug} />;
}

export default App;
