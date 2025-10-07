import React, { useState } from 'react';
import { fetchRagQuery, RagQueryResponse } from '../services/rag_query';

export default function Home() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<RagQueryResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    const res = await fetchRagQuery(query);
    setResponse(res);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-start py-10 text-gray-100">
      <h1 className="text-3xl font-bold mb-8 text-gray-100">Welcome to Socrates</h1>
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row items-center gap-4 w-full max-w-xl mb-8">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Enter your query..."
          className="w-full sm:w-80 px-4 py-2 border border-gray-700 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 bg-gray-800 text-gray-100 placeholder-gray-400"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 bg-blue-700 text-white rounded hover:bg-blue-800 transition disabled:opacity-50"
        >
          {loading ? 'Loading...' : 'Ask'}
        </button>
      </form>
      {response && (
        <div className="w-full max-w-xl bg-gray-800 rounded shadow p-6">
          <h3 className="text-xl font-semibold mb-4 text-gray-200">Response:</h3>
          {response.response?.content ? (
            <div className="mb-6">
              <span className="font-medium text-gray-300">AI Response:</span>
              <div className="bg-gray-900 p-4 rounded mt-2 text-gray-100 whitespace-pre-line border border-gray-700">
                {response.response.content}
              </div>
            </div>
          ) : response.error ? (
            <div className="text-red-400 font-semibold">{response.error}</div>
          ) : null}
          {response.context && response.context.length > 0 && (
            <div>
              <span className="font-medium text-gray-300">Context:</span>
              <ul className="list-disc pl-5 mt-2">
                {response.context.map((ctx: string, idx: number) => (
                  <li key={idx} className="mb-2">
                    <pre className="bg-gray-900 p-2 rounded text-gray-200 whitespace-pre-line break-words border border-gray-700">{ctx}</pre>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}