import { useState } from "react";


interface Props {
  setResults: (res: string) => void;
}

export default function TournamentForm({ setResults }: Props) {
  const [numPlayers, setNumPlayers] = useState(16);
  const [targetTop, setTargetTop] = useState(8);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent page reload
    const res = await fetch("/api/calc", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ numPlayers, targetTop }),
    });
    const data = await res.json();
    setResults(data.result);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md space-y-4">
      <div>
        <label>Number of Players:</label>
        <input
          type="number"
          value={numPlayers}
          onChange={(e) => setNumPlayers(Number(e.target.value))}
          className="border p-2 rounded ml-2"
        />
      </div>
      <div>
        <label>Target Top N:</label>
        <input
          type="number"
          value={targetTop}
          onChange={(e) => setTargetTop(Number(e.target.value))}
          className="border p-2 rounded ml-2"
        />
      </div>
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
        Calculate
      </button>
    </form>
  );
}
