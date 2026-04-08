import { useState, useEffect } from "react";
import ProductCard from "./productCard";
import { getWishlist } from "../utils/wishlistActions";

function Wishlist() {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchProducts = async () => {
    try {
    setIsLoading(true);
    setError(null);
    const data = await getWishlist();
    setProducts(data);
    } catch (err) {
        setError(err);
        setProducts([]);
      } finally {
        setIsLoading(false);
      }
    };

  useEffect(() => {
    fetchProducts();

    const handler = () => fetchProducts();
    window.addEventListener("wishlistChange", handler);

    return () => window.removeEventListener("wishlistChange", handler);
  }, []);


  if (error) {
    return (
      <div className="text-center py-10">
        <p className="text-red-500">
          Error: {error?.message || "Nie udało się pobrać danych"}
        </p>
        <p className="text-red-500">
          Please refresh the page
        </p>
      </div>
    );
  }

  return (
    <div className="container flex flex-col items-center my-10 h-[60vh] overflow-y-auto mx-auto">
      <h1 className="text-2xl font-bold mb-10">
        Ulubione produkty
      </h1>
      <div className="flex flex-wrap justify-center gap-6 mb-10">
        {isLoading ? (
          <div className="flex flex-col justify-center items-center py-10">
            <span className="loading loading-bars loading-lg text-primary"></span>
            <p className="text-gray-500">Please wait...</p>
          </div>
        ) : products.length > 0 ? (
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
