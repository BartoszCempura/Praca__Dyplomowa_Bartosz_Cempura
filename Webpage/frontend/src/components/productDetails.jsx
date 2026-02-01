import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api/tokenHandler";
import { useCart} from "../utils/useCart";
import { addToCart } from "../utils/cartActions";
import ProductCard from "./productCard";
import { trackInteraction } from "../utils/trackInteraction";

function ProductDetails() {
  const { productSlug } = useParams(); 
  const [product, setProduct] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [attributes, setAttributes] = useState([]);
  const isInCart  = useCart(product?.id);

  useEffect(() => {
    const getProduct = async () => {
      try {
        const response = await api.get(`/catalog/products/details/${productSlug}`);
        setProduct(response.data.product);
        setAttributes(response.data.attributes);
        const recomendation_response = await api.get(`/algorithms/products-similar/${productSlug}`);
        setRecommendations(recomendation_response.data || []);
        if (response.data.product?.id) {
          trackInteraction(response.data.product.id, 'View');
        }
      } catch (err) {
        console.error("Ups, nie udało się pobrać danych o produkcie:", err);
      }
    };
    getProduct();
  }, [productSlug]);

  if (!product)
    return <div className="flex justify-center py-12">Loading...</div>;

  const handleAddToCart = (change) => {
    addToCart({
      id: product.id,
      quantity: product.quantity,
      unit_price_with_discount: product.unit_price_with_discount
    }, change);
  };

  return (
    <>
      <div className="hero bg-base-100 min-h-screen py-12">

        <div className="hero-content flex-col lg:flex-row items-start gap-12 ">

          {/* Obraz produktu */}
          {/* Rating nie jest zapisywany - do rozwinięcia */}
          <div className="flex flex-col items-center">
            <img src={product.image} alt={product.name} className="max-w-sm rounded-lg shadow-2xl" />
            <div className="rating rating-xl mt-4 gap-2">
              <input type="radio" name="rating-5" className="mask mask-star-2 bg-orange-400" aria-label="1 star" />
              <input type="radio" name="rating-5" className="mask mask-star-2 bg-orange-400" aria-label="2 star" />
              <input type="radio" name="rating-5" className="mask mask-star-2 bg-orange-400" aria-label="3 star" />
              <input type="radio" name="rating-5" className="mask mask-star-2 bg-orange-400" aria-label="4 star" />
              <input type="radio" name="rating-5" className="mask mask-star-2 bg-orange-400" aria-label="5 star" defaultChecked/>
            </div>
          </div>

          {/* Dane produktu */}
          <div className="lg:ml-8 flex-1">
            <span className="text-sm text-gray-500">{product.category_slug}</span>
            <h1 className="text-4xl font-bold mb-4">{product.name}</h1>
            <p className="text-lg mb-6">{product.description}</p>
            <p className="text-2xl font-semibold mb-6">{product.unit_price_with_discount} PLN</p>

            {/*Przycisk dodania do koszyka */}
            <button type="button" onClick={() => handleAddToCart(1)}
                className={isInCart ? "btn btn-in-cart mb-6 w-full" : "btn btn-custom mb-6 w-full"}
                disabled={isInCart}>
              {isInCart ? "W koszyku" : "Dodaj do koszyka"}
            </button>

            {/* Atrybuty */}
            {attributes.length > 0 && (
              <div>
                <h2 className="text-2xl font-semibold mb-4">Specyfikacja:</h2>
                <ul className="list-disc list-inside space-y-1">
                  {attributes.map((attribute) => (
                    <li key={attribute.name}><strong>{attribute.name}:</strong> {attribute.value}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

        </div>

      </div>
      <div className="bg-base-200">
        <div className="p-4 text-center">
            <h1 className="text-4xl font-bold my-5">Podobne produkty</h1>
        </div>
        <div className="container flex gap-10 justify-center mx-auto flex-wrap">
            {recommendations.map((p) => (
            <div key={p.id}>
              <ProductCard id={p.id} variant="catalog" {...p} />
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default ProductDetails;
