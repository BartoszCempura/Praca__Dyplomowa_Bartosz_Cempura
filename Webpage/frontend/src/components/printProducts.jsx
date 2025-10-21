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

  return products.length > 0 ? (
    <div className="grid grid-cols-[1fr_4fr] gap-6">
      <aside className="bg-base-200 p-4">
        <h2 className="font-bold mb-2">Filtry</h2>
      </aside>
      <div className="flex flex-wrap justify-center gap-6 my-10">
        {products.map((p) => (
          <ProductCard key={p.id} categorySlug={categorySlug} {...p} />
        ))}
      </div>
    </div>
  ) : (
    <div className="flex justify-center items-center my-10">
      <span className="text-gray-400 italic text-lg">No products found</span>
    </div>
  );
}

export default PrintProducts;
