'use client';

import { useState } from 'react';
import { Candidate } from '@/types/candidate';
import CandidateCard from '@/components/CandidateCard';
import Link from 'next/link';

export default function SearchPage() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState<'name' | 'company' | 'skills'>('name');

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/candidates/search?query=${encodeURIComponent(searchQuery)}&type=${searchType}`
      );

      if (response.ok) {
        const data = await response.json();
        setCandidates(data.candidates || []);
      } else {
        console.error('Search failed');
        setCandidates([]);
      }
    } catch (error) {
      console.error('Error searching:', error);
      setCandidates([]);
    }
    setLoading(false);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <header className="border-b border-white/10 bg-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="text-2xl font-bold text-white">
                Trace
              </div>
            </div>
            <nav className="flex gap-4">
              <Link href="/" className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white transition-colors rounded-md hover:bg-white/5">
                Dashboard
              </Link>
              <Link href="/discover" className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white transition-colors rounded-md hover:bg-white/5">
                Discover
              </Link>
              <Link href="/search" className="px-4 py-2 text-sm font-medium text-white bg-white/10 transition-colors rounded-md">
                Search
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">
            Search Candidates
          </h1>
          <p className="text-xl text-gray-400">
            Find candidates by name, company, or skills
          </p>
        </div>

        {/* Search Interface */}
        <div className="bg-white/5 border border-white/10 rounded-lg p-8 mb-8">
          <div className="space-y-6">
            {/* Search Type Selector */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-3">
                Search By
              </label>
              <div className="flex gap-2">
                {(['name', 'company', 'skills'] as const).map((type) => (
                  <button
                    key={type}
                    onClick={() => setSearchType(type)}
                    className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                      searchType === type
                        ? 'bg-white text-black'
                        : 'bg-white/5 border border-white/10 text-gray-300 hover:bg-white/10'
                    }`}
                  >
                    {type.charAt(0).toUpperCase() + type.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            {/* Search Input */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Search Query
              </label>
              <div className="flex gap-3">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={`Search by ${searchType}...`}
                  className="flex-1 px-4 py-3 bg-black border border-white/10 rounded-md text-white placeholder-gray-500 focus:outline-none focus:border-white/30 transition-colors"
                />
                <button
                  onClick={handleSearch}
                  disabled={loading || !searchQuery.trim()}
                  className="px-8 py-3 bg-white text-black rounded-md hover:bg-gray-200 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Searching...' : 'Search'}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Results */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-white/20 border-r-white"></div>
            <p className="mt-4 text-gray-400">Searching candidates...</p>
          </div>
        ) : candidates.length > 0 ? (
          <div>
            <div className="mb-6">
              <p className="text-gray-400">
                Found <span className="text-white font-semibold">{candidates.length}</span> candidate{candidates.length !== 1 ? 's' : ''}
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {candidates.map((candidate) => (
                <CandidateCard key={candidate.id} candidate={candidate} />
              ))}
            </div>
          </div>
        ) : searchQuery && !loading ? (
          <div className="text-center py-12 bg-white/5 rounded-lg border border-white/10">
            <p className="text-gray-400 mb-4">No candidates found for "{searchQuery}"</p>
            <p className="text-sm text-gray-500">Try a different search term or discover new candidates</p>
            <Link
              href="/discover"
              className="inline-block mt-6 px-6 py-3 bg-white text-black rounded-md hover:bg-gray-200 transition-colors font-medium"
            >
              Discover Candidates
            </Link>
          </div>
        ) : null}

        {/* Search Tips */}
        <div className="mt-12 bg-white/5 border border-white/10 rounded-lg p-8">
          <h3 className="text-xl font-bold text-white mb-4">Search Tips</h3>
          <div className="space-y-3 text-gray-400">
            <p>
              <span className="text-white font-medium">Name:</span> Search for candidates by their full or partial name (e.g., "John Smith")
            </p>
            <p>
              <span className="text-white font-medium">Company:</span> Find candidates who have worked at specific companies (e.g., "Google", "OpenAI")
            </p>
            <p>
              <span className="text-white font-medium">Skills:</span> Search for candidates with specific technical skills or expertise
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 bg-black mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            Powered by Grok AI · Built with Next.js & Python
          </p>
        </div>
      </footer>
    </div>
  );
}
