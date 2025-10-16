function Home() {
  return (
    <div className="flex flex-col items-center mt-10">
      <h1 className="text-4xl font-bold mb-4">Witamy w sklepie TechTown!</h1>
      <p className="text-gray-600 mb-10">
        Wybierz kategorię z menu powyżej, aby zobaczyć produkty.
      </p>
      <img
        src="/assets/banner.jpg"
        alt="Banner"
        className="rounded-xl shadow-lg w-3/4"
      />
    </div>
  );
}

export default Home;
