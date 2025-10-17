import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import ProductCard from "./productCard";
import axios from "axios";

function SearchProducts() {
  const [searchParams] = useSearchParams();
  const searchValue = searchParams.get("search") || "";
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchSearchResults = async () => {
      try {
        const response = await axios.get(`/api/catalog/products?search=${searchValue}`);
        setProducts(response.data.products);
      } catch (err) {
        console.error("Error fetching search results:", err);
      }
    };

    if (searchValue.trim()) {
      fetchSearchResults();
    }
  }, [searchValue]);

  return (
    <div className="flex flex-col items-center mt-8">
        <h2 className="text-2xl font-bold mb-8">
          Wyniki wyszukiwania dla: <span className="text-primary">{searchValue} ({products.length})</span>
        </h2>
      <div className="flex flex-wrap justify-center gap-4">
        {products.length > 0 ? (
          products.map((p) => <ProductCard key={p.slug} {...p} />)
        ) : (
          <span className="text-gray-400 italic">Brak wyników</span>
        )}
      </div>
    </div>
  );
}

export default SearchProducts;
