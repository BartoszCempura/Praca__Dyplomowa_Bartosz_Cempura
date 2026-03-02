import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/tokenHandler";

function Menu() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const getCategories = async () => {
      try {
        const response = await api.get("/catalog/categories");
        const categories = response.data;

        setCategories(categories);
      } catch (err) {
        console.error("Ups nie udało się pobrać kategorii:", err);
      }
    };

    getCategories();
  }, []);

 return (
  <div className="flex justify-center bg-base-200 shadow-md relative z-40"> 
  {/*TODO:  Warto by było dodac skłądanie menu do jednej ikony dla lepszej responsywności */}
    {categories.map((category) => (
      <div key={category.id} className="dropdown dropdown-hover">
        {/* Warunek if/else czy kategoria ma podkategorie */}
        {category.children.length > 0 ? (
          <>
            {/* Przycisk rozwijający menu */}
            <div tabIndex={0} role="button" className="btn btn-ghost m-2">
              {category.name}
            </div>

            {/* Dropdown z podkategoriami */}
            <ul tabIndex={-1} className="dropdown-content menu bg-base-100 rounded-box z-50 w-52 p-2 shadow-sm left-0">
              {category.children.map((child) => (
                <li key={child.id}>
                  <Link to={`/${child.slug}`} onClick={() => setSelectedCategorySlug(child.slug)}>
                    {child.name}
                  </Link>
                </li>
              ))}
            </ul>
          </>
        ) : (
          // Kategoria bez podkategorii
          <Link to={`/${category.slug}`} onClick={() => setSelectedCategorySlug(category.slug)} className="btn btn-ghost m-2">
            {category.name}
          </Link>
        )}
      </div>
    ))}
  </div>
);
}

export default Menu;
