import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getItem, updateQuantity } from "../utils/tempCartStorage";
import { useCart } from "../utils/useCart"
import { useWishlist } from "../utils/useWhishlist";
import { addToCart, removeFromCart } from "../utils/cartActions";
import { addToWishlist, removeFromWishlist} from "../utils/wishlistActions";

function ProductCard({ id, name, slug, category_slug, image, unit_price, unit_price_with_discount, variant, quantity }) {
  const [ localQuantity, setLocalQuantity ] = useState(1);
  const inWishList = useWishlist(id);
  const isInCart = useCart(id);

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
      unit_price_with_discount
    }, change);
  };

  const handleAddToWishlist = () => {
    if (!inWishList) {
      addToWishlist(id);
    } else {
      removeFromWishlist(id);
    }
  };

  const handleRemove = () => {
    removeFromCart(id, quantity);
  };

  if (variant === "catalog") {
  return (
    <div className="card bg-base-200 shadow-md hover:shadow-black/40 transition-shadow duration-100 w-96 h-48 border border-gray-900 relative">
      
      <button 
        type="button" 
        className="absolute top-2 right-2 z-10 p-1.5 rounded-full bg-base-200 transition-colors group" 
        onClick={handleAddToWishlist}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className={`h-6 w-6 transition-colors duration-200 ${inWishList ? 'fill-amber-500 stroke-amber-500' : 'group-hover:stroke-amber-500'}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
        </svg>
      </button>

      {/* Grid layout dla obrazu i contentu */}
      <div className="grid grid-cols-2 h-full">
        {/* Obraz produktu */}
        <figure className="overflow-hidden h-full">
          <Link to={`/product/${slug}`}>
            <img src={image} alt={name} className="object-cover w-full h-full rounded-lg" />
          </Link>
        </figure>

        {/* Zawartość */}
        <div className="card-body flex flex-col justify-between p-4">
          {/* kategoria */}
          <span className="text-sm text-gray-500">{category_slug}</span>
          
          {/* Nazwa */}
          <Link to={`/product/${slug}`}>
            <h2 className="card-title text-base">{name}</h2>
          </Link>
          
          {/* Cena */}
          {unit_price_with_discount !== unit_price ? (
            <div className="flex flex-col gap-1 mb-1">
              <span className="text-lg font-semibold text-amber-500">{unit_price_with_discount} PLN</span>
              <span className="line-through text-sm text-gray-500">{unit_price} PLN</span>
            </div>
          ) : (
            <span className="text-lg font-semibold">{unit_price_with_discount} PLN</span>
          )}
          
          {/* Przycisk */}
          <div className="card-actions mt-auto">
            <button 
              type="button" 
              onClick={() => handleAddToCart(1)} 
              className={isInCart ? "btn btn-in-cart w-full btn-sm" : "btn btn-custom w-full btn-sm"} 
              disabled={isInCart}
            >
              {isInCart ? "W koszyku" : "Dodaj"}
            </button>
          </div>
        </div>
      </div>

    </div>
  );
}


  if (variant === "cart") {
    return (
      <div className="w-full flex items-center gap-6 bg-base-200 shadow-md border border-gray-900 rounded-lg p-4 hover:shadow-black/40 transition-shadow duration-100">
        {/* Zdjęcie produktu */}
        <figure className="w-24 h-24 flex-shrink-0 hidden 2xl:block">
          <Link to={`/product/${slug}`}>
            <img src={image} alt={name} className="w-full h-full object-cover rounded-lg" />
          </Link>
        </figure>

        <div className="flex justify-between items-center flex-grow gap-6">
          {/* Nazwa produktu */}
          <Link to={`/product/${slug}`} className="flex-1">
            <h2 className="text-lg font-semibold line-clamp-1">{name}</h2>
          </Link>
          {/* Cena produktu*/}
          <span className="font-medium whitespace-nowrap">{unit_price_with_discount} PLN</span>

          {/* Sekcja zmiany ilości */}
          <div className="flex items-center gap-2">
            <label className="text-sm text-gray-600">Ilość:</label>
            <div className="flex items-center border rounded-md overflow-hidden">
              <button type="button" className="btn btn-xs btn-ghost" disabled={localQuantity <= 1} onClick={() => updateQuantity(id, -1)}>-</button>
              <span className="w-10 text-center">{localQuantity}</span>
              <button type="button" className="btn btn-xs btn-ghost" onClick={() => updateQuantity(id, 1)}>+</button>
            </div>
          </div>

        </div>
        {/* Usówanie produktu z koszyka */}
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

  if (variant === "summary") {
    return (
      <div className="w-full flex items-center gap-6 bg-base-200 shadow-md border border-gray-900 rounded-lg p-4 hover:shadow-black/40 transition-shadow duration-100">
        {/* Zdjęcie produktu */}
        
        <figure className="w-24 h-24 flex-shrink-0">
            <img src={image} alt={name} className="w-full h-full object-cover rounded-lg" />
        </figure>

        <div className="flex justify-between items-center flex-grow gap-6">
          {/* Nazwa produktu */}
            <h2 className="text-lg font-semibold line-clamp-1">{name}</h2>

          {/* Cena produktu i ilość */}  
            <div className="flex items-center gap-2">
              <span className="font-medium whitespace-nowrap mr-4">{unit_price_with_discount} PLN</span>
              <label className="text-sm text-gray-500">Ilość:</label>
              <div className="flex items-center">
                <span className="w-10 text-center">{localQuantity}</span>
              </div>
            </div>

        </div>
      </div>
    );
  }

if (variant === "topProducts") {
  return (
    <div className="w-72 flex items-stretch gap-4 bg-base-200 shadow-md border border-gray-900 rounded-lg hover:shadow-black/40 transition-shadow duration-100">

      {/* Zdjęcie produktu */}
      <figure className="w-24 h-24 flex-shrink-0">
        <Link to={`/product/${slug}`}>
          <img src={image} alt={name} className="w-full h-full object-cover rounded-lg" />
        </Link>
      </figure>

      <div className="flex flex-col flex-1 gap-2 min-w-0 p-2">
        
        {/* Nazwa produktu */}
        <Link to={`/product/${slug}`} className="block">
          <h2 className="text-base font-semibold line-clamp-2 break-words">
            {name}
          </h2>
        </Link>
        
        {/* Cena produktu */}
        <span className="text-sm font-medium text-amber-500 whitespace-nowrap mt-auto">
          {unit_price_with_discount} PLN
        </span>
      </div>
    </div>
  );
}

if (variant === "bestseller") {
  return (
    <div className="card bg-base-200 shadow-md hover:shadow-black/40 transition-shadow duration-100 border border-gray-900 relative mx-10 group"
    style={{ height: 'calc((96px * 2) + 24px)' }}>
        <figure className="overflow-hidden rounded-lg h-full bg-white">
          <Link to={`/product/${slug}`}>
            <img src={image} alt={name} className="object-cover scale-[0.4]" />
          </Link>
        </figure>
        <div className="absolute bottom-0 left-0 right-0
        h-1/4 bg-base-200/95 text-white
        flex justify-center items-end gap-6 p-4
        opacity-0 group-hover:opacity-100
        transition-opacity duration-200">
          {/*<span className="text-base">{category_slug}</span>*/}
          <Link to={`/product/${slug}`}>
              <h2 className="card-title text-base">{name}</h2>
          </Link>
          <span className="text-base font-semibold text-amber-500">{unit_price_with_discount} PLN</span>
        </div>
      </div>
  );
}


  return null;
}

export default ProductCard;

