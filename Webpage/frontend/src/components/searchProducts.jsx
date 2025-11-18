import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import ProductCard from "./productCard";
import api from "../api/tokenHandler";

function SearchProducts() {
  const [searchParams] = useSearchParams();
  const searchValue = searchParams.get("search") || "";
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchSearchResults = async () => {
      try {
        const response = await api.get(`/catalog/products?search=${searchValue}`);
        setProducts(response.data.products);
      } catch (err) {
        console.error("Ups nie udało się pobrać produktów:", err);
      }
    };

    if (searchValue.trim()) {
      fetchSearchResults();
    }
  }, [searchValue]);

  return (
    <div className="flex flex-col items-center my-10">
        <h2 className="text-2xl font-bold mb-8">
          Wyniki wyszukiwania dla: <span className="text-primary">{searchValue} ({products.length})</span>
        </h2>
      <div className="flex flex-wrap justify-center gap-4">
        {products.length > 0 ? (
          products.map((p) => <ProductCard key={p.slug} variant="catalog" {...p} />)
        ) : (
          <div className="flex flex-col items-center gap-4">
            <div>
              <ul className="list-disc pl-5">
                <li>Sprawdź czy nie ma literówek</li>
                <li>Użyj ogólniejszych słów</li>
                <li>Skróć tekst</li>
              </ul>
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

export default SearchProducts;
