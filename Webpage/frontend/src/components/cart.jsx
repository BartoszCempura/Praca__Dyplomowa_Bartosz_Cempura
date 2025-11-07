import { useEffect, useState } from "react";
import ProductCard from "./productCard";
import api from "../api/tokenHandler";

function Cart() {
  const [products, setProducts] = useState([]);
  const [cartValue, setCartValue] = useState(0);

  useEffect(() => {
    const fetchCartProducts = async () => {
      try {
        const response = await api.get("/commerce/carts");
        setProducts(response.data.products || []);
        setCartValue(parseFloat(response.data.total_products_cost) || 0);
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
      <div className="flex flex-col gap-4 my-10 w-full pr-18">
        {products && products.length > 0 ? (
          products.map((p) => (
            <ProductCard
              key={p.id}          // id wpisu w koszyku
              id={p.product_id}   // id produktu z katalogu (ważne!)
              variant="cart"
              {...p}
            />
          ))
        ) : (
          <span>Brak produktów w koszyku</span>
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
