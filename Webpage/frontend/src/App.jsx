import './App.css'
import {Navbar, Menu, PrintProducts, SearchProducts, Home, ProductDetails, Footer, LoginPage, UserProfile, UserCreateAccount, Cart, Wishlist} from "./utils/"
import { Routes, Route, useParams } from "react-router-dom";

function App() {
  return (
    <>
      <Navbar />
      <Menu />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<UserCreateAccount />} />
        <Route path="/user" element={<UserProfile />} />
        <Route path="/" element={<Home />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/wishlist" element={<Wishlist />} />
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
