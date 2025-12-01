import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/tokenHandler";

function Settings() {
    const [adresses, setAdresses] = useState([]);
    const [selectedAddress, setSelectedAddress] = useState(null);


    useEffect(() => {
    const fetchAdresses = async () => {
      try {
        const response = await api.get("/user_management/addresses");
        setAdresses(response.data);

        if (response.data.length > 0) {
            let defaultAddress = null;
            for (let i = 0; i < response.data.length; i++) {
                if (response.data[i].type === "default") {
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

    fetchAdresses();
  }, []);

  function handleAddAdress() {

  }

    return (
        <div className="container grid grid-cols-[1fr_3fr] bg-base-100 py-20 gap-6 mx-auto">

            <div className="card bg-base-200 shadow-md shadow-black/40 p-6 mb-6 border border-gray-900">
                <h2 className="text-2xl font-bold text-center mb-6">Zapisane adresy:</h2>
                <div className="space-y-2">
                <div className="flex justify-center">   
                    {adresses.length === 0 ? (
                        <button className="btn btn-custom btn-block" onClick={() => document.getElementById("add_address").showModal()}>Dodaj adres</button>
                    ) : (adresses.map(address => (
                    <button key={address.id} className={`w-full text-left p-2 rounded transition ${
                  selectedAddress?.id === address.id ? "bg-base-300" : "hover:bg-base-300"
                }`} onClick={() => setSelectedAddress(address)}><strong>Tytuł:</strong>{address.title || `${address.street_name} ${address.city}`}</button>
                    )))}
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
                <h3 className="font-bold text-lg">Potwierdzenie usunięcia konta</h3>
                <p className="py-4 mb-2">Czy na pewno chcesz usunąć swoje konto?</p>

                <form onSubmit={handleAddAdress}>
                    <input type="password" placeholder="Podaj hasło" className="input input-bordered w-full mb-" required/>
                    <div className="modal-action justify-center">
                    <button type="submit" className="btn btn-error text-white hover:opacity-90" style={{ width: "151px" }}>Usuń konto</button>
                    </div>
                </form>
                
                </div>
            </dialog>
    </div>

    );
}
export default Settings;