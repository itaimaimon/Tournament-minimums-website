interface ResultsProps {
  results: string;
}

export default function Results({ results }: ResultsProps) {
  return (
    <div className="mt-8 p-6 bg-white roundedxl shadow-xl border border-gray-200 space-y-4">
      <h2 className="text-2xl font-semibold text-gray-700">Results</h2>
      <div className="text-gray-800 text-lg">{results}</div>

      {/* TEMPLATE: Add multiple results or grid here */}
      {/*
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        <div className="p-3 bg-gray-50 rounded-lg shadow-sm">Result 1</div>
        <div className="p-3 bg-gray-50 rounded-lg shadow-sm">Result 2</div>
      </div>
      */}
    </div>
  );
}
