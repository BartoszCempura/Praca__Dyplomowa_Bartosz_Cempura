import { useEffect, useState } from "react";
import axios from "axios";

function Product({ name, image, unit_price, price_including_promotion }) {
  return (
    <div className="card card-side bg-base-100 shadow-md w-100 grid grid-cols-2">
      <figure>
        <img src={image} alt={name}/>
      </figure>
      <div className="card-body flex flex-col justify-between">
        <h2 className="card-title">{name}</h2>
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

function Products({ categorySlug }) {
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
    <div className="flex flex-wrap justify-center gap-6 mt-6">
      {products.length > 0 ? (
        products.map((p) => <Product key={p.id} {...p} />)
      ) : (
        <span className="text-gray-400 italic">No products found</span>
      )}
    </div>
  );
}

export default Products;
