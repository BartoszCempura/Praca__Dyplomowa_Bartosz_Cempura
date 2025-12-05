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
    <div className="container flex flex-col items-center my-10 h-[60vh] overflow-y-auto mx-auto">
      <h1 className="text-2xl font-bold mb-10">
        Ulubione produkty
      </h1>
      <div className="flex flex-wrap justify-center gap-6 mb-10">
        {products.length > 0 ? (
          products.map((p) => <ProductCard key={p.id} categorySlug={p.category_slug} variant="catalog" {...p} />)
        ) : (
          <div className="flex flex-col items-center gap-6">
            <div className="flex flex-col gap-2">
              <h1 className="font-semibold text-center">Twoja lista jest pusta!</h1>
              <p><span className=" text-yellow-500">Zainteresował</span> cię produkt i chcesz zachować go na później?</p>
              <p>Dodaj go do ulubionych, klikając ikonę <span className="text-yellow-500">serca</span> przy produkcie.</p>
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
