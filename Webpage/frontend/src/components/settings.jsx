import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/tokenHandler";

function Settings() {
    const [addresses, setAddresses] = useState([]);
    const [selectedAddress, setSelectedAddress] = useState(null);
    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState('');

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
    const [type, setType] = useState("Shipping");


    useEffect(() => {
    const fetchAddresses = async () => {
      try {
        const response = await api.get("/user_management/addresses");
        setAddresses(response.data);

        if (response.data.length > 0) {
            let defaultAddress = null;
            for (let i = 0; i < response.data.length; i++) {
                if (response.data[i].type === "Default") {
                    defaultAddress = response.data[i];
                    break;
                }
            }
            setSelectedAddress(defaultAddress || response.data[0]);
        }

      } catch (err) {
        console.error(err);
        alert(err.response?.data?.error || "Coś poszło nie tak");
      }
    };

    fetchAddresses();
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

    setMessage(response.data.message);
    setMessageType("success");
    document.getElementById("add_address").close();
    e.target.reset();
    } catch (err) {
    console.error(err);
    setMessageType("error");
    setMessage(err.response?.data?.error || "Coś poszło nie tak");
    e.target.reset();
    }
  };

    return (
        <div className="container grid grid-cols-[1fr_3fr] bg-base-100 py-20 gap-6 mx-auto">

            <div className="card bg-base-200 shadow-md shadow-black/40 p-6 mb-6 border border-gray-900">
                <h2 className="text-2xl font-bold text-center mb-6">Zapisane adresy:</h2>

                <div className="space-y-2">
                    <div className="flex flex-col items-center gap-4">
                    
                        {addresses.map(address => (
                            <button key={address.id} className={`w-full text-left p-2 rounded transition ${
                                    selectedAddress?.id === address.id 
                                    ? "bg-base-300" 
                                    : "hover:bg-base-300"
                                }`} onClick={() => setSelectedAddress(address)}>
                                <strong>Tytuł: </strong>{address.title || `${address.street_name} ${address.city}`}
                            </button>
                        ))}

                        <button className="btn btn-custom btn-block" onClick={() => document.getElementById("add_address").showModal()}>
                            Dodaj adres
                        </button>
                    </div>
                </div>
            </div>


            <div className="card bg-base-200 shadow-md shadow-black/40 p-6 mb-6 border border-gray-900">
                <h2 className="text-2xl font-bold text-center mb-6">Szczegóły:</h2>
                <div className="space-y-2">
                    <div className="flex justify-between">
                    <strong>Tytuł:</strong>
                    <span>{selectedAddress?.title}</span>
                    </div>

                    <div className="flex justify-between">
                    <strong>Ulica:</strong>
                    <span>
                        {selectedAddress?.street_name} {selectedAddress?.building_number}
                    </span>
                    </div>

                    <div className="flex justify-between">
                    <strong>Kod pocztowy:</strong>
                    <span>{selectedAddress?.zip_code}</span>
                    </div>

                    <div className="flex justify-between">
                    <strong>Miasto:</strong>
                    <span>{selectedAddress?.city}</span>
                    </div>
                </div>
            </div>

            <dialog id="add_address" className="modal">
                <div className="modal-box">
                    <form method="dialog">
                        <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
                    </form>
                    <h3 className="font-bold text-lg text-center">Dodaj adres</h3>

                    <form onSubmit={handleAddAddress}>
                        <label className="label text-sm">Tytuł (opcjonalne):</label> 
                        <input type="text" className="input validator w-full mb-4" value={title} onChange={(e) => setTitle(e.target.value)}/>
                        <label className="label text-sm">Nazwa firmy (opcjonalnie):</label> 
                        <input type="text" className="input validator w-full mb-4" value={companyName} onChange={(e) => setCompanyName(e.target.value)}/>
                        <label className="label text-sm">Imie:</label> 
                        <input type="text" className="input validator w-full mb-4" value={firstName} onChange={(e) => setFirstName(e.target.value)}/>
                        <label className="label text-sm">Nazwisko:</label> 
                        <input type="text" className="input validator w-full mb-4" value={lastName} onChange={(e) => setLastName(e.target.value)}/>
                        <label className="label text-sm">NIP (opcjonalnie):</label> 
                        <input type="text" className="input validator w-full mb-4" value={nip} onChange={(e) => setNip(e.target.value)}/>
                        <label className="label text-sm">Nazwa ulicy:</label> 
                        <input type="text" className="input validator w-full mb-4" value={streetName} onChange={(e) => setStreetName(e.target.value)}/>
                        <label className="label text-sm">Nr budynku</label> 
                        <input type="text" className="input validator w-full mb-4" value={buildingNumber} onChange={(e) => setBuildingNumber(e.target.value)}/>
                        <label className="label text-sm">Nr mieszkania (opcjonalnie)</label> 
                        <input type="text" className="input validator w-full mb-4" value={apartmentNumber} onChange={(e) => setApartmentNumber(e.target.value)}/>
                        <label className="label text-sm">Kod pocztowy:</label> 
                        <input type="text" className="input validator w-full mb-4" value={zipCode} onChange={(e) => setZipCode(e.target.value)}/>
                        <label className="label text-sm">Miasto:</label> 
                        <input type="text" className="input validator w-full mb-4" value={city} onChange={(e) => setCity(e.target.value)}/>
                        <label className="label text-sm">Typ adresu:</label> 
                        <select className="select select-bordered w-full" value={type} onChange={(e) => setType(e.target.value)}>
                            <option value="Shipping">Adres wysyłkowy</option>
                            <option value="Billing">Adres rozliczeniowy</option>
                            <option value="Default">Domyślny adres</option>
                        </select>

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
export default Settings;