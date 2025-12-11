import { getPaymentMethods, getDeliveryMethods, getUserAdresses } from "../utils/cartActions";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getCart } from "../utils/tempCartStorage";
import AddressCard from "./addressCard";

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
        const dataAdresses = await getUserAdresses();

        setPaymentMethods(dataPayment);
        setSelectedPayment(dataPayment[0]?.id || null);

        setDeliveryMethods(dataDelivery);
        setSelectedDelivery(dataDelivery[0]?.id || null);

        setUserAdresses(dataAdresses);

        const defaultAdress = dataAdresses.find(a => a.type === "Default");
        setShippingAdress(defaultAdress || null);
        setBillingAdress(defaultAdress || null);

        const tempCart = getCart(); //pracujemy nad tym !!!
        const total = Object.values(tempCart).reduce((sum, item) => {
          return sum + item.quantity_user * parseFloat(item.price_including_promotion);
        }, 0);

        setCartValue(total);
    };


    useEffect(() => {
        fetchData();

        const handler = () => fetchData();

        window.addEventListener("addressesChange", handler);
        window.addEventListener("paymentsChange", handler);

        return () => {
            window.removeEventListener("addressesChange", handler);
            window.removeEventListener("paymentsChange", handler);
        };
    }, []);

    
    const handleSelectPayment = (methodId) => {
        setSelectedPayment(methodId);
    };
    const handleSelectDelivery = (methodId) => {
        setSelectedDelivery(methodId);
    };

    const handleSelectShippingAdress = (addressId) => {
        const selected = userAdresses.find(a => a.id === addressId);
        setShippingAdress(selected);
    };

    const handleSelectBillingAdress = (addressId) => {
        const selected = userAdresses.find(a => a.id === addressId);
        setBillingAdress(selected);
    };


    //jak dam wybieranie adresu z listy
    const billingAddresses = userAdresses.filter(a => a.type === "Billing");
    const shippingAddresses = userAdresses.filter(a => 
        a.type === "Shipping" || a.type === "Default"
    );

    return (
        <div className="container grid grid-cols-[4fr_1fr] items-start gap-6 mx-60">
            <div className="flex flex-col items-center gap-6 my-10 w-full pr-18 bg-base-100">

                <div className="flex w-full rounded-lg bg-red-500">
                    <div className="flex mx-auto gap-20 bg-white">
                        {/* Adres dostawy - zawsze wyświetlany */}
                        <div>
                            <h2 className="text-xl font-semibold mb-4">Adres dostawy:</h2>
                            {shippingAdress ? (
                                <AddressCard variant="summary" {...shippingAdress} />
                            ) : (
                                <div className="card justify-center items-center bg-base-200 h-full shadow-md hover:shadow-black/40 transition-shadow duration-100 w-full border border-gray-900 p-5">
                                    <button className="btn btn-custom btn-block" onClick={() => navigate('/dane-do-zamowien')}>
                                        Dodaj
                                    </button>
                                </div>
                            )}
                        </div>

                        {/* Adres rozliczeniowy - 3 scenariusze */}
                        <div>
                            <h2 className="text-xl font-semibold mb-4">Adres rozliczeniowy:</h2>
                            
                            {/* Scenariusz 1: billingAdress jest null */}
                            {!billingAdress ? (
                                <div className="card justify-center items-center bg-base-200 h-full shadow-md hover:shadow-black/40 transition-shadow duration-100 w-full border border-gray-900 p-5">
                                    <button className="btn btn-custom btn-block" onClick={() => navigate('/dane-do-zamowien')}>
                                        Dodaj
                                    </button>
                                </div>
                            ) : (
                                /* Scenariusz 2 i 3: billingAdress istnieje */
                                shippingAdress && billingAdress.id === shippingAdress.id ? (
                                    /* Scenariusz 2: billingAdress === shippingAdress */
                                    <div className="card justify-center items-center bg-amber-400 h-full shadow-md hover:shadow-black/40 transition-shadow duration-100 border border-gray-900 p-5">
                                        <button className="btn btn-custom btn-block" onClick={() => document.getElementById("select_address").showModal()}>
                                            Zmień adres
                                        </button>
                                    </div>
                                ) : (
                                    /* Scenariusz 3: billingAdress !== shippingAdress */
                                    <AddressCard variant="summary" {...billingAdress} />
                                )
                            )}
                        </div>
                    </div>
                </div>

                <div className="w-full rounded-lg bg-base-100">
                    <h2 className="text-xl font-semibold mb-4">Wybierz metodę dostawy:</h2>

                    <ul className="list bg-base-200 rounded-box shadow-md border-1 border-gray-900">

                        {deliveryMethods.map((method) => (
                            <li key={method.id} className="flex justify-between items-center p-4 mx-2">
                                <div className="flex flex-col gap-2">
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
                 <div className="card-actions">
                    <button className="btn btn-custom btn-block" onClick={() => navigate(-1)}>Powrót</button>
                </div>
                </div>
            </aside>  



            <dialog id="select_address" className="modal">
                <div className="modal-box">
                    
                    <form method="dialog">
                        <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
                            ✕
                        </button>
                    </form>

                    <h3 className="font-bold text-lg text-center mb-4">Dodaj adres</h3>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
                        {shippingAddresses.map((address) => (
                            <div 
                                key={address.id}
                                className={`cursor-pointer rounded-lg hover:bg-base-200 ${
                                    shippingAdress?.id === address.id ? "ring-2 ring-amber-500" : ""
                                }`}
                                onClick={() => handleSelectShippingAdress(address.id)}
                            >
                                <AddressCard variant="summary" {...address} />
                            </div>
                        ))}
                    </div>

                </div>
            </dialog>


        </div>
    );
}
export default CartPartTwo;