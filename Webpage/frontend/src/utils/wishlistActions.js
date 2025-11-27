import api, { isAuthenticated } from "../api/tokenHandler";


export async function getWishlist() {

  if (!isAuthenticated()) {
    alert("Musisz być zalogowany, aby zobaczyć listę ulubionych!");
    window.location.href = "/login";
    return;
  }

    try {
        const response = await api.get("/commerce/wishlists");
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
}; 

export async function addToWishlist(id) {

  if (!isAuthenticated()) {
    alert("Musisz być zalogowany, aby dodać produkt do ulubionych!");
    window.location.href = "/login";
    return;
  }

  try {
    await api.post("/commerce/wishlists", {product_id: id});
    window.dispatchEvent(new Event("wishlistChange"));
  } catch (err) {
    console.error(err);
    if (err.response?.status === 401) {
      alert("Sesja wygasła. Zaloguj się ponownie.");
    } else {
      alert(err.response?.data?.error || "Coś poszło nie tak");
    }
  }
}

export async function removeFromWishlist(id) {

    try {
        await api.delete(`/commerce/wishlists/${id}`);
        window.dispatchEvent(new Event("wishlistChange"));
    } catch (err) {
        console.error(err);
        if (err.response?.status === 401) {
            alert("Sesja wygasła. Zaloguj się ponownie.");
        } else {
            alert(err.response?.data?.error || "Coś poszło nie tak");
        }
    }
}