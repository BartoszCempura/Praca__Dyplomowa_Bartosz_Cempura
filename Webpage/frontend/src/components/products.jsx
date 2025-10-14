import { useEffect, useState } from "react";
import axios from "axios";

function Product({ name, image, unit_price, price_including_promotion }) {
  return (
    <div className="card bg-base-200 max-w-60 shadow hover:shadow-lg transition">
      <figure className="hover-gallery">
        <img src={image} alt={name} className="w-full h-40 object-cover" />
      </figure>
      <div className="card-body">
        <h2 className="card-title flex justify-between">
          {name}
          <span className="font-normal">
            ${price_including_promotion || unit_price}
          </span>
        </h2>
      </div>
    </div>
  );
}

function Products({ categorySlug }) {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const getProducts = async () => {
      try {
        const response = await axios.get(`/api/catalog/products/${categorySlug}`);
        setProducts(response.data.products); // <--- access products array
      } catch (err) {
        console.error("Error fetching products:", err);
      }
    };

    if (categorySlug) getProducts(); // only fetch if slug exists
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
