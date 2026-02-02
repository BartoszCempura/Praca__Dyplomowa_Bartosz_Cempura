import { useEffect, useState, useRef } from "react";
import { getTopProducts } from "../utils/topProductsActions"
import ProductCard from "./productCard";

function TopProducts() {
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
      const data = await getTopProducts();
      setProducts(data);
      setOffset(0); // reset offset on load
    }
    load();
  }, []);

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

  return (
    <div ref={containerRef} className="container w-full overflow-hidden mx-auto">
      <div className="flex flex-col justify-center items-center">
        <h1 className="text-4xl font-bold mb-5">
          Top produkty tego miesiąca
        </h1>

        <div className="relative w-full">
            {/* Pojemnik z produktami */}
            <div
              ref={trackRef}
              className="flex gap-10 transition-transform duration-500 ease-in-out mt-5 mb-5 justify-start"
              style={{ transform: `translate3d(${offset}px, 0, 0)` }}
            >
              {products.map((p, index) => (
                <div key={p.id} className="flex-shrink-0">
                  <ProductCard id={p.id} variant="catalog" {...p} />
                </div>
              ))}
            </div>

            {/* Przyciski nawigacji - absolute positioning */}
            <div className="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between pointer-events-none">
              <button 
                disabled={!canScrollPrev} 
                onClick={prev} 
                className="btn btn-circle pointer-events-auto"
              >
                ❮
              </button>
              <button 
                disabled={!canScrollNext} 
                onClick={next} 
                className="btn btn-circle pointer-events-auto"
              >
                ❯
              </button>
            </div>
          </div>

      </div>
    </div>
  );
}

export default TopProducts;
