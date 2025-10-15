import { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function Menu() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const getCategories = async () => {
      try {
        const rootCategories = (await axios.get("/api/catalog/categories")).data; // przetwarzam dane response na json

        const categoriesWithTheirChildren = await Promise.all( //promise jest szybsze bo wykonuje wszystko na raz
          rootCategories.map(async (rootCategory) => {
            const childCategories = await axios.get(`/api/catalog/categories/${rootCategory.id}`);
            return { ...rootCategory, children: childCategories.data }; // spread operator (...) kopiuje wszystkie wlasciwosci rootCategory i dodaje nowe children
          })
        );

        setCategories(categoriesWithTheirChildren);
      } catch (err) {
        console.error("Unable to get categories:", err);
      }
    };

    getCategories();
  }, []);

  return (
    <div className="flex lg:justify-center bg-base-100 shadow-md">
      <ul className="menu lg:menu-horizontal rounded-box">
        {categories.map((category) => (
            <li key={category.id}>
            {category.children.length > 0 ? (
            <details>
              <summary className="px-8">{category.name}</summary>
              <ul className="relative z-50">
                {category.children.map((child) => (
                  <li key={child.id}>
                    <Link to={`/${child.slug}`} onClick={() => setSelectedCategorySlug(child.slug)}>
                      {child.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </details>
            ) : (
              <Link to={`/${category.slug}`} onClick={() => setSelectedCategorySlug(category.slug)}>
                {category.name}
              </Link>
            )}
          </li>
        ))}
      </ul>
  </div>
);
}

export default Menu;
