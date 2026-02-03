import './App.css'
import {Navbar, Menu, ProductCatalog, SearchProducts, Home, ProductDetails, Footer, LoginPage, UserProfile, DaneDoZamowien, UserCreateAccount, CartPartOne, CartPartTwo, Wishlist, AdminDashboard} from "./utils/"
import { Routes, Route, useParams } from "react-router-dom";
import { useEffect } from "react";
import { getSessionId } from "./utils/trackInteraction";

function App() {

  useEffect(() => {
    getSessionId(); // Wygeneruje UUID jeśli nie istnieje
  }, [])

  return (
    <>
      <Navbar />
      <Menu />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<UserCreateAccount />} />
        <Route path="/user" element={<UserProfile />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/dane-do-zamowien" element={<DaneDoZamowien />} />
        <Route path="/" element={<Home />} />
        <Route path="/cart" element={<CartPartOne />} />
        <Route path="/cart/delivery-payment-address" element={<CartPartTwo />} />
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
  return <ProductCatalog categorySlug={categorySlug} />;
}

export default App;
