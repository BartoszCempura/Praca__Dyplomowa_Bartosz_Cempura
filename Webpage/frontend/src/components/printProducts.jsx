import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import axios from "axios";
import ProductCard from "./productCard";

function PrintProducts({ categorySlug }) {
  const [products, setProducts] = useState([]);
  const [attributes, setAttributes] = useState({});
  const [searchParams, setSearchParams] = useSearchParams();

  // 🔹 1️⃣ Pobierz dostępne atrybuty dla kategorii
  useEffect(() => {
    const fetchAttributes = async () => {
      try {
        const res = await axios.get(`/api/catalog/attributes/${categorySlug}`);
        setAttributes(res.data);
      } catch (err) {
        console.error("Unable to fetch attributes:", err);
      }
    };
    fetchAttributes();
  }, [categorySlug]);

  // 🔹 2️⃣ Pobierz produkty z uwzględnieniem filtrów z URL
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const queryString = searchParams.toString();
        const url = `/api/catalog/products/${categorySlug}?${queryString}`;
        const res = await axios.get(url);
        setProducts(res.data.products);
      } catch (err) {
        console.error("Unable to get products:", err);
      }
    };
    fetchProducts();
  }, [categorySlug, searchParams]);

  // 🔹 3️⃣ Zmiana checkboxa → aktualizacja URL (czyli searchParams)
const handleCheckboxChange = (attrName, value) => {
  const currentValues = searchParams.getAll(attrName);

  if (currentValues.includes(value)) {
    // odznaczenie → usuń
    searchParams.delete(attrName);
  } else {
    // zaznaczenie → nadpisz poprzednią wartość, żeby tylko jedna była aktywna
    searchParams.delete(attrName);
    searchParams.set(attrName, value);
  }

  // reset paginacji przy zmianie filtrów
  searchParams.delete("page");
  setSearchParams(searchParams);
};

  // 🔹 4️⃣ Render
  return (
    <div className="grid grid-cols-[1fr_4fr] gap-6 items-start">
      <aside className="bg-base-200 p-4 pl-10 max-h-screen overflow-y-auto sticky top-0">
        <h2 className="font-bold mb-2 text-lg">Filtry</h2>

        {/* Gdy są atrybuty */}
        {Object.keys(attributes).length > 0 ? (
          Object.keys(attributes).map(attrName => (
            <details key={attrName} className="mb-3">
              <summary className="cursor-pointer font-medium capitalize">
                {attrName}
              </summary>
              <ul className="menu dropdown-content bg-base-100 rounded-box w-60 p-2 shadow-sm ml-4 mt-2">
                {Object.entries(attributes[attrName]).map(([value, count]) => {
                  const isChecked = searchParams.getAll(attrName).includes(value);
                  return (
                    <li key={value} className="flex flex-row items-center gap-2">
                      <input
                        type="checkbox"
                        className="checkbox checkbox-sm"
                        checked={isChecked}
                        onChange={() => handleCheckboxChange(attrName, value)}
                      />
                      <span className="whitespace-nowrap">
                        {value} ({count})
                      </span>
                    </li>
                  );
                })}
              </ul>
            </details>
          ))
        ) : (
          <p className="text-gray-500 text-sm italic">Brak filtrów</p>
        )}
      </aside>

      {/* Produkty */}
      <div className="flex flex-wrap justify-center gap-6 my-10">
        {products.length > 0 ? (
          products.map(p => (
            <ProductCard key={p.id} categorySlug={categorySlug} {...p} />
          ))
        ) : (
          <span className="text-gray-400 italic text-lg">
            Brak produktów spełniających kryteria
          </span>
        )}
      </div>
    </div>
  );
}

export default PrintProducts;
