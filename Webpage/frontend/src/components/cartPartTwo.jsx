import { getPaymentMethods } from "../utils/cartActions";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function CartPartTwo() {
    const navigate = useNavigate();
    const [cartValue, setCartValue] = useState(0);
    const [paymentMethods, setPaymentMethods] = useState([]);
    const [selectedPayment, setSelectedPayment] = useState(null);


    const fetchPayments = async () => {
            const data = await getPaymentMethods();
            setPaymentMethods(data);
            setSelectedPayment(data[0]);

    }

    useEffect(() => {
        fetchPayments();

        const handler = () => fetchPayments();
        window.addEventListener("paymentsChange", handler);

        return () => window.removeEventListener("paymentsChange", handler);
    }, []);

    
    const handleSelectPayment = (methodId) => {
        setSelectedPayment(methodId);
    };

    return (
        <div className="grid grid-cols-[4fr_1fr] gap-6 mx-28 bg-white">
            <div className="flex flex-col items-center gap-4 my-10 w-full pr-18 bg-blue-400">
                <div className="w-full bg-base-200 p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4">Adres dostawy</h2>
                </div>
                <div className="w-full bg-base-200 p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4">Metoda dostawy</h2>
                </div>
                <div className="w-full p-6 rounded-lg shadow-md bg-base-200">
                    <h2 className="text-xl font-semibold mb-4">Metoda płatności</h2>

                    <ul className="list bg-base-100 rounded-box shadow-md">
                        <li className="p-4 pb-2 text-xs opacity-60 tracking-wide">
                            Wybierz metodę płatności:
                        </li>

                        {paymentMethods.map((method) => (
                            <li key={method.id} className="flex justify-around items-center p-4">
                                <div className="font-medium">{method.name}</div>
                                <div className="flex items-center gap-6">
                                    <img
                                        className="size-10 rounded-box object-contain"
                                        src={method.image}
                                        alt={method.name}
                                    />

                                    <input
                                        type="checkbox"
                                        className="checkbox checkbox-sm bg-cyan-500 checked:bg-amber-500"
                                        checked={selectedPayment === method.id}
                                        onChange={() => handleSelectPayment(method.id)}
                                    />
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>               
            </div>


            <aside className="bg-base-200 p-4 max-h-screen overflow-y-auto rounded-lg shadow-md my-10 border-1 border-gray-900">
                <div className="card-body">
                <span className="text-info mb-2">
                    Wartość: {cartValue.toFixed(2)} zł
                </span>
                <div className="card-actions">
                    <button className="btn btn-custom btn-block" onClick={() => navigate(-1)}>Przejdź dalej</button>
                </div>
                </div>
            </aside>  

        </div>
    );
}
export default CartPartTwo;