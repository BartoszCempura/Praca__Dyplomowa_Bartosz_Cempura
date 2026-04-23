import { useEffect, useState, useRef } from "react";
import { getTopProducts } from "../utils/topProductsActions"
import ProductCard from "./productCard";

function TopProducts() {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [offset, setOffset] = useState(0);

  const trackRef = useRef(null);
  const containerRef = useRef(null);

  const [canScrollNext, setCanScrollNext] = useState(false);
  const [canScrollPrev, setCanScrollPrev] = useState(false);

  const CARDS_TO_SHOW = 3;  // Ilość kart do pokazania
  const CARD_WIDTH = 320;   // w-96 = 384px
  const GAP = 47;  // gap-10 = 40px
  
  useEffect(() => {
    async function load() {
      try {
        setIsLoading(true);
        setError(null);
        const data = await getTopProducts();
        setProducts(data.topProducts || []);
      } catch (err) {
        setError(err);
        setProducts([]);
      } finally {
        setIsLoading(false);
        setOffset(0);
      }
    }
    load();
  }, []);

  const next = () => {
    if (!canScrollNext) return;
    const scrollAmount = (CARD_WIDTH + GAP) * CARDS_TO_SHOW;
    setOffset(prev => {
      const newOffset = prev - scrollAmount;
      const maxOffset = -(trackRef.current.scrollWidth - containerRef.current.offsetWidth + 65);
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

  useEffect(() => {
    function checkScroll() {
      if (!containerRef.current || !trackRef.current) return;

      const containerWidth = containerRef.current.offsetWidth;
      const trackWidth = trackRef.current.scrollWidth;

      setCanScrollPrev(offset < 0);

      setCanScrollNext(Math.abs(offset) + containerWidth < trackWidth  - 1);
    }

    checkScroll();
    window.addEventListener("resize", checkScroll);

    return () => window.removeEventListener("resize", checkScroll);
  }, [products, offset]);

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
        <p className="text-gray-500">Brak zarejestrowanych interakcji.</p>
      </div>
    );
  }
 
  return (
    <div ref={containerRef} className="w-full overflow-hidden mx-auto relative">
      <div className="flex flex-col justify-center items-center">
        <div className="relative w-full pl-8">
            {/* Przyciski nawigacji - absolute positioning */}

            <div className="flex justify-center items-center w-full gap-10 mb-10">
              <button 
                disabled={!canScrollPrev} 
                onClick={prev} 
                className="btn btn-circle pointer-events-auto shadow-sm hover:shadow-amber-500 transition-shadow duration-100"
              >
                ❮
              </button>

              <h1 className="text-4xl font-bold">Top produkty tego tygodnia</h1>
          
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
              className="grid grid-rows-2 transition-transform duration-500 ease-in-out ml-5"
              style={{ 
                transform: `translate3d(${offset}px, 0, 0)`,
                gridAutoFlow: 'column',
                gridAutoColumns: '320px', // Szerokość kolumny (w-96) 
                columnGap: GAP, // gap-10
                rowGap: '24px'// gap-6
              }}
            >
              {products.map((p) => (
                <ProductCard key={p.id} id={p.id} variant="topProducts" {...p} />
              ))}
            </div>
          </div>

      </div>
    </div>
  );
}

export default TopProducts;
