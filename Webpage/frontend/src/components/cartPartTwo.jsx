import { getPaymentMethods, getDeliveryMethods, getUserAdresses } from "../utils/cartActions";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getCart } from "../utils/tempCartStorage";

function CartPartTwo() {
    const navigate = useNavigate();
    const [cartValue, setCartValue] = useState(0);

    const [paymentMethods, setPaymentMethods] = useState([]);
    const [selectedPayment, setSelectedPayment] = useState(null);

    const [deliveryMethods, setDeliveryMethods] = useState([]);
    const [selectedDelivery, setSelectedDelivery] = useState(null);

    const [ userAdresses, setUserAdresses ] = useState([]);
    const [ shippingAdress, setShippingAdress ] = useState(null);
    const [ billingAdress, setBillingAdress ] = useState(null);


    const fetchData = async () => {
        const dataPayment = await getPaymentMethods();
        const dataDelivery = await getDeliveryMethods();

        setPaymentMethods(dataPayment);
        setSelectedPayment(dataPayment[0]?.id || null);

        setDeliveryMethods(dataDelivery);
        setSelectedDelivery(dataDelivery[0]?.id || null);

        

        const tempCart = getCart(); //pracujemy nad tym !!!
        const total = Object.values(tempCart).reduce((sum, item) => {
          return sum + item.quantity_user * parseFloat(item.price_including_promotion);
        }, 0);

        setCartValue(total);
    };


    useEffect(() => {
        fetchData();

        const handler = () => fetchData();
        window.addEventListener("paymentsChange", handler);

        return () => window.removeEventListener("paymentsChange", handler);
    }, []);

    
    const handleSelectPayment = (methodId) => {
        setSelectedPayment(methodId);
    };
    const handleSelectDelivery = (methodId) => {
        setSelectedDelivery(methodId);
    };

    const handleSelectShippingAdress = (adressid) => {
        setShippingAdress(adressid);
    }

    return (
        <div className="contsiner grid grid-cols-[4fr_1fr] items-start gap-6 mx-60">
            <div className="flex flex-col items-center gap-4 my-10 w-full pr-18 bg-base-100">

                <div className="w-full bg-base-200 p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4">Adres dostawy</h2>
                </div>

                <div className="w-full rounded-lg bg-base-100">
                    <h2 className="text-xl font-semibold mb-4">Wybierz metodę dostawy:</h2>

                    <ul className="list bg-base-200 rounded-box shadow-md border-1 border-gray-900">

                        {deliveryMethods.map((method) => (
                            <li key={method.id} className="flex justify-between items-center p-4 mx-2">
                                <div classNAme="flex flex-col gap-2">
                                    <div className="font-semibold">{method.name}</div>
                                    <p className="text-gray-500">Przewidywany czas dostawy: {method.estimated_delivery_days} dni</p>
                                </div>
                                <div className="flex items-center gap-6">
                                    <p>Koszt: {method.fee}</p>                         
                                    <input
                                        type="checkbox"
                                        className="checkbox checkbox-sm bg-cyan-500 checked:bg-amber-500"
                                        checked={selectedDelivery === method.id}
                                        onChange={() => handleSelectDelivery(method.id)}
                                    />
                                </div>  
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="w-full rounded-lg bg-base-100 ">
                    <h2 className="text-xl font-semibold mb-4">Wybierz metodę płatności:</h2>

                    <ul className="list bg-base-200 rounded-box shadow-md border-1 border-gray-900">

                        {paymentMethods.map((method) => (
                            <li key={method.id} className="flex justify-between items-center p-4 mx-2">
                                <div className="font-semibold">{method.name}</div>
                                <div className="flex items-center gap-6">
                                     <p>Koszt: {method.fee}</p> 
                                    <img
                                        className="size-15 rounded-box object-contain"
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


            <aside className="bg-base-200 p-4 rounded-lg shadow-md my-10 border-1 border-gray-900">
                <div className="card-body items-center">
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