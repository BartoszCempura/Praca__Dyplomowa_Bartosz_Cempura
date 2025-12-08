import { useEffect, useState } from "react";
import api from "../api/tokenHandler";
import { getAddressess, checkIfDefaultIsSet } from "../utils/daneDoZamowieniaActions";
import AddressCard from "./addressCard";

function DaneDoZamowien() {
    const [addresses, setAddresses] = useState([]);

    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState('');

    const [defaultExists, setDefaultExists] = useState(false);

    const [title, setTitle] = useState("");
    const [companyName, setCompanyName] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [nip, setNip] = useState("");
    const [streetName, setStreetName] = useState("");
    const [buildingNumber, setBuildingNumber] = useState("");
    const [apartmentNumber, setApartmentNumber] = useState("");
    const [zipCode, setZipCode] = useState("");
    const [city, setCity] = useState("");
    const [type, setType] = useState("Shipping"); // był problem z dodawaniem adresu domyślnego przy usunięciu wszystkich adresów z listy - chyba nie występuje


    const fetchAddresses = async () => {
        const data = await getAddressess();
        setAddresses(data);

        const exists = await checkIfDefaultIsSet();
        setDefaultExists(exists);
    };

    useEffect(() => {
        fetchAddresses();

        const handler = () => fetchAddresses();
        window.addEventListener("addressesChange", handler);

        return () => window.removeEventListener("addressesChange", handler);
    }, []);

    const handleAddAddress = async (e) => {
        e.preventDefault(); // submit nie przeładowuje strony
        setMessage("");

        try {
            const response = await api.post("/user_management/addresses", {
                title,
                company_name: companyName,
                first_name: firstName,
                last_name: lastName,
                nip,
                street_name: streetName,
                building_number: buildingNumber,
                flat_number: apartmentNumber,
                zip_code: zipCode,
                city,
                type,
        });

        window.dispatchEvent(new Event("addressesChange"));
        document.getElementById("add_address").close();
        e.target.reset();
        handleCloseModal();
        } catch (err) {
        console.error(err);
        setMessageType("error");
        setMessage(err.response?.data?.error || "Coś poszło nie tak");
        e.target.reset();
        }
    };

    const handleCloseModal = () => {
        setTitle("");
        setCompanyName("");
        setFirstName("");
        setLastName("");
        setNip("");
        setStreetName("");
        setBuildingNumber("");
        setApartmentNumber("");
        setZipCode("");
        setCity("");
        setMessage("");
        setMessageType("");
        setType("Shipping");
    };


    const handleZipChange = (e) => {
        let value = e.target.value.replace(/\D/g, ""); // tylko liczby
        if (value.length > 2) {
            value = value.slice(0, 2) + "-" + value.slice(2, 5);
        }
        setZipCode(value);
    };

    const handleNipChange = (e) => {
        let value = e.target.value.replace(/\D/g, ""); // tylko liczby

        if (value.length > 3) {
            value = value.slice(0, 3) + "-" + value.slice(3);
        }
        if (value.length > 10) {
            value = value.slice(0, 10) + "-" + value.slice(10);
        }
        value = value.slice(0, 12);

        setNip(value);
    };

    const billingAddresses = addresses.filter(a => a.type === "Billing");
    const nonBillingAddresses = addresses.filter(a => a.type !== "Billing"); // a co jak adres będzie typu other?? 

    return (
        <div className="container py-20 mx-auto" style={{ width: "60%" }}>

            {/* Adresy wysyłkowe / domyślne */}
            <div>
                <h2 className="divider text-2xl font-bold text-center mb-10">Adresy wysyłkowe:</h2>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch mb-10">
                    {nonBillingAddresses.length > 0 ? (
                    nonBillingAddresses.map(a => <AddressCard key={a.id} {...a} />)
                    ) : (
                        <span className="col-span-full block text-center my-15">Brak dodanych adresów</span>
                    )}
                </div>
            </div>

            {/* Adresy rozliczeniowe */}
            <div>
                <h2 className="divider text-2xl font-bold text-center mb-10">Adresy rozliczeniowe:</h2>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch mb-10">
                    {billingAddresses.length > 0 ? (
                    billingAddresses.map(a => <AddressCard key={a.id} {...a} />)
                    ) : (
                        <span className="col-span-full block text-center my-15">Brak dodanych adresów</span>
                    )}
                </div>
            </div>

            <div className="flex justify-center">
                <button className="btn btn-custom btn-block" onClick={() => document.getElementById("add_address").showModal()}>
                    Dodaj adres
                </button>
            </div>


            {/*modal - dodawanie adresu*/}
            <dialog id="add_address" className="modal">
                <div className="modal-box">
                    <form method="dialog">
                        <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onClick={handleCloseModal} >✕</button>
                    </form>
                    <h3 className="font-bold text-lg text-center">Dodaj adres</h3>

                    <form onSubmit={handleAddAddress}>
                        <label className="label text-sm">Typ adresu:</label>
                        <select className="select select-bordered w-full mb-4" value={type} onChange={(e) => setType(e.target.value)}>
                            <option value="Shipping">Wysyłkowy</option>
                            <option value="Billing">Rozliczeniowy</option>
                            {!defaultExists && (
                            <option value="Default">Domyślny</option>
                             )}
                        </select>
                        <label className="label text-sm">Tytuł (opcjonalne):</label> 
                        <input type="text" className="input validator w-full mb-4" value={title} onChange={(e) => setTitle(e.target.value)}/>
                        {type === "Billing" && (
                        <>
                            <label className="label text-sm">Nazwa firmy (opcjonalnie):</label> 
                            <input type="text" className="input validator w-full mb-4" value={companyName} onChange={(e) => setCompanyName(e.target.value)}/>
                            <label className="label text-sm">NIP (opcjonalnie):</label> 
                            <input type="text" pattern="(^$|^[0-9]{3}-[0-9]{6}-[0-9]{1}$)" className="input validator w-full mb-4" value={nip} onChange={handleNipChange}/>
                        </>
                        )}
                        <div className="grid grid-cols-2 gap-4 mb-4">
                            <div className="w-full">
                                <label className="label text-sm">Imie (opcjonalne):</label> 
                                <input type="text" className="input validator" value={firstName} onChange={(e) => setFirstName(e.target.value)}/>
                            </div>
                            <div className="w-full">
                                <label className="label text-sm">Nazwisko (opcjonalne):</label>                       
                                <input type="text" className="input validator" value={lastName} onChange={(e) => setLastName(e.target.value)}/>
                            </div>
                        </div>
                        <div className="grid grid-cols-[5fr_2fr] gap-4 mb-4">
                            <div className="w-full">               
                                <label className="label text-sm">Nazwa ulicy:</label> 
                                <input type="text" className="input validator" value={streetName} onChange={(e) => setStreetName(e.target.value)}/>
                            </div> 
                            <div className="w-full">
                                <label className="label text-sm">Nr. budynku</label> 
                                <input type="number" inputMode="numeric" max={99999} className="input validator" value={buildingNumber} onChange={(e) => setBuildingNumber(e.target.value)}/>
                            </div>
                        </div>
                        <label className="label text-sm">Nr. mieszkania (opcjonalne)</label> 
                        <input type="number" inputMode="numeric" max={99999} className="input validator w-full mb-4" value={apartmentNumber} onChange={(e) => setApartmentNumber(e.target.value)}/> 
                        <div className="grid grid-cols-[4fr_2fr] gap-4 mb-4">
                            <div className="w-full">
                                <label className="label text-sm">Miasto:</label> 
                                <input type="text" className="input validator" value={city} onChange={(e) => setCity(e.target.value)}/>
                            </div>
                            <div className="w-full">
                                <label className="label text-sm">Kod pocztowy:</label> 
                                <input type="text" pattern="(^$|^[0-9]{2}-[0-9]{3}$)" className="input validator" value={zipCode} onChange={handleZipChange}/>       
                            </div>
                        </div> 
                        <div className="modal-action justify-center">
                            <button type="submit" className="btn btn-custom btn-block">Zapisz</button>
                        </div>
                    </form>

                    {message && (
                    <p className={`mt-4 text-center ${messageType === 'success' ? 'text-green-600' : ''} ${messageType === 'error' ? 'text-red-600' : ''}`}>
                        {message}
                    </p>
                    )}
                
                </div>
            </dialog>
    </div>

    );
}
export default DaneDoZamowien;