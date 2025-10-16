import './App.css'
import {Navbar, Menu, PrintProducts, SearchProducts, Home, ProductDetails, Footer} from "./components/"
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
        <Route path="/search" element={<SearchProducts />} />
      </Routes>
      <Footer />
    </>
  );
}

function ProductsBasedOnURL() {
  const { categorySlug } = useParams();
  return <PrintProducts categorySlug={categorySlug} />;
}

export default App;
