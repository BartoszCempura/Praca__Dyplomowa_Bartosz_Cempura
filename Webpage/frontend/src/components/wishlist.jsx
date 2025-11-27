import { useState, useEffect } from "react";
import ProductCard from "./productCard";
import { getWishlist } from "../utils/wishlistActions";

function Wishlist() {
  const [products, setProducts] = useState([]);

  const fetchProducts = async () => {
    const data = await getWishlist();
    setProducts(data);
  };

  useEffect(() => {
    fetchProducts();

    const handler = () => fetchProducts();
    window.addEventListener("wishlistChange", handler);

    return () => window.removeEventListener("wishlistChange", handler);
  }, []);

  return (
    <div className="flex flex-col items-center my-10">
      <h2 className="text-2xl font-bold mb-8">
        Wishlist
      </h2>
      <div className="flex flex-wrap justify-center gap-4">
        {products.length > 0 ? (
          products.map((p) => <ProductCard key={p.id} variant="catalog" {...p} />)
        ) : (
          <div className="flex flex-col items-center gap-4">
            <div>
              <p>Brak produktów na liście życzeń. Spróbuj dodać jakieś produkty!</p>
            </div>

            <div className="bg-base-100 p-4 text-center shadow-md">
              <h1 className="text-4xl font-bold">Top produkty tego miesiąca</h1>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Wishlist;
