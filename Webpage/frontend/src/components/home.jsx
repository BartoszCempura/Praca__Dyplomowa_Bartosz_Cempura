import PromotionSlider from "./promotionSlider";
import { useRef } from "react";

function Home() {

  const sliderRef = useRef(null);

  const next = () => {
    sliderRef.current.scrollBy({ left: sliderRef.current.offsetWidth, behavior: "smooth" });
  };

  const prev = () => {
    sliderRef.current.scrollBy({ left: -sliderRef.current.offsetWidth, behavior: "smooth" });
  };

  return (
    <>
      <div ref={sliderRef} className="carousel w-full h-100">
        <div className="carousel-item relative w-full">
          <img
            src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
            className="w-full" />
          <div className="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between">
            <button onClick={prev} className="btn btn-circle">❮</button>
            <button onClick={next} className="btn btn-circle">❯</button>
          </div>
        </div>
        <div className="carousel-item relative w-full">
          <img
            src="https://img.daisyui.com/images/stock/photo-1609621838510-5ad474b7d25d.webp"
            className="w-full" />
          <div className="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between">
            <button onClick={prev} className="btn btn-circle">❮</button>
            <button onClick={next} className="btn btn-circle">❯</button>
          </div>
        </div>
        <div className="carousel-item relative w-full">
          <img
            src="https://img.daisyui.com/images/stock/photo-1414694762283-acccc27bca85.webp"
            className="w-full" />
          <div className="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between">
            <button onClick={prev} className="btn btn-circle">❮</button>
            <button onClick={next} className="btn btn-circle">❯</button>
          </div>
        </div>
        <div className="carousel-item relative w-full">
          <img
            src="https://img.daisyui.com/images/stock/photo-1665553365602-b2fb8e5d1707.webp"
            className="w-full" />
          <div className="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between">
            <button onClick={prev} className="btn btn-circle">❮</button>
            <button onClick={next} className="btn btn-circle">❯</button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-[30%_70%] items-center my-10 gap-4">
        <div className="bg-base-100 p-4 text-center shadow-md">
          <h1 className="text-4xl font-bold">Bestseller</h1>
        </div>
        <div className="bg-base-100 p-4 text-center shadow-md">
          <h1 className="text-4xl font-bold">Top produkty tego miesiąca</h1>
        </div>
      </div>

      <PromotionSlider promotionId={1} />

    </>
  );
}

export default Home;
