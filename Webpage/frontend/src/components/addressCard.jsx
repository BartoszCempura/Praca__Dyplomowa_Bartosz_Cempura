import { deleteAddress, setDefaultAddress } from "../utils/daneDoZamowieniaActions";


function AddressCard({id, title, company_name, first_name, last_name, nip, street_name, building_number, flat_number, zip_code, city, type}) {
    

    const handleDeleteAddress = () => {
        deleteAddress(id);
    };

    const handleDefaultChange = async () => {
        if (type !== "Default") {
            await setDefaultAddress(id);
        }
    };

    const handleEditAddress = () => {
        alert("Na tę chwile brak implementacji :(");
    }

    return (
        <div className="card bg-base-200 shadow-md hover:shadow-black/40 transition-shadow duration-100 w-70 border border-gray-900 p-5">
            <div className="flex flex-col space-y-2 flex-grow">

                {/* Tytuł */}
                {title && (
                    <h3 className="font-medium text-center">
                        {title}
                    </h3>
                )}

                {/* Nazwa firmy */}
                {company_name && (
                    <p className="font-medium">{company_name}</p>
                )}

                {/* NIP */}
                {nip && <p>NIP: {nip}</p>}

                {/* Osoba */}
                {(first_name || last_name) && (
                    <p>
                        {first_name} {last_name}
                    </p>
                )}

                {/* Ulica */}
                {(street_name || building_number) && (
                    <p>
                        {street_name} {building_number}
                        {flat_number ? `/${flat_number}` : ""}
                    </p>
                )}

                {/* Miasto */}
                {(zip_code || city) && (
                    <p>
                        {zip_code} {city}
                    </p>
                )}

                <div className="card-actions mt-auto justify-between items-center pt-4">
                    <label className="flex items-center gap-2 cursor-pointer">
                        <span className="text-sm">Domyślny</span>
                        <input
                            type="checkbox"
                            checked={type === "Default"}
                            onChange={handleDefaultChange}
                            className="checkbox checkbox-sm bg-cyan-500 checked:bg-amber-500"
                        />
                    </label>
                    <div className="flex gap-4">
                        <button type="button" className="btn btn-outline btn-sm"  onClick={handleEditAddress}>Edytuj</button>
                        <button type="button" className="btn btn-outline btn-sm" onClick={handleDeleteAddress}>Usuń</button>
                    </div>
                    
                </div>
            </div>
        </div>
    );
}

export default AddressCard;
