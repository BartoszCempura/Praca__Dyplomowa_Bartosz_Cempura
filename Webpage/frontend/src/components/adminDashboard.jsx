import { useEffect, useState} from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { getTopProducts } from "../utils/topProductsActions"
import { getTransactions, setTransactionStatus } from "../utils/transactionsActions"

function AdminDashboard() {
  const [kokpitSection, setKokpitSection ] = useState("products_popularity");
  const [loading, setLoading] = useState(false);

  const [chartData, setChartData] = useState([]);
  const [topViewed, setTopViewed] = useState(null);
  const [mostPurchased, setMoustPurchased] = useState(null);
  
  const [transactions, setTransactions] = useState([])
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    pages: 1,
    hasNext: false,
    hasPrev: false
  });
  const [filters, setFilters] = useState({
    status: '',
    date_from: '',
    date_to: '',
    page: 1,
    limit: 20
  });

  // elementy dla wykresów
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

  // elementy dla transakcji
  useEffect(() => {
      loadTransactions();
    }, [filters]);

  const loadTransactions = async () => {
      setLoading(true);
      
      try {
        const data = await getTransactions(filters);
        
        setTransactions(data.transactions);
        setPagination({
          total: data.total,
          page: data.page,
          pages: data.pages,
          hasNext: data.hasNext,
          hasPrev: data.hasPrev
        });
        
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value,
      page: 1 
    }));
  };

  const handlePageChange = (newPage) => {
    setFilters(prev => ({
      ...prev,
      page: newPage
    }));
  };

    const handleStatusChange = async (id, status) => {
      const success = await setTransactionStatus (id, status);
      if (success) {
        await loadTransactions();
      }
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
            <div className="py-15 px-20">

              {/* Filters */}
              <div className="mb-6 flex gap-6">

                <div className="mb-6">
                  <label className="label">Filtruj po statusie</label>
                  <select 
                    className="select select-bordered" 
                    value={filters.status}
                    onChange={(e) => handleFilterChange('status', e.target.value)}
                  >
                    <option value="">Wszystkie</option>
                    <option value="Pending">Oczekujące</option>
                    <option value="Shipped">Wysłane</option>
                    <option value="Completed">Zakończone</option>
                    <option value="Cancelled">Anulowane</option>
                  </select>
                </div>

                <div>
                  <label className="label">Data od</label>
                  <input type="date" className="input input-bordered" value={filters.date_from}
                    onChange={(e) => handleFilterChange('date_from', e.target.value)}/>
                </div>

                <div>
                  <label className="label">Data do</label>
                  <input type="date" className="input input-bordered" value={filters.date_to}
                    onChange={(e) => handleFilterChange('date_to', e.target.value)}/>
                </div>

                <button className="btn btn-error text-white self-center" onClick={() =>
                 setFilters({
                    status: '',
                    date_from: '',
                    date_to: '',
                    page: 1,
                    limit: 20
                  })}>
                  Wyczyść
                </button>

              </div>

              {/* Loading */}
              {loading ? (
                <div className="flex justify-center py-20">
                  <span className="loading loading-spinner loading-lg"></span>
                </div>
              ) : (
                <>
                  {/* Transactions List */}
                  <div className="space-y-5">
                    {transactions.length === 0 ? (
                      <p className="text-center text-gray-500 py-10">Brak transakcji</p>
                    ) : (
                      transactions.map((transaction) => (
                        <div key={transaction.id} className="card bg-base-200 shadow">
                          <div className="card-body">

                            <div className="flex justify-between items-start">

                              {/* Nagłówek */}
                              <div className="flex gap-6">
                                <div className="flex flex-col">
                                  <p className="font-bold">Transakcja <span className="text-gray-500">#{transaction.id}</span></p>
                                  <p className="font-bold">
                                    Rejestracja: <span className="text-gray-500">{transaction.created_at}</span>
                                  </p>
                                </div>
                                <div className="flex flex-col">
                                  <p className="font-bold">Użytkownik: <span className="text-gray-500">{transaction.user.first_name} {transaction.user.last_name}</span></p>
                                  <p className="font-bold">Kontakt: <span className="text-gray-500">Tel: {transaction.user.phone_number} Email: {transaction.user.email}</span></p>
                                </div>
                              </div>

                              {/* Status */}
                              <select
                                className="select select-bordered select-sm"
                                value={transaction.status}
                                onChange={(e) => handleStatusChange(transaction.id, e.target.value)}
                              >
                                <option value="Pending">Oczekujące</option>
                                <option value="Shipped">Wysłane</option>
                                <option value="Completed">Zakończone</option>
                                <option value="Cancelled">Anulowane</option>
                              </select>
                              
                            </div>

                            <div className="divider my-0"></div>

                            {/* Products */}
                            <div className="space-y-2">
                              <h4 className="font-semibold">Produkty:</h4>
                              {transaction.producty.map((product) => (
                                <div key={product.id} className="flex justify-between text-sm">
                                  <span>ID: {product.product_id}</span>
                                  <span>Ilość: {product.quantity}</span>
                                  <span>{product.unit_price_with_discount} zł</span>
                                </div>
                              ))}
                            </div>

                            <div className="divider my-0"></div>

                            {/* Addresses */}
                            <div className="grid grid-cols-2 gap-5 text-sm">
                              <div>
                                <p className="font-semibold">Adres wysyłki:</p>
                                <p>{transaction.shipping_address_data.first_name} {transaction.shipping_address_data.last_name}</p>
                                <p>{transaction.shipping_address_data.street_name} {transaction.shipping_address_data.building_number}</p>
                                <p>{transaction.shipping_address_data.zip_code} {transaction.shipping_address_data.city}</p>
                              </div>
                              <div>
                                <p className="font-semibold">Adres rozliczeniowy:</p>
                                <p>{transaction.billing_address_data.first_name} {transaction.billing_address_data.last_name}</p>
                                <p>{transaction.billing_address_data.street_name} {transaction.billing_address_data.building_number}</p>
                                <p>{transaction.billing_address_data.zip_code} {transaction.billing_address_data.city}</p>
                              </div>
                            </div>

                            <div className="divider my-0"></div>

                            {/* Total */}
                            <div className="flex justify-center items-center my-4">
                              <span className="font-bold text-xl mr-5">Należność:</span>
                              <span className="text-xl font-bold text-orange-400 ml-5">
                                {transaction.total_transaction_value} zł
                              </span>
                            </div>

                            {transaction.notes && (
                              <div className="mt-3 p-5 bg-base-300 rounded">
                                <p className="text-sm"><strong>Notatki:</strong> {transaction.notes}</p>
                              </div>
                            )}
                          </div>
                        </div>
                      ))
                    )}
                  </div>

                  {/* Pagination */}
                  {pagination.pages > 1 && (
                    <div className="flex justify-center items-center gap-4 mt-8">
                      <button 
                        className="btn btn-sm"
                        disabled={!pagination.hasPrev}
                        onClick={() => handlePageChange(filters.page - 1)}
                      >
                        ← Poprzednia
                      </button>

                      <span className="text-sm">
                        Strona {pagination.page} z {pagination.pages}
                      </span>

                      <button 
                        className="btn btn-sm"
                        disabled={!pagination.hasNext}
                        onClick={() => handlePageChange(filters.page + 1)}
                      >
                        Następna →
                      </button>
                    </div>
                  )}

                  {/* Stats */}
                  <div className="text-center text-sm text-gray-500 mt-4">
                    Wyświetlono {transactions.length} z {pagination.total} transakcji
                  </div>
                </>
              )}
            </div>
          )}

        </div>
       
      </div>
    </>
  );
}

export default AdminDashboard;
