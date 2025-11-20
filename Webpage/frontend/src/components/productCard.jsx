import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useCart} from "../utils/realCart";
import { getItem, updateQuantity } from "../utils/tempCartStorage";

function ProductCard({ id, name, slug, image, unit_price, price_including_promotion, variant, quantity }) {
  const [localQuantity, setLocalQuantity] = useState(1);
  const { isInCart, addToCart, removeFromCart } = useCart(id);

  useEffect(() => {
    const sync = () => {
      const item = getItem(id);
      setLocalQuantity(item?.quantity_user ?? 1);
    };

    sync();
    window.addEventListener("cartChange", sync);
    return () => window.removeEventListener("cartChange", sync);
  }, [id]);

  
  const handleAddToCart = (change) => {
    addToCart({
      id,
      quantity,
      price_including_promotion
    }, change);
  };

  const handleRemove = () => {
    removeFromCart(id, quantity);
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

          <div className="card-actions"> {/* blokowanie przycisku - checkIfInCart */}
            <button
              type="button"
              onClick={() => handleAddToCart(1)}
              className={isInCart ? "btn btn-in-cart mb-6 w-full" : "btn btn-custom mb-6 w-full"}
              disabled={isInCart}
            >
              {isInCart ? "W koszyku" : "Dodaj do koszyka"}
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
              <button type="button" className="btn btn-xs btn-ghost" disabled={localQuantity <= 1} onClick={() => updateQuantity(id, -1)}>
                –
              </button>
              <span className="w-10 text-center">
                {localQuantity}
                </span>
              <button type="button" className="btn btn-xs btn-ghost" onClick={() => updateQuantity(id, 1)}>
                +
              </button>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
             onClick={handleRemove}
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
