import './App.css'
import {Navbar, Menu, PrintProducts, SearchProducts, Home, ProductDetails, Footer, LoginPage} from "./components/"
import { Routes, Route, useParams } from "react-router-dom";

function App() {
  return (
    <>
      <Navbar />
      <Menu />
      <Routes>
         <Route path="/login" element={<LoginPage />} />
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
