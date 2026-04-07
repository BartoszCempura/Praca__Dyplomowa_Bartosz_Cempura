import { useEffect, useState, useRef } from "react";
import { getProductsInPromotion } from "../utils/promotionsActions";
import ProductCard from "./productCard";

function PromotionSlider({ promotionId }) {
  const [products, setProducts] = useState([]);
  const [offset, setOffset] = useState(0);

  const trackRef = useRef(null);
  const containerRef = useRef(null);

  const [canScrollNext, setCanScrollNext] = useState(false);
  const [canScrollPrev, setCanScrollPrev] = useState(false);

  const CARDS_TO_SHOW = 3;  // Ilość kart do pokazania
  const CARD_WIDTH = 384;   // w-96 = 384px
  const GAP = 40;  // gap-10 = 40px

  // ---- LOAD PRODUCTS ----
  useEffect(() => {
    async function load() {
      const data = await getProductsInPromotion(promotionId);
      setProducts(data);
      setOffset(0); // reset offset on load
    }
    load();
  }, [promotionId]);

  // ---- SCROLL BUTTONS LOGIC ----
  const next = () => {
    if (!canScrollNext) return;
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
      return Math.min(newOffset, 0); // Nie scrolluj przed początek
    });
  };

  // ---- BUTTON DISABLE LOGIC ----
  useEffect(() => {
    function checkScroll() {
      if (!containerRef.current || !trackRef.current) return;

      const containerWidth = containerRef.current.offsetWidth;
      const trackWidth = trackRef.current.scrollWidth;

      // Can scroll left?
      setCanScrollPrev(offset < 0);

      // Can scroll right?
      setCanScrollNext(Math.abs(offset) + containerWidth < trackWidth  - 1);
    }

    checkScroll();
    window.addEventListener("resize", checkScroll);

    return () => window.removeEventListener("resize", checkScroll);
  }, [products, offset]);

  if (!products) {
    return (
      <div className="text-center py-10">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  return (
    <div ref={containerRef} className="container w-full overflow-hidden mx-auto">
      <div className="flex flex-col">
        <div className="flex justify-center items-center w-full gap-10">  
          {/* Przyciski nawigacji - absolute positioning */}
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
            {/* Pojemnik z produktami */}
            <div
              ref={trackRef}
              className="flex gap-10 transition-transform duration-500 ease-in-out my-10 justify-start"
              style={{ transform: `translate3d(${offset}px, 0, 0)` }}
            >
              {products.map((p, index) => (
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
