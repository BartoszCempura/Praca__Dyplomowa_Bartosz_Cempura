import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api/tokenHandler";

function ProductDetails() {
  const { productSlug } = useParams(); 
  const [product, setProduct] = useState(null);
  const [attributes, setAttributes] = useState([]);
  const [isInCart, setIsInCart] = useState(false);

  // 🟢 Pobieranie danych o produkcie
  useEffect(() => {
    const getProduct = async () => {
      try {
        const response = await api.get(`/catalog/products/details/${productSlug}`);
        setProduct(response.data.product);
        setAttributes(response.data.attributes);
      } catch (err) {
        console.error("Ups, nie udało się pobrać danych o produkcie:", err);
      }
    };
    getProduct();
  }, [productSlug]);

  // 🟢 Sprawdzenie, czy produkt jest w koszyku
  useEffect(() => {
    if (!product?.id) return;

    const checkIfInCart = async () => {
      try {
        const response = await api.get("/commerce/carts");
        const products = response.data.products || [];
        const exists = products.some((p) => p.product_id === product.id);
        setIsInCart(exists);
      } catch (err) {
        console.error("Błąd sprawdzania koszyka:", err);
      }
    };

    checkIfInCart();
    window.addEventListener("cartChange", checkIfInCart);
    return () => window.removeEventListener("cartChange", checkIfInCart);
  }, [product?.id]);

  if (!product)
    return <div className="flex justify-center py-12">Loading...</div>;

  // 🟢 Funkcja dodająca produkt do koszyka (identyczna logika jak w CartProduct)
  const addToCart = async (change = 1) => {
    try {
      await api.put("/commerce/carts", { product_id: product.id, quantity: change });

      // 🔹 Aktualizacja localStorage
      const stored = localStorage.getItem("tempCartQuantity");
      const tempCart = stored ? JSON.parse(stored) : {};

      tempCart[product.id] = tempCart[product.id] || {};
      const currentQty = tempCart[product.id].quantity_user || 0;
      const newQty = currentQty + change;

      // 🔸 Zabezpieczenie: jeśli wynik byłby ujemny, pomijamy zapis
      if (change < 0 && newQty < 0) {
        console.warn(`❌ Pominięto zapis — ilość produktu ${product.id} byłaby ujemna.`);
        return;
      }

      tempCart[product.id].quantity_user = newQty;
      tempCart[product.id].price_including_promotion = product.price_including_promotion;

      localStorage.setItem("tempCartQuantity", JSON.stringify(tempCart));

      // 🔹 Odświeżamy widok koszyka
      window.dispatchEvent(new Event("cartChange"));
      setIsInCart(true); // po dodaniu ustawiamy od razu flagę
    } catch (err) {
      console.error(err);
      if (err.response?.status === 401) {
        alert("Musisz być zalogowany, aby dodać produkt do koszyka!");
      } else {
        alert(err.response?.data?.error || "Coś poszło nie tak");
      }
    }
  };

  return (
    <div className="hero bg-base-100 min-h-screen py-12">
      <div className="hero-content flex-col lg:flex-row items-start gap-12">
        {/* Obraz produktu */}
        <img src={product.image} alt={product.name} className="max-w-sm rounded-lg shadow-2xl" />

        {/* Dane produktu */}
        <div className="lg:ml-8 flex-1">
          <h1 className="text-4xl font-bold mb-4">{product.name}</h1>
          <p className="text-lg mb-6">{product.description}</p>
          <p className="text-2xl font-semibold mb-6">
            {product.price_including_promotion} PLN
          </p>

          {/* 🔘 Przycisk dodania do koszyka */}
          <button
              type="button"
              onClick={() => addToCart(1)}
              className={isInCart ? "btn btn-in-cart mb-6 w-full" : "btn btn-custom mb-6 w-full"}
              disabled={isInCart} // ✅ blokada przycisku
            >
            {isInCart ? "W koszyku" : "Dodaj do koszyka"}
          </button>
          

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
