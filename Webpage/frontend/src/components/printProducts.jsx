import { useEffect, useState } from "react";
import axios from "axios";
import ProductCard from "./productCard";


function PrintProducts({ categorySlug }) {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const getProducts = async () => {
      try {
        const productsFromCategory = await axios.get(`/api/catalog/products/${categorySlug}`);
        setProducts(productsFromCategory.data.products); // pisownia pozwala na dostęp do tablicy produktów
      } catch (err) {
        console.error("Unable to get products:", err);
      }
    };

    getProducts();
  }, [categorySlug]);

  return (
    <div className="flex flex-wrap justify-center gap-6 mt-10">
      {products.length > 0 ? (
        products.map((p) => <ProductCard key={p.id} categorySlug={categorySlug} {...p} />)
      ) : (
        <span className="text-gray-400 italic">No products found</span>
      )}
    </div>
  );
}

export default PrintProducts;
