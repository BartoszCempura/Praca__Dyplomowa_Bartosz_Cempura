import { useEffect, useState} from "react";
import { getTopProducts } from "../utils/topProductsActions"

function AdminDashboard() {
  const [topProducts, setToProduct] = useState([]);
  const [kokpitSection, setKokpitSection ] = useState("products_popularity")

  useEffect(() => {
    async function loadTopProducts() {
      const data = getTopProducts()
      setToProduct(data);
    }
    loadTopProducts();
  }, []);


  return (
      <div className="grid grid-cols-[1fr_4fr] min-h-[80vh]">
        
        <aside className="bg-green-500">
          <nav className="sticky top-0 py-10 flex flex-col gap-5 items-center">
            <button 
                type="button" 
                onClick={() => setKokpitSection("products_popularity")} 
                className={kokpitSection === "products_popularity" ? "btn btn-in-cart w-full btn-sm" : "btn btn-custom w-full btn-sm"}>
                Popularność produktów
            </button>
            <button 
                type="button" 
                onClick={() => setKokpitSection("sales_list")} 
                className={kokpitSection === "sales_list" ? "btn btn-in-cart w-full btn-sm" : "btn btn-custom w-full btn-sm"}>
                Wyniki sprzedaży
            </button>
            <button 
                type="button" 
                onClick={() => setKokpitSection("transaction_edit")} 
                className={kokpitSection === "transaction_edit" ? "btn btn-in-cart w-full btn-sm" : "btn btn-custom w-full btn-sm"}>
                Transakcje
            </button>
            </nav>
        </aside>

        <div className="container bg-red-500">

           {kokpitSection === "products_popularity" && (
            <div className="flex flex-col gap-6 items-center bg-yellow-500">
              <h2 className="text-2xl font-bold mt-10">Popularność produktów</h2>
              <p>Wykres słupkowy popularności - ładuje 20 i strzałka ładuje kolejne 20</p>
            </div>
           )}
          
          {kokpitSection === "sales_list" && (
             <div className="flex flex-col gap-6 items-center">
              <h2 className="text-2xl font-bold mt-10">Wyniki sprzedaży</h2>
              <p>Lista produktów wraz z ilością sprzedanych sztuk - dodatkowo filtracjaod do wg daty</p>
            </div>
          )}

          {kokpitSection === "transaction_edit" && (
             <div className="flex flex-col gap-6 items-center">
              <h2 className="text-2xl font-bold mt-10">Transakcje</h2>
              <p>Lista transakcji - filtrowana po dacie z możliwością edycji</p>
            </div>
          )}

        </div>
       
      </div>
  );
}

export default AdminDashboard;
