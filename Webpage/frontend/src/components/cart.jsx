import { useEffect, useState } from "react";
import ProductCard from "./productCard";
import api from "../api/tokenHandler";
import { getCart, saveCartSilent} from "./tempCartStorage";

function Cart() {
  const [products, setProducts] = useState([]);
  const [cartValue, setCartValue] = useState(0);

  useEffect(() => {
  const fetchCartProducts = async () => {
    try {
      const response = await api.get("/commerce/carts");
      const cartProducts = response.data.products || [];
      setProducts(cartProducts);
      

      if (cartProducts.length > 0) {
        const tempCart = getCart(); // pobieramy zmienną w local storrage

        const productIds = cartProducts.map(p => p.product_id).join(',');
        const response = await api.get(`/catalog/products?product_ids=${productIds}`);
        const productsData = response.data.products;

        // Aktualizacja tempCart - endpoint przyjmuje wiele id więc możemy zaktualizować wszystkie na raz - mniejsze obciążenie backendu
        productsData.forEach(productData => {
          const prev = tempCart[productData.id] || {};
          tempCart[productData.id] = {
            quantity_db: productData.quantity,
            quantity_user: prev.quantity_user || 1,
            price_including_promotion: productData.price_including_promotion,
          };
        });

        saveCartSilent(tempCart); // nie inicjujemy eventów za pomocą saveCart i tym samym backend nie wpada w pętle wywołań

        const total = Object.values(tempCart).reduce((sum, item) => {
          return sum + item.quantity_user * parseFloat(item.price_including_promotion);
        }, 0);

        setCartValue(total);
      } else {
        setCartValue(0);
      }

    } catch (err) {
      console.error("Błąd podczas pobierania koszyka:", err);
    }
  };

  fetchCartProducts();
  window.addEventListener("cartChange", fetchCartProducts);
  return () => window.removeEventListener("cartChange", fetchCartProducts);
}, []);

  return (
    <div className="grid grid-cols-[4fr_1fr] gap-6 items-start mx-28">
      <div className="flex flex-col items-center gap-4 my-10 w-full pr-18">
        {products && products.length > 0 ? (
          products.map((p) => (
            <ProductCard
              key={p.product_id}          // id wpisu w koszyku
              id={p.product_id}   // id produktu z katalogu (ważne!)
              variant="cart"
              {...p}
            />
          ))
        ) : (
          <span className="mt-15">Brak produktów w koszyku</span>
        )}
      </div>

      <aside className="bg-base-200 p-4 max-h-screen overflow-y-auto rounded-lg shadow-md my-10 border-1 border-gray-900">
        <div className="card-body">
          <span className="text-info mb-2">
            Wartość: {cartValue.toFixed(2)} zł
          </span>
          <div className="card-actions">
            <button className="btn btn-custom btn-block">Przejdź dalej</button>
          </div>
        </div>
      </aside>
    </div>
  );
}

export default Cart;
