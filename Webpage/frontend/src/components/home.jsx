import Bestseller from "./bestseller";
import PromotionSlider from "./promotionSlider";
import TopProducts from "./topProducts";
import { useEffect, useRef } from "react";

function Home() {

  const sliderRef = useRef(null);
  const sliderIntervalRef = useRef(null);

  const next = () => {

    const slider = sliderRef.current; // tam gdzie mamy ref tam zostanie zastosowane
    const sliderPageWidth = slider.offsetWidth; // szerokość jednego slajdu
    // Math.ceil zaokrągla w górę do najbliższej liczby całkowitej - aby działało dobrze na wszystkich rozdzielczościach
    // scrollLeft i scrollWidth to właściwości sliderRef.current
    if (Math.ceil(slider.scrollLeft + sliderPageWidth) >= slider.scrollWidth) {
      slider.scrollTo({ left: 0 });
    } else {
      slider.scrollBy({ left: sliderPageWidth });
    }
  };

  const prev = () => {
      
    const slider = sliderRef.current;
    const sliderPageWidth = slider.offsetWidth;

    if (slider.scrollLeft <= 0) {
      slider.scrollTo({ left: slider.scrollWidth });
    } else {
      slider.scrollBy({ left: -sliderPageWidth });
  }
};
  // informacje o tym który timer pobierane są z funkcji next()
  const startAutoPlay = () => {
    sliderIntervalRef.current = setInterval(() => {
      next();
    }, 5000);
  };

  const stopAutoPlay = () => {
    clearInterval(sliderIntervalRef.current);
  };

  useEffect(() => {
    startAutoPlay();
    return stopAutoPlay;
  }, []);

  // reset timera po kliknięciu przycisku dla lepszego UX
  const handleNext = () => {
    stopAutoPlay();
    next();
    startAutoPlay();
  }

  return (
    <>
      <div ref={sliderRef} className="carousel w-full h-100">
        <div className="carousel-item relative w-full">
          <img
            src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
            className="w-full" />
          <div className="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between">
            <button onClick={prev} className="btn btn-circle">❮</button>
            <button onClick={handleNext} className="btn btn-circle">❯</button>
          </div>
        </div>
        <div className="carousel-item relative w-full">
          <img
            src="/images/other/Karuzela-dane.jpg"
            className="w-full" />
          <div className="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between">
            <button onClick={prev} className="btn btn-circle">❮</button>
            <button onClick={handleNext} className="btn btn-circle">❯</button>
          </div>
        </div>
        <div className="carousel-item relative w-full">
          <img
            src="https://img.daisyui.com/images/stock/photo-1665553365602-b2fb8e5d1707.webp"
            className="w-full" />
          <div className="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between">
            <button onClick={prev} className="btn btn-circle">❮</button>
            <button onClick={handleNext} className="btn btn-circle">❯</button>
          </div>
        </div>
      </div>

      <div className="container grid grid-cols-[30%_70%] items-center mx-auto my-10">
        <Bestseller/>
        <TopProducts/>
      </div>
      
      <PromotionSlider promotionId={1} />

    </>
  );
}

export default Home;
