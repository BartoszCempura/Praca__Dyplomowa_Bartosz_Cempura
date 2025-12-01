import api from "../api/tokenHandler";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function CartDeliveryPaymentAdress() {
    const navigate = useNavigate();
    const [cartValue, setCartValue] = useState(0);

    return (
        <div className="grid grid-cols-[4fr_1fr] gap-6 items-start mx-28">
            <div className="flex flex-col items-center gap-4 my-10 w-full pr-18">
                <div className="w-full bg-base-200 p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4">Adres dostawy</h2>
                </div>
                <div className="w-full bg-base-200 p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4">Metoda dostawy</h2>
                </div>
                <div className="w-full bg-base-200 p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4">Metoda płatności</h2>
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
export default CartDeliveryPaymentAdress;