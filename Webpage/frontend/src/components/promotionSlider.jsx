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
    const containerWidth = containerRef.current?.offsetWidth || 0;
    setOffset(prev => prev - containerWidth);
  };

  const prev = () => {
    if (!canScrollPrev) return;
    const containerWidth = containerRef.current?.offsetWidth || 0;
    setOffset(prev => prev + containerWidth);
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
      setCanScrollNext(Math.abs(offset) + containerWidth < trackWidth);
    }

    checkScroll();
    window.addEventListener("resize", checkScroll);

    return () => window.removeEventListener("resize", checkScroll);
  }, [products, offset]);

  return (
    <div ref={containerRef} className="container w-full overflow-hidden mx-auto">
      <div className="flex flex-col justify-center items-center">
        <h1 className="text-4xl font-bold mb-5">
          Produkty w promocyjnych cenach
        </h1>

        <div className="flex gap-2">
          <button disabled={!canScrollPrev} onClick={prev} className="btn btn-circle">
            ❮
          </button>
          <button disabled={!canScrollNext} onClick={next} className="btn btn-circle">
            ❯
          </button>
        </div>
      </div>

      <div
        ref={trackRef}
        className="flex gap-10 transition-transform duration-500 ease-in-out mt-5 mb-10 justify-start"
        style={{ transform: `translate3d(${offset}px, 0, 0)` }}
      >
        {products.map((p) => (
          <div key={p.id}>
            <ProductCard id={p.id} variant="catalog" {...p} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default PromotionSlider;
