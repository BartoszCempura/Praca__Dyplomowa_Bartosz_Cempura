import { useState, useEffect } from 'react'
import reactLogo from './assets/LOGO.svg'
import './App.css'
import axios from 'axios'

function App() {
  const [count, setCount] = useState(0)
  const [productData, setProductData] = useState(null);

  const fetchAPI = async () => {
    const response = await axios.get('/api/catalog/products/2'); 
    setProductData(response.data);
  };

  useEffect(() => {
    fetchAPI();
  }, []);

  return (
    <>
      <div>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1 class="kolor">Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
         <div className="bg-red-500 text-white p-4 mt-4 rounded">
          {productData && (
            <div>
              <h2 className="text-xl font-bold mb-2">
                {productData.product.name}
              </h2>
              <img
                src={productData.product.image}
                alt={productData.product.name}
                className="w-64 rounded mb-4"
              />
              <p className="text-sm mb-2">
                <strong>Category:</strong> {productData.product.category_name}
              </p>
              <p className="text-sm mb-4">{productData.product.description}</p>
              <p className="font-semibold">
                💰 Price: {productData.product.price_including_promotion} zł
              </p>

              <h3 className="mt-4 font-bold text-lg">Specifications:</h3>
              <ul className="list-disc ml-5 text-sm">
                {productData.attributes.map((attr, index) => (
                  <li key={index}>
                    <strong>{attr.name}:</strong> {attr.value}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
