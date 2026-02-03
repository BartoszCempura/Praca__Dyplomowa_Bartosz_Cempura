import { useEffect, useState} from "react";

function AdminDashboard() {
  const [product, setProduct] = useState(null);

  useEffect(() => {
    async function load() {
      const data = await getTopProducts();
      setProduct(data.mostPurchased || null);
    }
    load();
  }, []);


  return (
      <div className="flex justify-center">
        <p className="text-xl">Kokpit</p>
      </div>
  );
}

export default AdminDashboard;
