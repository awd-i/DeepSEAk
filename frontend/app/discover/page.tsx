'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import Link from 'next/link';

export default function DiscoverPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // GitHub discovery state
  const [githubQuery, setGithubQuery] = useState('machine learning');
  const [minFollowers, setMinFollowers] = useState(100);

  // X/Twitter discovery state
  const [xQuery, setXQuery] = useState('AI engineer');
  const [minXFollowers, setMinXFollowers] = useState(1000);

  const discoverFromGitHub = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/candidates/discover/github`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: githubQuery,
          min_followers: minFollowers,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || 'Failed to discover candidates');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    }

    setLoading(false);
  };

  const discoverFromX = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/candidates/discover/x`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: xQuery,
          min_followers: minXFollowers,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || 'Failed to discover candidates');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    }

    setLoading(false);
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
              <Link href="/discover" className="px-4 py-2 text-sm font-medium text-white bg-white/10 transition-colors rounded-md">
                Discover
              </Link>
              <Link href="/search" className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white transition-colors rounded-md hover:bg-white/5">
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
            Discover Talent
          </h1>
          <p className="text-xl text-gray-400">
            Find engineering talent from GitHub and X using AI-powered discovery
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          {/* GitHub Discovery */}
          <div className="bg-white/5 border border-white/10 rounded-lg p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-white text-black rounded-lg flex items-center justify-center text-2xl font-bold">
                GH
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">GitHub</h2>
                <p className="text-sm text-gray-400">Search by repository topics</p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Search Query
                </label>
                <input
                  type="text"
                  value={githubQuery}
                  onChange={(e) => setGithubQuery(e.target.value)}
                  placeholder="e.g., machine learning, react, python"
                  className="w-full px-4 py-3 bg-black border border-white/10 rounded-md text-white placeholder-gray-500 focus:outline-none focus:border-white/30 transition-colors"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Minimum Followers
                </label>
                <input
                  type="number"
                  value={minFollowers}
                  onChange={(e) => setMinFollowers(Number(e.target.value))}
                  className="w-full px-4 py-3 bg-black border border-white/10 rounded-md text-white focus:outline-none focus:border-white/30 transition-colors"
                />
              </div>

              <button
                onClick={discoverFromGitHub}
                disabled={loading}
                className="w-full px-6 py-3 bg-white text-black rounded-md hover:bg-gray-200 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Discovering...' : 'Discover from GitHub'}
              </button>
            </div>
          </div>

          {/* X/Twitter Discovery */}
          <div className="bg-white/5 border border-white/10 rounded-lg p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-white text-black rounded-lg flex items-center justify-center text-2xl font-bold">
                𝕏
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">X (Twitter)</h2>
                <p className="text-sm text-gray-400">Search by keywords</p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Search Query
                </label>
                <input
                  type="text"
                  value={xQuery}
                  onChange={(e) => setXQuery(e.target.value)}
                  placeholder="e.g., AI engineer, ML researcher"
                  className="w-full px-4 py-3 bg-black border border-white/10 rounded-md text-white placeholder-gray-500 focus:outline-none focus:border-white/30 transition-colors"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Minimum Followers
                </label>
                <input
                  type="number"
                  value={minXFollowers}
                  onChange={(e) => setMinXFollowers(Number(e.target.value))}
                  className="w-full px-4 py-3 bg-black border border-white/10 rounded-md text-white focus:outline-none focus:border-white/30 transition-colors"
                />
              </div>

              <button
                onClick={discoverFromX}
                disabled={loading}
                className="w-full px-6 py-3 bg-white text-black rounded-md hover:bg-gray-200 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Discovering...' : 'Discover from X'}
              </button>
            </div>
          </div>
        </div>

        {/* Results */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-6 mb-8">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {result && (
          <div className="bg-white/5 border border-white/10 rounded-lg p-8">
            <h3 className="text-xl font-bold text-white mb-4">Discovery Results</h3>
            <div className="space-y-2">
              <p className="text-gray-300">
                <span className="font-medium text-white">Candidates Found:</span> {result.candidates_found || 0}
              </p>
              <p className="text-gray-300">
                <span className="font-medium text-white">Added to Database:</span> {result.candidates_added || 0}
              </p>
              {result.message && (
                <p className="text-gray-400 mt-4">{result.message}</p>
              )}
            </div>
            <Link
              href="/"
              className="inline-block mt-6 px-6 py-3 bg-white text-black rounded-md hover:bg-gray-200 transition-colors font-medium"
            >
              View Candidates
            </Link>
          </div>
        )}

        {/* Info Section */}
        <div className="mt-12 bg-white/5 border border-white/10 rounded-lg p-8">
          <h3 className="text-xl font-bold text-white mb-4">How Discovery Works</h3>
          <div className="space-y-3 text-gray-400">
            <p>
              <span className="text-white font-medium">GitHub:</span> Searches for repositories matching your query and discovers their top contributors based on stars and activity.
            </p>
            <p>
              <span className="text-white font-medium">X (Twitter):</span> Finds influential engineers and researchers in the tech community based on follower count and engagement.
            </p>
            <p className="text-sm text-gray-500 mt-4">
              Note: Discovery uses AI to analyze profiles and automatically scores candidates based on their experience, contributions, and impact.
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
