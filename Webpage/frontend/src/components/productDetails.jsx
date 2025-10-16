import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

function ProductDetails() {
  const { categorySlug, productSlug } = useParams(); // categorySlug też możesz użyć jeśli chcesz breadcrumb
  const [product, setProduct] = useState(null);
  const [attributes, setAttributes] = useState([]);

  useEffect(() => {
    const getProduct = async () => {
      try {
        const response = await axios.get(
          `/api/catalog/products/details/${productSlug}`
        );

        // Rozpakowujemy obiekt z API
        setProduct(response.data.product);
        setAttributes(response.data.attributes);
      } catch (err) {
        console.error("Unable to get product:", err);
      }
    };

    getProduct();
  }, [productSlug]);

  if (!product)
    return <div className="flex justify-center py-12">Loading...</div>;

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
          <button className="btn btn-primary mb-6">Dodaj do koszyka</button>

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
