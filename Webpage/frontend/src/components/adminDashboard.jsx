import { useEffect, useState} from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { getTopProducts } from "../utils/topProductsActions"
import { getTransactions } from "../utils/transactionsActions"

function AdminDashboard() {
  const [chartData, setChartData] = useState([]);
  const [topViewed, setTopViewed] = useState(null);
  const [mostPurchased, setMoustPurchased] = useState(null);
  const [kokpitSection, setKokpitSection ] = useState("products_popularity");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (kokpitSection === "products_popularity") {
      loadPopularityData();
    }
  }, [kokpitSection]);

  const loadPopularityData = async () => {
  setLoading(true);
  
  try {
    const data = await getTopProducts();
    
    if (data.topProducts.length === 0) {
      setChartData([]);
      return;
    }
    
    const rechartsData = data.topProducts.map((product) => ({
      name: product.name,
      score: parseFloat(product.popularity_score || 0),
      id: product.id
    }));

    const top_viewed = data.mostViewed
    setTopViewed(top_viewed)
    const most_puchased = data.mostPurchased
    setMoustPurchased(most_puchased)
    
    setChartData(rechartsData);
    
  } catch (err) {
    console.error(err);
    setChartData([]);
  } finally {
    setLoading(false);
  }
};

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const { name, id, score } = payload[0].payload;

    return (
      <div className="bg-base-200 p-3 rounded-lg shadow border border-gray-700">
        <p className="text-sm text-gray-400">ID: {id}</p>
        <p className="font-semibold">{name}</p>
        <p className="text-amber-500">Score: {score}</p>
      </div>
    );
  }

  return null;
};


  return (
    <>
      {/*-----------------tytuł strony ------------------------*/}
      <div className="bg-base-200 py-10">
        {kokpitSection === "products_popularity" && (
             <div className="flex flex-col gap-6 items-center">
              <h2 className="text-2xl font-bold">Popularność produktów</h2>
              <p className="text-gray-500">Top 20 produktów z ostatniego tygodnia</p>
            </div>
          )}
        {kokpitSection === "sales_list" && (
             <div className="flex flex-col gap-6 items-center">
              <h2 className="text-2xl font-bold">Wyniki sprzedaży</h2>
              <p>Lista produktów wraz z ilością sprzedanych sztuk - dodatkowo filtracjaod do wg daty</p>
            </div>
          )}
        {kokpitSection === "transaction_edit" && (
             <div className="flex flex-col gap-6 items-center">
              <h2 className="text-2xl font-bold">Transakcje</h2>
              <p>Lista transakcji - filtrowana po dacie z możliwością edycji</p>
            </div>
          )}
      </div>
      {/*---------------------------przestrzeń kokpitu-------------------------- */}
      <div className="grid grid-cols-[1fr_5fr] min-h-[80vh]">
        
        <aside className="bg-base-200">
          <div className="divider mb-6 px-4">
              <h2 className="font-bold text-lg">Menu</h2>
          </div> 
          <nav className="sticky top-0 py-5 flex flex-col gap-5 items-center">
            <button 
                type="button" 
                onClick={() => setKokpitSection("products_popularity")} 
                className={kokpitSection === "products_popularity" ? "btn btn-in-cart w-full" : "btn btn-custom w-full"}>
                Popularność
            </button>
            <button 
                type="button" 
                onClick={() => setKokpitSection("sales_list")} 
                className={kokpitSection === "sales_list" ? "btn btn-in-cart w-full" : "btn btn-custom w-full"}>
                Wyniki sprzedaży
            </button>
            <button 
                type="button" 
                onClick={() => setKokpitSection("transaction_edit")} 
                className={kokpitSection === "transaction_edit" ? "btn btn-in-cart w-full" : "btn btn-custom w-full"}>
                Transakcje
            </button>
            </nav>
        </aside>

        <div className="">

           {kokpitSection === "products_popularity" && (

            <div className="flex flex-col gap-6 p-20">
              {/* Loading */}
              {loading ? (
                <div className="flex justify-center items-center h-96">
                  <span className="loading loading-bars loading-lg text-primary"></span>
                </div>
              ) : chartData.length === 0 ? (
                <div className="text-center py-20">
                  <p className="text-xl text-gray-500">Brak danych</p>
                  <button onClick={loadPopularityData} className="btn btn-custom mt-4">
                    Odśwież
                  </button>
                </div>
              ) : (
                <>
                  {/* wykres */}
                  <div className="w-full rounded-xl p-5 border">
                    <ResponsiveContainer width="100%" aspect={2}> 
                      <BarChart data={chartData}> 
                        <CartesianGrid strokeDasharray="3 3" vertical />
                        <XAxis  hide={true}/>
                        <YAxis tick={{ fill: '#ffffff', fontSize: 14, fontWeight: 'bold', dx: -10}}/>
                        <Tooltip content={<CustomTooltip />} />
                        <Legend/>
                        <Bar dataKey="score" fill="#00E0FF" legendType="none" activeBar={{ fill: '#00A8CC' }}/>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>

                  {/* Podsumowanie danych */}
                  <div className="grid grid-cols-3 gap-4 text-center mt-10">
                    <div className="stat">
                      <div className="stat-title">Najpopularniejszy</div>
                      <div className="stat-value text-primary">{chartData[0].name} ( {chartData[0].score} )</div>
                    </div>
                    <div className="stat">
                      <div className="stat-title">Najczęściej kupowany</div>
                      <div className="stat-value text-secondary">
                        {mostPurchased.name} ( {mostPurchased.purchase_count} )
                      </div>
                    </div>
                    <div className="stat">
                      <div className="stat-title">Najczęściej oglądany</div>
                      <div className="stat-value">
                        {topViewed.name} ( {topViewed.view_count} )
                      </div>
                    </div>
                  </div>

                  {/* Przyciski */}
                  <div className="flex justify-center gap-4 pt-10 border-t">
                    <button onClick={loadPopularityData} className="btn btn-custom">
                      Odśwież
                    </button>
                  </div>
                </>
              )}
            </div>
          )}
          
          {kokpitSection === "sales_list" && (
            <p>Trwają prace</p>
          )}

          {kokpitSection === "transaction_edit" && (
            <p>Trwają prace</p>
          )}

        </div>
       
      </div>
    </>
  );
}

export default AdminDashboard;
