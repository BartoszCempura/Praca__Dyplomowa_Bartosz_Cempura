import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import axios from "axios";

function Product({ name, slug, image, unit_price, price_including_promotion }) {
  return (
    <div className="card card-side bg-base-100 shadow-md w-100 grid grid-cols-2">
      <figure>
        <Link to={`/product/${slug}`}><img src={image} alt={name}/></Link>
      </figure>
      <div className="card-body flex flex-col justify-between">
        <Link to={`/product/${slug}`}><h2 className="card-title">{name}</h2></Link>
        <span className="font-normal">
          ${price_including_promotion || unit_price}
        </span>
        <div className="card-actions">
          <button className="btn btn-primary">Dodaj do koszyka</button>
        </div>
      </div>
    </div>
  );
}

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
      <h2 className="text-2xl font-bold mb-6">
        Wyniki wyszukiwania dla: <span className="text-primary">{searchValue}</span>
      </h2>
      <div className="flex flex-wrap justify-center gap-6">
        {products.length > 0 ? (
          products.map((p) => <Product key={p.slug} {...p} />)
        ) : (
          <span className="text-gray-400 italic">Brak wyników</span>
        )}
      </div>
    </div>
  );
}

export default SearchProducts;
