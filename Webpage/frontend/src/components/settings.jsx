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
        setAddresses(response.data || []);

        if (response.data && response.data.length > 0) {
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
};

  const handleDeleteAddress = async (id) => {
    if (!id) return;

    try {
        const response = await api.delete(`/user_management/addresses/${id}`); 

    } catch (err) {
    console.error(err);
    setMessage(err.response?.data?.error || "Coś poszło nie tak");
    }
  };

  const handleZipChange = (e) => {
    let value = e.target.value.replace(/\D/g, ""); // remove non-digits
    if (value.length > 2) {
        value = value.slice(0, 2) + "-" + value.slice(2, 5);
    }
    setZipCode(value);
    };

  const handleNipChange = (e) => {
  let value = e.target.value.replace(/\D/g, ""); // only digits

  if (value.length > 3) {
    value = value.slice(0, 3) + "-" + value.slice(3);
  }
  if (value.length > 10) {
    value = value.slice(0, 10) + "-" + value.slice(10);
  }
  value = value.slice(0, 12);

  setNip(value);
};


    return (
        <div className="container grid grid-cols-[1fr_3fr] bg-base-100 py-20 gap-6 mx-auto" style={{width:"60%"}}>

            <div className="card bg-base-200 shadow-md shadow-black/40 p-6 mb-6 border border-gray-900 lg:h-66 h-75">
                <h2 className="text-2xl font-bold text-center mb-6">Zapisane adresy:</h2>

                <div className="space-y-2">
                    <div className="flex flex-col items-center gap-4">
                    
                       <select defaultValue="Medium" className="select select-md">
                            {addresses.map(address => (
                                <option key={address.id} onClick={() => setSelectedAddress(address)}>{(address.title || `${address.street_name} ${address.city}`) + ` - ${address.type}`}</option>
                            ))}
                        </select>

                        <button className="btn btn-custom btn-block" onClick={() => document.getElementById("add_address").showModal()}>
                            Dodaj adress
                        </button>
                        <button className="btn btn-error text-white hover:opacity-90 mb-2" style={{ width: "151px" }} onClick={() => handleDeleteAddress(selectedAddress?.id)} disabled={!selectedAddress}>
                            Usuń adress
                        </button>
                    </div>
                </div>
            </div>


        <div className="card bg-base-200 shadow-md shadow-black/40 p-6 mb-6 border border-gray-900">
            <h2 className="text-2xl text-center font-bold mb-6">Szczegóły:</h2>

            <div className="space-y-2">

                {[
                { label: "Tytuł:", value: selectedAddress?.title || "-" },
                { label: "Nazwa firmy:", value: selectedAddress?.company_name || "-" },
                { label: "NIP:", value: selectedAddress?.nip || "-" },
                { label: "Osoba:", value: `${selectedAddress?.first_name} ${selectedAddress?.last_name}` },
                { label: "Ulica:", value: `${selectedAddress?.street_name} ${selectedAddress?.building_number}` },
                { label: "Nr mieszkania:", value: selectedAddress?.flat_number || "-" },
                { label: "Miasto:", value: selectedAddress?.city },
                { label: "Kod pocztowy:", value: selectedAddress?.zip_code }
                ].map((item, index) => (
                <div key={index} className="grid grid-cols-[150px_1fr_auto] gap-2 items-center">
                    <strong>{item.label}</strong>
                    <span>{item.value}</span>
                    <button className="btn btn-sm border-gray-600">Edytuj</button>
                </div>
                ))}

            </div>
        </div>

            {/*modal - dodawanie adresu*/}
            <dialog id="add_address" className="modal">
                <div className="modal-box">
                    <form method="dialog">
                        <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onClick={handleCloseModal} >✕</button>
                    </form>
                    <h3 className="font-bold text-lg text-center">Dodaj adres</h3>

                    <form onSubmit={handleAddAddress}>
                        <label className="label text-sm">Tytuł (opcjonalne):</label> 
                        <input type="text" className="input validator w-full mb-4" value={title} onChange={(e) => setTitle(e.target.value)}/>
                        <label className="label text-sm">Nazwa firmy (opcjonalnie):</label> 
                        <input type="text" className="input validator w-full mb-4" value={companyName} onChange={(e) => setCompanyName(e.target.value)}/>
                        <label className="label text-sm">NIP (opcjonalnie):</label> 
                        <input type="text" pattern="(^$|^[0-9]{3}-[0-9]{6}-[0-9]{1}$)" className="input validator w-full mb-4" value={nip} onChange={handleNipChange}/>
                        <div className="grid grid-cols-2 gap-4 mb-4">
                            <div className="w-full">
                                <label className="label text-sm">Imie:</label> 
                                <input type="text" className="input validator" value={firstName} onChange={(e) => setFirstName(e.target.value)}/>
                            </div>
                            <div className="w-full">
                                <label className="label text-sm">Nazwisko:</label>                       
                                <input type="text" className="input validator" value={lastName} onChange={(e) => setLastName(e.target.value)}/>
                            </div>
                        </div>
                        <div className="grid grid-cols-[3fr_1fr] gap-4 mb-4">
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