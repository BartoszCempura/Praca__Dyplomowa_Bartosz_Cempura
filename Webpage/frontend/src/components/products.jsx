import { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function Product({categorySlug, name, slug, image, unit_price, price_including_promotion }) {
  return (
    <div className="card card-side bg-base-100 shadow-md w-100 grid grid-cols-2">
      <figure>
        <Link to={`/${categorySlug}/${slug}`}><img src={image} alt={name}/></Link>
      </figure>
      <div className="card-body flex flex-col justify-between">
        <Link to={`/${categorySlug}/${slug}`}><h2 className="card-title">{name}</h2></Link>
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
    <div className="flex flex-wrap justify-center gap-6 mt-10">
      {products.length > 0 ? (
        products.map((p) => <Product key={p.id} categorySlug={categorySlug} {...p} />)
      ) : (
        <span className="text-gray-400 italic">No products found</span>
      )}
    </div>
  );
}

export default Products;
