import { useEffect, useState} from "react";
import { getTopProducts } from "../utils/topProductsActions"
import ProductCard from "./productCard";

function Bestseller() {
  const [product, setProduct] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      setIsLoading(true);
      setError(null);
      try {
        const data = await getTopProducts();
        setProduct(data.mostPurchased || null);
      } catch (err) {
        setError(err);
      } finally {
        setIsLoading(false);
      }
    }
    load();
  }, []);

  if (isLoading) {
    return (
      <div className="flex flex-col justify-center items-center">
          <span className="loading loading-bars loading-lg text-primary"></span>
          <p className="text-gray-500">Please wait...</p>
      </div>
    );
  }

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

  if (!product) {
    return (
      <div className="text-center py-10">
        <p className="text-gray-500">Brak zarejestrowanych interakcji.</p>
      </div>
    );
  }

  return (
    <div className="bg-base-100 p-4 text-center">
      <h1 className="text-4xl font-bold bg-[linear-gradient(to_right,#06b6d4_0%,#67e8f9_50%,#f59e0b_55%,#f59e0b_100%)] bg-clip-text text-transparent mb-10">Bestseller</h1>
      <div className="flex justify-center">
        <ProductCard id={product.id} variant="bestseller" {...product} />
      </div>
    </div>

  );
}

export default Bestseller;
