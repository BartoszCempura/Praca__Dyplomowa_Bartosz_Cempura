import { useEffect, useState} from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, LineChart, Line } from 'recharts';
import { getTopProducts } from "../utils/topProductsActions"
import { getTransactions, setTransactionStatus } from "../utils/transactionsActions"

function AdminDashboard() {
  const [kokpitSection, setKokpitSection ] = useState("products_popularity");
  const [loading, setLoading] = useState(false);

  const [chartData, setChartData] = useState([]);

  const [topViewed, setTopViewed] = useState(null);

  const [mostPurchased, setMoustPurchased] = useState(null);

  const [purchasedThisWeek, setPurchasedThisWeek] = useState([])
  const [selectedProductId, setSelectedProductId] = useState(null)
  const [selectedProductData, setSelectedProductData] = useState([])
  
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

  // operacje z użyciem algorytmu popularności
  useEffect(() => {
    if (kokpitSection === "products_popularity" || kokpitSection === "sales_list") {
      loadChartData();
    }
  }, [kokpitSection]);

  const loadChartData = async () => {
    setLoading(true);
    
    try {
      const data = await getTopProducts();
      
      if (data.topProducts.length === 0) {
        setChartData([]);
        return;
      }

      if (data.purchasedThisWeek.length === 0) {
        setPurchasedThisWeek([]);
        return;
      }
      
      const rechartsData = data.topProducts.map((product) => ({
        name: product.name,
        score: parseFloat(product.popularity_score || 0),
        id: product.id
      }));

      setChartData(rechartsData);

      setTopViewed(data.mostViewed)
   
      setMoustPurchased(data.mostPurchased)

      setPurchasedThisWeek(data.purchasedThisWeek)

      if (data.purchasedThisWeek.length > 0) {
        const firstProductId = data.purchasedThisWeek[0].id;
        setSelectedProductId(firstProductId);
        loadProductChartData(firstProductId);
      }
      
    } catch (err) {
      console.error(err);
      setChartData([]);
      setPurchasedThisWeek([]);
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
  
  const handleProductChange = (productId) => {
    setSelectedProductId(productId);
    loadProductChartData(productId);
  }

  const loadProductChartData = async (productId) => {
    setLoading(true);
  try {
    const productHistory = purchasedThisWeek.filter(
    item => item.id === parseInt(productId)  // 'id' zamiast 'product_id'
    );
    
    const chartData = productHistory.map(item => ({
      date: item.date,
      sold: item.count
    }));
    
    setSelectedProductData(chartData);
    } catch (err) {
      console.error(err);
      setSelectedProductData([]);
    } finally {
      setLoading(false);
    }
  };

  const uniqueProducts = [];
  const seenIds = new Set();
  purchasedThisWeek.forEach(item => {
    if (!seenIds.has(item.id)) {
      seenIds.add(item.id);
      uniqueProducts.push(item);
    }
  });

  return (
    <>
      {/*-----------------tytuł strony ------------------------*/}
      <div className="bg-base-200 py-10">
        {kokpitSection === "products_popularity" && (
             <div className="flex flex-col gap-6 items-center">
              <h2 className="text-2xl font-bold">Popularność produktów</h2>
            </div>
          )}
        {kokpitSection === "sales_list" && (
             <div className="flex flex-col gap-6 items-center">
              <h2 className="text-2xl font-bold">Wyniki sprzedaży produktów</h2>
            </div>
          )}
        {kokpitSection === "transaction_edit" && (
             <div className="flex flex-col gap-6 items-center">
              <h2 className="text-2xl font-bold">Transakcje</h2>
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

        <main className="">

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
                  <button onClick={loadChartData} className="btn btn-custom mt-4">
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
                    <button onClick={loadChartData} className="btn btn-custom">
                      Odśwież
                    </button>
                  </div>
                </>
              )}
            </div>
          )}
          
          {kokpitSection === "sales_list" && (
            <div className="flex flex-col gap-6 p-20">

              <div className="mb-6 flex gap-6">
                  <label className="label">Wybierz produkt:</label>
                  <select className="select select-bordered"
                  value={selectedProductId || ''}
                  onChange={(e) => handleProductChange(e.target.value)}
                  >
                    {uniqueProducts.map((product) => (
                    <option key={product.id} value={product.id}>
                      {product.name}
                    </option>
                    ))}
                  </select>
              </div>
              {/* Loading */}
              {loading ? (
                <div className="flex justify-center items-center h-96">
                  <span className="loading loading-bars loading-lg text-primary"></span>
                </div>
              ) : purchasedThisWeek.length === 0 ? (
                <div className="text-center py-20">
                  <p className="text-xl text-gray-500">Brak danych</p>
                  <button onClick={loadChartData} className="btn btn-custom mt-4">
                    Odśwież
                  </button>
                </div>
              ) : (
                <>
                  {/* wykres */}
                  <div className="w-full rounded-xl p-5 border">
                    <div className="w-full rounded-xl p-5 border">
                      <LineChart
                        style={{ 
                          width: '100%', 
                          maxWidth: '700px', 
                          height: '100%', 
                          maxHeight: '70vh', 
                          aspectRatio: 1.618 
                        }}
                        data={selectedProductData}
                        margin={{
                          top: 5,
                          right: 0,
                          left: 0,
                          bottom: 5,
                        }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis 
                          dataKey="date" 
                          angle={-45}
                          textAnchor="end"
                          height={80}
                        />
                        <YAxis 
                          width="auto"
                          label={{ value: 'Ilość zakupów', angle: -90, position: 'insideLeft' }}
                        />
                        <Tooltip />
                        <Legend />
                        <Line 
                          type="monotone" 
                          dataKey="sold" 
                          stroke="#00E0FF" 
                          strokeWidth={2}
                          activeDot={{ r: 8 }}
                        />
                      </LineChart>
                    </div>

                  </div>

                  {/* Przyciski */}
                  <div className="flex justify-center gap-4 pt-10 border-t">
                    <button onClick={loadChartData} className="btn btn-custom">
                      Odśwież
                    </button>
                  </div>
                </>
              )}
            </div>
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
                        <div key={transaction.id} className="card bg-base-200">
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
                                  disabled={transaction.status === 'Cancelled' || transaction.status === 'Completed'}
                                >
                                  <option value="Pending">Oczekujące</option>
                                  <option value="Shipped">Wysłane</option>
                                  <option value="Completed">Zakończone</option>
                                  <option value="Cancelled">Anulowane</option>
                                </select>
          
                              
                            </div>

                            <div className="divider my-1"></div>
                            
                            <div tabIndex={0} className="collapse bg-base-100 border-base-300 border">
                              <div className="collapse-title font-semibold my-0 text-center">Szczeguły</div>
                                <div className="collapse-content text-sm">

                                  <div className="divider mt-0"></div>

                                  {/* Products */}
                                  <div className="space-y-2 mx-5">
                                    <h4 className="font-semibold">Produkty:</h4>
                                    {transaction.producty.map((product) => (
                                      <div key={product.id} className="grid grid-cols-3 text-sm">
                                        <span className="text-start">ID: {product.product_id}</span>
                                        <span className="text-center">Ilość: {product.quantity}</span>
                                        <span className="text-end">{product.unit_price_with_discount} zł</span>
                                      </div>
                                    ))}
                                  </div>

                                  <div className="divider mb-3"></div>

                                  {/* Addresses */}
                                  <div className="grid grid-cols-2 gap-5 text-sm mx-5">
                                    <div className="text-end">
                                      <p className="font-semibold">Adres wysyłki:</p>
                                      <p>{transaction.shipping_address_data.first_name} {transaction.shipping_address_data.last_name}</p>
                                      <p>{transaction.shipping_address_data.street_name} {transaction.shipping_address_data.building_number}</p>
                                      <p>{transaction.shipping_address_data.zip_code} {transaction.shipping_address_data.city}</p>
                                    </div>
                                    <div className="text-start">
                                      <p className="font-semibold">Adres rozliczeniowy:</p>
                                      <p>{transaction.billing_address_data.first_name} {transaction.billing_address_data.last_name}</p>
                                      <p>{transaction.billing_address_data.street_name} {transaction.billing_address_data.building_number}</p>
                                      <p>{transaction.billing_address_data.zip_code} {transaction.billing_address_data.city}</p>
                                    </div>
                                  </div>

                                  <div className="divider mb-3"></div>

                                  {/* Total */}
                                  <div className="flex justify-center items-center mb-6 gap-5">
                                    <span className="font-bold text-xl test-end">Należność:</span>
                                    <span className="text-xl font-bold text-orange-400 text-start">
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

        </main>
       
      </div>
    </>
  );
}

export default AdminDashboard;
