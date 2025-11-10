import { Link } from "react-router-dom";
import api from "../api/tokenHandler";

function ProductCard({ id, name, slug, image, unit_price, price_including_promotion, variant, quantity }) {

  const addToCart = async (change) => {
  try {  
    const response = await api.put("/commerce/carts", {
      product_id: id,
      quantity: change, // <- zamiast "quantity"
    });
    window.dispatchEvent(new Event("cartChange"));
  } catch (err) {
    console.error(err);
    if (err.response?.status === 401) {
      alert("Musisz być zalogowany, aby dodać produkt do koszyka!");
    } else {
      alert(err.response?.data?.error || "Coś poszło nie tak");
    }
  }
};

  if (variant === "catalog") {
    return (
      <div className="card card-side bg-base-200 shadow-md hover:shadow-black/40 transition-shadow duration-100 w-100 grid grid-cols-2 border border-gray-900">
        <figure>
          <Link to={`/product/${slug}`}>
            <img src={image} alt={name} className="object-cover w-full h-full" />
          </Link>
        </figure>
        <div className="card-body flex flex-col justify-between">
          <Link to={`/product/${slug}`}>
            <h2 className="card-title">{name}</h2>
          </Link>
          
          {price_including_promotion !== unit_price ? (
            <div className="relative inline-block">
              <span className="text-md font-semibold text-success">
                ${price_including_promotion}
              </span>
              <span className="absolute right-2 -top-1 text-error line-through text-sm">
                ${unit_price}
              </span>
            </div>
          ) : (
            <span className="text-md font-semibold">
              ${price_including_promotion}
            </span>
          )}

          <div className="card-actions">
            <button type="button" onClick={() => addToCart(1)} className="btn btn-custom">
              Dodaj do koszyka
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (variant === "cart") {
    return (
      <div className="w-full flex items-center gap-6 bg-base-200 shadow-md border border-gray-900 rounded-lg p-4 hover:shadow-black/40 transition-shadow duration-100">
        <figure className="w-24 h-24 flex-shrink-0">
          <Link to={`/product/${slug}`}>
            <img src={image} alt={name} className="w-full h-full object-cover rounded-lg" />
          </Link>
        </figure>

        <div className="flex justify-between items-center flex-grow gap-6">
          <Link to={`/product/${slug}`} className="flex-1">
            <h2 className="text-lg font-semibold line-clamp-1">{name}</h2>
          </Link>

          <span className="font-medium whitespace-nowrap">
            ${price_including_promotion}
          </span>

          {/* Sekcja zmiany ilości */}
          <div className="flex items-center gap-2">
            <label className="text-sm text-gray-600">Ilość:</label>
            <div className="flex items-center border rounded-md overflow-hidden">
              <button
                type="button"
                className="btn btn-xs btn-ghost"
                disabled={quantity <= 1}
                onClick={() => addToCart((-1))} // zmniejsz ilość
              >
                –
              </button>
              <span className="w-10 text-center">{quantity}</span>
              <button
                type="button"
                className="btn btn-xs btn-ghost"
                onClick={() => addToCart(1)} // zwiększ ilość
              >
                +
              </button>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={() => addToCart(-quantity)} // usuń cały produkt
            className="btn btn-sm btn-error text-white">
            Usuń
          </button>
        </div>
      </div>
    );
  }

  return null;
}

export default ProductCard;
