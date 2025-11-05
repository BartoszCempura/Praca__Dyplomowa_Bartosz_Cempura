import { Link } from "react-router-dom";
import api from "../api/tokenHandler";

function ProductCard({ id, name, slug, image, unit_price, price_including_promotion }) {
  const addToCart = async () => {
    try {
      const response = await api.post("/commerce/carts", {
        product_id: id,
        quantity: 1, // Dodajemy 1 sztukę produktu. Można to rozszerzyć o możliwość wyboru ilości.
      });

      window.dispatchEvent(new Event("cartChange"));
    } catch (err) {
      console.error(err);

      if (err.response?.status === 401) {
        alert("Musisz być zalogowany, aby dodać produkt do koszyka!");
      } else {
        alert(err.response?.data?.error || "Something went wrong");
      }
    }
  };

  return (
    <div className="card card-side bg-base-200 shadow-md hover:shadow-md hover:shadow-black/40 transition-shadow duration-100 w-100 grid grid-cols-2 border-1 border-gray-900">
      <figure>
        <Link to={`/product/${slug}`}><img src={image} alt={name} className="object-cover w-full h-full"/></Link>
      </figure>
      <div className="card-body flex flex-col justify-between">
        <Link to={`/product/${slug}`}><h2 className="card-title">{name}</h2></Link>
        <span className="font-normal">
          ${price_including_promotion || unit_price}
        </span>
        <div className="card-actions">
          <button type="button" onClick={addToCart} className="btn btn-custom">Dodaj do koszyka</button>
        </div>
      </div>
    </div>
  );
}

export default ProductCard;