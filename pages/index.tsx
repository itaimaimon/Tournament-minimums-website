import { useState } from "react";
import Results from "../components/Results";

interface FormData {
  numPlayers: number;
  targetTop: number;
  numMatches: number| null;
  gamesPerMatch: number;
  pointsPerWin: number;
  pointsPerTie: number;
  pointsPerLoss: number;
  tiebreakers: boolean [];
  lastMatchIsDraw: boolean;
  numUncomp: number;
  probLastGameTiesBetweenComp: number;
  probLastGameTiesBetweenUncomp: number;
  probLastGameTiesBetweenMismatched: number;
  probGameWinBetweenMismatched: number;
  monteCarloChosen: boolean;
  monteCarloIterations: number;
  // Add more variables here
  // exampleVariable?: number;
}

export default function Home() {
  const [formData, setFormData] = useState<FormData>({
    numPlayers: 16,
    numMatches: null, // 4,
    gamesPerMatch: 3,
    targetTop: 8, //8,
    pointsPerWin: 3, //3,
    pointsPerTie: 1, //1,
    pointsPerLoss: 0, //0,
    tiebreakers: [true,true,true], // ['omw','gw','ogw'],
    lastMatchIsDraw: true, //true,
    numUncomp: 0, //0,
    probLastGameTiesBetweenComp: .1, //.1,
    probLastGameTiesBetweenUncomp: .1, //.1,
    probLastGameTiesBetweenMismatched: .05, //.05,
    probGameWinBetweenMismatched: .6, //.6,
    monteCarloChosen: true,
    monteCarloIterations: 11, //0.10

  });
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [showSuperAdvanced, setShowSuperAdvanced] = useState(false);
  const [results, setResults] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (key: keyof FormData, value: number) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };



  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("/api/calc", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (!res.ok) throw new Error("API request failed");
      const data = await res.json();
      setResults(data.result);
    } catch (err) {
      console.error(err);
      setResults("Error calculating results. Check console.");
    }
      finally {
        setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-gray-100 flex flex-col items-center justify-start py-12 px-4">
      <h1 className="text-4xl md:text-5xl font-extrabold text-gray-800 mb-8 font-sans">
        MTG Tournament Calculator
      </h1>

      <div className="w-full max-w-3xl bg-white rounded-3xl shadow-2xl p-8 space-y-6">
        <form onSubmit={handleSubmit} className=" advanced-options w-full h-auto overflow-visible space-y-6">
          {/* Basic Section */}
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold text-gray-700 border-b pb-2 mb-4">
              Basic Options
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-gray-50 rounded-xl shadow-inner">
                <label className="block font-medium text-gray-700 mb-1">
                  Number of Players
                </label>
                <input
                  type="number"
                  value={formData.numPlayers}
                  onChange={(e) =>
                    setFormData({...formData,
                    numPlayers: Number(e.target.value),
                    })
                  }
                  placeholder="e.g. 16"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 focus:outline-none transition"
                />
              </div>
              <div className="p-4 bg-gray-50 rounded-xl shadow-inner">
                <label className="block font-medium text-gray-700 mb-1">Number of Matches</label>
                <input
                  type="number"
                  value={formData.numMatches ?? ""}
                  onChange={(e) =>
                    setFormData({...formData,
                    numMatches: e.target.value === "" ? null : Number(e.target.value),
                    })
                  }
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 focus:outline-none transition"
                  placeholder="If left empty is Ceiling(log_2(players))"
                />
              </div>
              <div className="p-4 bg-gray-50 rounded-xl shadow-inner">
                <label className="block font-medium text-gray-700 mb-1">Target Top N</label>
                <input
                  type="number"
                  value={formData.targetTop}
                  onChange={(e) =>
                    setFormData({...formData,
                    targetTop: Number(e.target.value),
                    })
                  }
                  placeholder="e.g. 8"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 focus:outline-none transition"
                />
              </div>
              <div className="p-4 bg-gray-50 rounded-xl shadow-inner">
                <label className="block font-medium text-gray-700 mb-1">Games per Match</label>
                <input
                  type="number"
                  value={formData.gamesPerMatch}
                  onChange={(e) =>
                    setFormData({...formData,
                    gamesPerMatch: Number(e.target.value),
                    })
                  }
                  placeholder="e.g. 3"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 focus:outline-none transition"
                />
              </div>
            </div>
          </div>

          {/* Advanced Toggle */}
          <button
            type="button"
            onClick={() => {setShowAdvanced(!showAdvanced); setShowSuperAdvanced(false);} }
            className="text-blue-600 font-medium hover:underline transition"
          >
            {showAdvanced ? "Hide Advanced Options" : "Show Advanced Options"}
          </button>

          {/* Advanced Section */}
          <div
            className={`transition-all duration-500 overflow-hidden ${
            showAdvanced ? "max-h-[2000px] mt-4" : "max-h-0"
            }`}
          >
            <div className="p-4 rounded-xl shadow-inner bg-gray-50 space-y-4">
              <h2 className="text-xl font-semibold text-gray-700 border-b pb-1 mb-2">
                Advanced Options
              </h2>
              <div className="grid sm:grid-cols-1 md:grid-cols-2 gap-4">
                
                
                  <div className="col-span-2 p-3 bg-white rounded-lg shadow-sm">
                  <label className="block font-medium text-gray-700 mb-1">Point Allocation</label>

                  <div className="grid grid-cols-3 gap-3">
                    <div>
                      <label className="block text-xs text-gray-500">Win</label>
                      <input
                        type="number"
                        value={formData.pointsPerWin ?? ""}
                        onChange={(e) =>
                          setFormData({ ...formData, pointsPerWin: Number(e.target.value) })
                        }
                        className="w-full px-1 py-1 rounded-md border-gray-300 focus:ring-2 focus:ring-blue-400 focus:outline-none transition sm:text-sm"
                        placeholder="e.g. 3"
                      />
                    </div>
                  <div>
                    <label className="block text-xs text-gray-500">Loss</label>
                    <input
                      type="number"
                      value={formData.pointsPerLoss ?? ""}
                      onChange={(e) =>
                        setFormData({ ...formData, pointsPerLoss: Number(e.target.value) })
                      }
                    className="w-full px-1 py-1 rounded-md border-gray-300 focus:ring-2 focus:ring-blue-400 focus:outline-none transition sm:text-sm"
                    placeholder="e.g. 0"
                    />
                  </div>
                  <div>
                    <label className="block text-xs text-gray-500">Tie</label>
                    <input
                      type="number"
                      value={formData.pointsPerTie ?? ""}
                      onChange={(e) =>
                        setFormData({ ...formData, pointsPerTie: Number(e.target.value) })
                      }
                      className="w-full px-1 py-1 rounded-md border-gray-300 focus:ring-2 focus:ring-blue-400 focus:outline-none transition sm:text-sm"
                      placeholder="e.g. 1"
                    />
                  </div>
                </div>
              </div>
                
              <div className="p-3 bg-white rounded-lg shadow-sm">
                <label className="block font-medium text-gray-700 mb-1">Tiebreakers</label>
                {["Opponent Match Win%", "Game Win%", "Opponent Game Win%"].map(
                  (label, index) => (
                    <label key={index} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={formData.tiebreakers[index]}
                        onChange={(e) => {
                          const newTiebreakers = [...formData.tiebreakers];
                          newTiebreakers[index] = e.target.checked;
                          setFormData({ ...formData, tiebreakers: newTiebreakers });
                        }}
                      />
                      <span>{label}</span>
                    </label>
                  )
                )}
              </div>
                
                
              <div className="p-3 bg-white rounded-lg shadow-sm">
                <label className="block font-medium text-gray-700 mb-1">Is the last match Normal?</label>
                  <select
                    id="allowLastRoundDraw"
                    value={formData.lastMatchIsDraw ? "Draws" : "Normal"}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        lastMatchIsDraw: e.target.value === "Draws",
                      })
                    }
                    className="w-full rounded-lg border p-2"
                  >
                    <option value="Draws"> Players draw to both make the top N</option>
                    <option value="Normal"> Players play normally</option>
                  </select>
              </div>   
      {/* super Advanced Toggle */}
        <button
          type="button"
          onClick={() => setShowSuperAdvanced(!showSuperAdvanced)}
          className="text-blue-600 font-medium hover:underline transition"
        >
          {showSuperAdvanced ? "Hide Super Advanced Options" : "Show Super Advanced Options"}
        </button>
            
        {/* Super Advanced Section */}
        <div
            className={`col-span-2 transition-all duration-500 overflow-hidden ${
            showSuperAdvanced ? "max-h-[2000px] mt-4" : "max-h-0"
            }`}
        >
          <div className=" advanced-options w-full h-auto overflow-visible p-4 rounded-xl shadow-inner bg-gray-50 space-y-4">
            <h2 className=" text-xl font-semibold text-gray-700 border-b pb-1 mb-2">
              Super Advanced Options
            </h2>
            <div className="grid sm:grid-cols-1 md:grid-cols-2 gap-4">
            
            <div className="p-3 bg-white rounded-lg shadow-sm">
                  <label className="block font-medium text-gray-700 mb-1"> Number of Uncompetitive decks in Tournament</label>
                  <input
                    type="number"
                    value={formData.numUncomp ?? ""}
                    onChange={(e) => handleChange("numUncomp", Number(e.target.value))}
                    placeholder="0"
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 focus:outline-none transition"
                  />
              </div>

            <div className="p-3 bg-white rounded-lg shadow-sm">
                  <label className="block font-medium text-gray-700 mb-1"> Probability of Game Win for Comp. against Uncomp.</label>
                  <input
                    type="number"
                    value={formData.probGameWinBetweenMismatched ?? ""}
                    onChange={(e) => handleChange("probGameWinBetweenMismatched", Number(e.target.value))}
                    placeholder="e.g. 0.6"
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 focus:outline-none transition"
                  />
            </div>


            <div className=" col-span-2 p-3 bg-white rounded-lg shadow-sm">
                  <label className="block font-medium text-gray-700 mb-1">Probability of Last Game Timing out to a Draw</label>

                  <div className="grid grid-cols-3 gap-3">
                    <div>
                      <label className="block text-xs text-gray-500">Both Comp.</label>
                      <input
                        type="number"
                        value={formData.probLastGameTiesBetweenComp ?? ""}
                        onChange={(e) =>
                          setFormData({ ...formData, probLastGameTiesBetweenComp: Number(e.target.value) })
                        }
                        className="w-full px-1 py-1 rounded-md border-gray-300 focus:ring-2 focus:ring-blue-400 focus:outline-none transition sm:text-sm"
                        placeholder="e.g. 0.1"
                      />
                    </div>
                  <div>
                    <label className="block text-xs text-gray-500">Both Uncomp.</label>
                    <input
                      type="number"
                      value={formData.probLastGameTiesBetweenUncomp ?? ""}
                      onChange={(e) =>
                        setFormData({ ...formData, probLastGameTiesBetweenUncomp: Number(e.target.value) })
                      }
                      className="w-full px-1 py-1 rounded-md border-gray-300 focus:ring-2 focus:ring-blue-400 focus:outline-none transition sm:text-sm"
                      placeholder="e.g. 0.1"
                    />
                  </div>
                  <div>
                    <label className="block text-xs text-gray-500">Mismatched</label>
                    <input
                      type="number"
                      value={formData.probLastGameTiesBetweenMismatched ?? ""}
                      onChange={(e) =>
                        setFormData({ ...formData, probLastGameTiesBetweenMismatched: Number(e.target.value) })
                      }
                      className="w-full px-1 py-1 rounded-md border-gray-300 focus:ring-2 focus:ring-blue-400 focus:outline-none transition sm:text-sm"
                      placeholder="e.g. .05"
                    />
                  </div>
                </div>
              </div>

            <div className="p-3 bg-white rounded-lg shadow-sm">
              <label className="block font-medium text-gray-700 mb-1">Use Monte-Carlo? (More accurate but a little slower)</label>
                <input
                  type="checkbox"
                    checked={formData.monteCarloChosen}
                      onChange={(e) => {
                        setFormData({ ...formData, monteCarloChosen: e.target.checked });
                        }}
                />
            </div>

            <div className="p-3 bg-white rounded-lg shadow-sm">
              <label className="block font-medium text-gray-700 mb-1"> Number of Monte-Carlo Iterations (odd)</label>
              <input
                type="number"
                value={formData.monteCarloIterations ?? ""}
                onChange={(e) => handleChange("monteCarloIterations", Number(e.target.value))}
                placeholder="If even we add 1 to make median pretty"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 focus:outline-none transition"
              />
            </div>




                {/* TEMPLATE: Add more advanced inputs here */}
                {/*
                <div className="p-3 bg-white rounded-lg shadow-sm">
                  <label className="block font-medium text-gray-700 mb-1">Example Advanced Variable</label>
                  <input
                    type="number"
                    value={formData.exampleVariable || 0}
                    onChange={(e) => handleChange("exampleVariable", Number(e.target.value))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 focus:outline-none transition"
                  />
                </div>
                */}
              </div>
            </div>
          </div>
         </div>
        </div>
      </div> 
      <button
          type="submit"
          className={`w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 flex items-center justify-center`}
          disabled={loading} // disables button while calculating
        >
          {loading ? (
            <svg
              className="animate-spin h-5 w-5 mr-2 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
              ></path>
            </svg>
          ) : null}
          {loading ? "Calculating..." : "Calculate"}
        </button>
        </form>
        
        {/* Results Section */}
        {results && <Results results={results} />}
      </div>

      <footer className="mt-12 text-gray-500 text-sm">
        &copy; 2025 MTG Calculator
      </footer>
    </div>
  );
}
