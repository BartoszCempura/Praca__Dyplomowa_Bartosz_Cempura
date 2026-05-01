import { useEffect, useState } from "react";

function BackendLoader() {
    const [dots, setDots] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setDots((prev) => (prev +1) % 4);
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    return ( 
        <div className="flex items-center justify-center h-32 bg-white/80">
            <div className="text-center text-3xl font-semibold px-6 py-4">
                Budzenie backendu{Array(dots).fill(".").join("")}
            </div>
        </div>
    );
}

export default BackendLoader;