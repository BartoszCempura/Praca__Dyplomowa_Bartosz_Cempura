import { useEffect, useState, useRef } from "react";
import { getProductsInPromotion } from "../utils/promotionsActions";
import ProductCard from "./productCard";

function PromotionSlider({ promotionId }) {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [offset, setOffset] = useState(0);

  const trackRef = useRef(null);
  const containerRef = useRef(null);

  const [canScrollNext, setCanScrollNext] = useState(false);
  const [canScrollPrev, setCanScrollPrev] = useState(false);

  const CARDS_TO_SHOW = 3;
  const CARD_WIDTH = 384;
  const GAP = 40;

  useEffect(() => {
    async function load() {
      try {
        setIsLoading(true);
        setError(null);
        const data = await getProductsInPromotion(promotionId);
        setProducts(Array.isArray(data) ? data : []);
      } catch (err) {
        setError(err);
        setProducts([]);
      } finally {
        setIsLoading(false);
        setOffset(0);
      }
    }
    load();
  }, [promotionId]);

  useEffect(() => {
    function checkScroll() {
      if (!containerRef.current || !trackRef.current) return;

      const containerWidth = containerRef.current.offsetWidth;
      const trackWidth = trackRef.current.scrollWidth;

      setCanScrollPrev(offset < 0);
      setCanScrollNext(Math.abs(offset) + containerWidth < trackWidth - 1);
    }

    checkScroll();
    window.addEventListener("resize", checkScroll);

    return () => window.removeEventListener("resize", checkScroll);
  }, [products, offset]);

  const next = () => {
    if (!canScrollNext || !trackRef.current || !containerRef.current) return;
    const scrollAmount = (CARD_WIDTH + GAP) * CARDS_TO_SHOW;

    setOffset(prev => {
      const newOffset = prev - scrollAmount;
      const maxOffset = -(trackRef.current.scrollWidth - containerRef.current.offsetWidth);
      return Math.max(newOffset, maxOffset);
    });
  };

  const prev = () => {
    if (!canScrollPrev) return;
    const scrollAmount = (CARD_WIDTH + GAP) * CARDS_TO_SHOW;

    setOffset(prev => {
      const newOffset = prev + scrollAmount;
      return Math.min(newOffset, 0);
    });
  };

  if (isLoading) {
    return (
      <div className="flex flex-col justify-center items-center py-10">
          <span className="loading loading-bars loading-lg text-primary"></span>
          <p className="text-gray-500">Please wait...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-10">
        <p className="text-red-500">
          Error: {error?.message || "Nie udało się pobrać danych"}
        </p>
        <p className="text-red-500">
          Please refresh the page
        </p>
      </div>
    );
  }

  if (products.length === 0) {
    return (
      <div className="text-center py-10">
        <p className="text-gray-500">Brak produktów w promocji.</p>
      </div>
    );
  }

  return (
    <div ref={containerRef} className="container w-full overflow-hidden mx-auto">
      <div className="flex flex-col">
        <div className="flex justify-center items-center w-full gap-10">
          <button
            disabled={!canScrollPrev}
            onClick={prev}
            className="btn btn-circle pointer-events-auto shadow-sm hover:shadow-amber-500 transition-shadow duration-100"
          >
            ❮
          </button>

          <h1 className="text-4xl font-bold text-center">
            Produkty w promocyjnych cenach
          </h1>

          <button
            disabled={!canScrollNext}
            onClick={next}
            className="btn btn-circle pointer-events-auto shadow-sm hover:shadow-amber-500 transition-shadow duration-100"
          >
            ❯
          </button>
        </div>

        <div
          ref={trackRef}
          className="flex gap-10 transition-transform duration-500 ease-in-out my-10 justify-start"
          style={{ transform: `translate3d(${offset}px, 0, 0)` }}
        >
          {products.map((p) => (
            <div key={p.id} className="flex-shrink-0">
              <ProductCard id={p.id} variant="catalog" {...p} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default PromotionSlider;