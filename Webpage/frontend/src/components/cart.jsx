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
        setProducts(response.data.products || []); // zabezpieczenie
        setCartValue(parseFloat(response.data.total_products_cost) || 0);
      } catch (err) {
        console.error("Błąd podczas pobierania koszyka:", err);
      }
    };

    fetchCartProducts();
  }, []);

  return (
    <div className="grid grid-cols-[4fr_1fr] gap-6 items-start">
      <div className="flex flex-col gap-4 my-10 w-full pl-24 pr-18">
        {products && products.length > 0 ? (
          products.map((p) => (
            <ProductCard key={p.id} variant="cart" {...p} />
          ))
        ) : (
          <span>Brak produktów w koszyku</span>
        )}
      </div>

      <aside className="bg-base-200 p-4 pl-10 max-h-screen overflow-y-auto sticky top-0 rounded-lg shadow">
        <div className="card-body">
              <span className="text-info mb-2">
                Wartość: {cartValue.toFixed(2)} zł
              </span>
              <div className="card-actions" onClick={() => navigate("")}>
                <button className="btn btn-custom btn-block">Przejdź dalej</button>
              </div>
            </div>
      </aside>
    </div>
  );
}

export default Cart;
