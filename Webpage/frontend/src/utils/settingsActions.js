import api, { isAuthenticated } from "../api/tokenHandler";

export async function getAddressess() {

    if (!isAuthenticated()) {
        alert("Musisz być zalogowany, aby zobaczyć ustawienia!");
        window.location.href = "/login";
        return;
      }

      try {
        const response = await api.get("/user_management/addresses");
        return response.data || [];
      } catch (err) {
            console.error(err);
            if (err.response?.status === 401) {
                alert("Sesja wygasła. Zaloguj się ponownie.");
            } else {
                alert(err.response?.data?.error || "Coś poszło nie tak");
            }
            return [];
      }
}

export async function deleteAddress(id) {

    if (!id) return;

      try {
        await api.delete(`/user_management/addresses/${id}`);
        window.dispatchEvent(new Event("addressesChange"));
      } catch (err) {
            console.error(err);
            if (err.response?.status === 401) {
                alert("Sesja wygasła. Zaloguj się ponownie.");
            } else {
                alert(err.response?.data?.error || "Coś poszło nie tak");
            }
      }
}


export async function setDefaultAddress(id) {
    try {
        await api.patch(`/user_management/addresses/${id}/type`, { 
            type: "Default" 
        });
        window.dispatchEvent(new Event("addressesChange"));
    } catch (err) {
        console.error(err);
        alert(err.response?.data?.error || "Coś poszło nie tak");
    }
}
