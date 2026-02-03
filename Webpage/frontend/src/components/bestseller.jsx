import { useEffect, useState} from "react";
import { getTopProducts } from "../utils/topProductsActions"
import ProductCard from "./productCard";

function Bestseller() {
  const [product, setProduct] = useState(null);

  useEffect(() => {
    async function load() {
      const data = await getTopProducts();
      setProduct(data.mostPurchased || null);
    }
    load();
  }, []);

  if (!product) {
    return (
      <div className="text-center py-10">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  return (
      <div className="flex justify-center">
        <ProductCard id={product.id} variant="bestseller" {...product} />
      </div>
  );
}

export default Bestseller;
