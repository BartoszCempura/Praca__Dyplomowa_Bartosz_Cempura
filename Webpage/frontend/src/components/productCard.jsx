import { Link } from "react-router-dom";

function ProductCard({ name, slug, image, unit_price, price_including_promotion }) {
  return (
    <div className="card card-side bg-base-100 shadow-md hover:shadow-md hover:shadow-black/40 transition-shadow duration-100 w-100 grid grid-cols-2">
      <figure>
        <Link to={`/product/${slug}`}><img src={image} alt={name} className="object-cover w-full h-full"/></Link>
      </figure>
      <div className="card-body flex flex-col justify-between">
        <Link to={`/product/${slug}`}><h2 className="card-title">{name}</h2></Link>
        <span className="font-normal">
          ${price_including_promotion || unit_price}
        </span>
        <div className="card-actions">
          <button className="btn btn-custom">Dodaj do koszyka</button>
        </div>
      </div>
    </div>
  );
}

export default ProductCard;