import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api/tokenHandler";

function ProductDetails() {
  const { productSlug } = useParams(); 
  const [product, setProduct] = useState(null);
  const [attributes, setAttributes] = useState([]);

  useEffect(() => {
    const getProduct = async () => {
      try {
        const response = await api.get(`/catalog/products/details/${productSlug}`);
        setProduct(response.data.product);
        setAttributes(response.data.attributes);
      } catch (err) {
        console.error("Ups nie udało się pobrać danych o produkcie:", err);
      }
    };

    getProduct();
  }, [productSlug]);

  if (!product) // potrzebne aby React nie starał się załadować danych przed ich wczytaniem z API
    return <div className="flex justify-center py-12">Loading...</div>;

    const addToCart = async () => {
    try {
      const response = await api.put("/commerce/carts", {
        product_id: product.id,
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
    <div className="hero bg-base-100 min-h-screen py-12">
      <div className="hero-content flex-col lg:flex-row items-start gap-12">
        {/* Obraz produktu */}
        <img src={product.image} alt={product.name} className="max-w-sm rounded-lg shadow-2xl"/>

        {/* Dane produktu */}
        <div className="lg:ml-8 flex-1">
          <h1 className="text-4xl font-bold mb-4">{product.name}</h1>
          <p className="text-lg mb-6">{product.description}</p>
          <p className="text-2xl font-semibold mb-6">
            {product.price_including_promotion} PLN
          </p>
          <button type="button" onClick={addToCart} className="btn btn-custom mb-6">Dodaj do koszyka</button>

          {/* Atrybuty */}
          {attributes.length > 0 && (
            <div>
              <h2 className="text-2xl font-semibold mb-4">Specyfikacja:</h2>
              <ul className="list-disc list-inside space-y-1">
                {attributes.map((attr) => (
                  <li key={attr.name}>
                    <strong>{attr.name}:</strong> {attr.value}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProductDetails;
