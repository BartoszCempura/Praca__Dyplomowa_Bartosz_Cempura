import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import ProductCard from "./productCard";
import api from "../api/tokenHandler";

function ProductCatalog({ categorySlug }) {
  const [products, setProducts] = useState([]);
  const [attributes, setAttributes] = useState({});
  const [searchParams, setSearchParams] = useSearchParams();

// pobieranie atrybutów
  useEffect(() => {
    const fetchAttributes = async () => {
      try {
        const response = await api.get(`/catalog/attributes/${categorySlug}`);
        setAttributes(response.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchAttributes();
  }, [categorySlug]);

// pobieranie produktów na podstawie URL
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const queryString = searchParams.toString();
        const url = `/catalog/products/${categorySlug}?${queryString}`;
        const response = await api.get(url);
        setProducts(response.data.products);
      } catch (err) {
        console.error(err);
      }
    };
    fetchProducts();
  }, [categorySlug, searchParams]);

  // funkcja modyfikująca zachowanie checkboxa i aktualizująca URL o filtry
const handleCheckboxChange = (attrName, value) => {
  const currentValues = searchParams.getAll(attrName);

  if (currentValues.includes(value)) {
    searchParams.delete(attrName);
  } else {
    searchParams.delete(attrName);
    searchParams.set(attrName, value);
  }

  // reset paginacji przy zmianie filtrów
  searchParams.delete("page");
  setSearchParams(searchParams);
};

const handleResetFilters = () => {
  setSearchParams({});
};

  return (
    <div className="grid grid-cols-[1fr_4fr] gap-6 items-start">
      <aside className="bg-base-200 p-4 pl-10 max-h-screen overflow-y-auto sticky top-0">
        <div className="divider mb-6">
          <h2 className="font-bold text-lg">Filtry</h2>
        </div>         


        {/* Gdy są atrybuty */}
        {Object.keys(attributes).length > 0 ? (
          Object.keys(attributes).map(attrName => (
            <details key={attrName} className="mb-3">
              <summary className="cursor-pointer font-medium capitalize">
                {attrName}
              </summary>
              <ul className="menu dropdown-content bg-base-100 rounded-box w-70 p-2 shadow-sm ml-4 mt-2">
                {Object.entries(attributes[attrName]).map(([value, count]) => {
                  const isChecked = searchParams.getAll(attrName).includes(value);
                  return (
                    <li key={value} className="flex flex-row items-center gap-2">
                      <input type="checkbox" className="checkbox checkbox-sm" checked={isChecked} onChange={() => handleCheckboxChange(attrName, value)}/>
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
          <p>Brak filtrów</p>
        )}
        <div className="divider mt-10">
          <button onClick={handleResetFilters} className="btn btn-md btn-outline">
            Resetuj
          </button>
        </div>
      </aside>

      {/* Produkty */}
      <div className="flex flex-wrap justify-center gap-6 my-10 mr-5">
        {products.length > 0 ? (
          products.map(p => (
            <ProductCard key={p.id} categorySlug={p.category_slug} variant="catalog" {...p} />
          ))
        ) : (
          <span>
            Brak produktów spełniających kryteria
          </span>
        )}
      </div>
    </div>
  );
}

export default ProductCatalog;
