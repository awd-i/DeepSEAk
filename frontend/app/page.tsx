'use client';

import React, { useState, useEffect } from 'react';
import Scene from '../components/Scene';
import { api } from '../lib/api';

// Mock data for development
const MOCK_CANDIDATES = [
  {
    id: '0',
    name: 'Dr. Alex Chen',
    current_title: 'Distinguished Engineer',
    current_company: 'Google DeepMind',
    priority_tier: 'top',
    score: { total_score: 98 },
    experiences: [
      { title: 'Distinguished Engineer', company: 'Google DeepMind', duration_months: 20 },
      { title: 'Principal Scientist', company: 'OpenAI', duration_months: 30 },
      { title: 'Tech Lead', company: 'Tesla AI', duration_months: 24 }
    ],
    github_profile: { top_languages: ['Python', 'C++', 'CUDA', 'Rust', 'Julia'] },
    notes: 'World-class AI researcher and systems architect. Pioneer in large-scale distributed training. Published 50+ papers in top ML conferences. Led teams building state-of-the-art foundation models.',
    linkedin_url: 'https://linkedin.com/in/alexchen',
    x_profile: { url: 'https://x.com/alexchen' }
  },
  {
    id: '1',
    name: 'Sarah Chen',
    current_title: 'Senior Software Engineer',
    current_company: 'Meta',
    priority_tier: 'top',
    score: { total_score: 92 },
    experiences: [
      { title: 'Senior Software Engineer', company: 'Meta', duration_months: 24 },
      { title: 'Software Engineer', company: 'Google', duration_months: 36 },
      { title: 'Junior Developer', company: 'Startup Inc', duration_months: 18 }
    ],
    github_profile: { top_languages: ['TypeScript', 'Python', 'Rust', 'Go'] },
    notes: 'Exceptional full-stack engineer with strong systems design experience. Led migration of critical services to microservices architecture.',
    linkedin_url: 'https://linkedin.com/in/sarahchen',
    x_profile: { url: 'https://x.com/sarahchen' }
  },
  {
    id: '2',
    name: 'Marcus Johnson',
    current_title: 'Staff Engineer',
    current_company: 'Stripe',
    priority_tier: 'top',
    score: { total_score: 88 },
    experiences: [
      { title: 'Staff Engineer', company: 'Stripe', duration_months: 18 },
      { title: 'Senior Engineer', company: 'Airbnb', duration_months: 30 },
      { title: 'Software Engineer', company: 'Amazon', duration_months: 24 }
    ],
    github_profile: { top_languages: ['JavaScript', 'Java', 'Kotlin', 'Swift'] },
    notes: 'Infrastructure specialist with deep expertise in payment systems and distributed computing. Known for excellent mentorship.',
    linkedin_url: 'https://linkedin.com/in/marcusjohnson',
    x_profile: { url: 'https://x.com/marcusj' }
  },
  {
    id: '3',
    name: 'Priya Patel',
    current_title: 'Engineering Manager',
    current_company: 'Uber',
    priority_tier: 'high',
    score: { total_score: 85 },
    experiences: [
      { title: 'Engineering Manager', company: 'Uber', duration_months: 20 },
      { title: 'Tech Lead', company: 'Netflix', duration_months: 28 },
      { title: 'Senior Engineer', company: 'Microsoft', duration_months: 36 }
    ],
    github_profile: { top_languages: ['Python', 'C++', 'Java', 'Scala'] },
    notes: 'Strong technical leader with proven track record of scaling teams and delivering complex projects on time.',
    linkedin_url: 'https://linkedin.com/in/priyapatel',
    x_profile: { url: 'https://x.com/priyap' }
  },
  {
    id: '4',
    name: 'Alex Rodriguez',
    current_title: 'Principal Engineer',
    current_company: 'Shopify',
    priority_tier: 'top',
    score: { total_score: 90 },
    experiences: [
      { title: 'Principal Engineer', company: 'Shopify', duration_months: 22 },
      { title: 'Staff Engineer', company: 'Square', duration_months: 32 },
    ],
    github_profile: { top_languages: ['Ruby', 'Go', 'TypeScript', 'Elixir'] },
    notes: 'E-commerce platform expert. Built high-throughput systems handling millions of transactions daily.',
    linkedin_url: 'https://linkedin.com/in/alexrodriguez',
    x_profile: { url: 'https://x.com/alexr' }
  },
  {
    id: '5',
    name: 'Emily Wang',
    current_title: 'ML Engineer',
    current_company: 'OpenAI',
    priority_tier: 'top',
    score: { total_score: 94 },
    experiences: [
      { title: 'ML Engineer', company: 'OpenAI', duration_months: 16 },
      { title: 'Research Engineer', company: 'DeepMind', duration_months: 24 },
      { title: 'Data Scientist', company: 'Facebook AI', duration_months: 20 }
    ],
    github_profile: { top_languages: ['Python', 'C++', 'CUDA', 'Julia'] },
    notes: 'Cutting-edge AI/ML researcher. Published papers on transformer architectures and large language models.',
    linkedin_url: 'https://linkedin.com/in/emilywang',
    x_profile: { url: 'https://x.com/emilyw' }
  },
  {
    id: '6',
    name: 'David Kim',
    current_title: 'Senior Backend Engineer',
    current_company: 'Coinbase',
    priority_tier: 'high',
    score: { total_score: 78 },
    experiences: [
      { title: 'Senior Backend Engineer', company: 'Coinbase', duration_months: 14 },
      { title: 'Backend Engineer', company: 'Robinhood', duration_months: 26 },
      { title: 'Full Stack Engineer', company: 'Startup', duration_months: 18 }
    ],
    github_profile: { top_languages: ['Go', 'Python', 'Solidity', 'Rust'] },
    notes: 'Blockchain and fintech specialist. Built secure, scalable APIs for cryptocurrency trading platforms.',
    linkedin_url: 'https://linkedin.com/in/davidkim',
    x_profile: { url: 'https://x.com/davidk' }
  },
  {
    id: '7',
    name: 'Jessica Martinez',
    current_title: 'Frontend Architect',
    current_company: 'Figma',
    priority_tier: 'high',
    score: { total_score: 82 },
    experiences: [
      { title: 'Frontend Architect', company: 'Figma', duration_months: 18 },
      { title: 'Senior Frontend Engineer', company: 'Adobe', duration_months: 30 },
      { title: 'UI Engineer', company: 'Dropbox', duration_months: 24 }
    ],
    github_profile: { top_languages: ['TypeScript', 'React', 'WebGL', 'CSS'] },
    notes: 'Expert in building performant, real-time collaborative applications. Deep knowledge of browser internals.',
    linkedin_url: 'https://linkedin.com/in/jessicamartinez',
    x_profile: { url: 'https://x.com/jessicam' }
  },
  {
    id: '8',
    name: 'Ryan Thompson',
    current_title: 'DevOps Engineer',
    current_company: 'GitHub',
    priority_tier: 'high',
    score: { total_score: 76 },
    experiences: [
      { title: 'DevOps Engineer', company: 'GitHub', duration_months: 22 },
      { title: 'Site Reliability Engineer', company: 'Atlassian', duration_months: 28 },
      { title: 'Systems Engineer', company: 'Red Hat', duration_months: 20 }
    ],
    github_profile: { top_languages: ['Python', 'Bash', 'Terraform', 'Go'] },
    notes: 'Infrastructure automation expert. Reduced deployment times by 80% through CI/CD optimization.',
    linkedin_url: 'https://linkedin.com/in/ryanthompson',
    x_profile: { url: 'https://x.com/ryant' }
  },
  {
    id: '9',
    name: 'Lisa Anderson',
    current_title: 'Security Engineer',
    current_company: 'Cloudflare',
    priority_tier: 'high',
    score: { total_score: 80 },
    experiences: [
      { title: 'Security Engineer', company: 'Cloudflare', duration_months: 16 },
      { title: 'Application Security', company: 'Twitter', duration_months: 24 },
      { title: 'Security Analyst', company: 'Cisco', duration_months: 22 }
    ],
    github_profile: { top_languages: ['Rust', 'C', 'Python', 'Go'] },
    notes: 'Cybersecurity specialist focused on DDoS mitigation and zero-trust architectures.',
    linkedin_url: 'https://linkedin.com/in/lisaanderson',
    x_profile: { url: 'https://x.com/lisaa' }
  },
  {
    id: '10',
    name: 'James Lee',
    current_title: 'Mobile Engineer',
    current_company: 'Instagram',
    priority_tier: 'standard',
    score: { total_score: 68 },
    experiences: [
      { title: 'Mobile Engineer', company: 'Instagram', duration_months: 20 },
      { title: 'iOS Developer', company: 'Snapchat', duration_months: 18 },
      { title: 'Android Developer', company: 'Spotify', duration_months: 16 }
    ],
    github_profile: { top_languages: ['Swift', 'Kotlin', 'Objective-C', 'Java'] },
    notes: 'Cross-platform mobile development expert. Improved app performance and reduced crash rates significantly.',
    linkedin_url: 'https://linkedin.com/in/jameslee',
    x_profile: { url: 'https://x.com/jamesl' }
  },
  {
    id: '11',
    name: 'Sofia Gonzalez',
    current_title: 'Data Engineer',
    current_company: 'Snowflake',
    priority_tier: 'high',
    score: { total_score: 72 },
    experiences: [
      { title: 'Data Engineer', company: 'Snowflake', duration_months: 14 },
      { title: 'Analytics Engineer', company: 'Databricks', duration_months: 22 },
      { title: 'Data Analyst', company: 'LinkedIn', duration_months: 18 }
    ],
    github_profile: { top_languages: ['SQL', 'Python', 'Scala', 'Java'] },
    notes: 'Big data pipeline specialist. Built real-time analytics systems processing petabytes of data.',
    linkedin_url: 'https://linkedin.com/in/sofiagonzalez',
    x_profile: { url: 'https://x.com/sofiag' }
  },
  {
    id: '12',
    name: 'Kevin Nguyen',
    current_title: 'Full Stack Engineer',
    current_company: 'Notion',
    priority_tier: 'standard',
    score: { total_score: 65 },
    experiences: [
      { title: 'Full Stack Engineer', company: 'Notion', duration_months: 12 },
      { title: 'Software Engineer', company: 'Asana', duration_months: 20 },
      { title: 'Web Developer', company: 'Startup', duration_months: 16 }
    ],
    github_profile: { top_languages: ['TypeScript', 'Node.js', 'React', 'PostgreSQL'] },
    notes: 'Product-minded engineer with strong UX sensibility. Shipped features used by millions of users.',
    linkedin_url: 'https://linkedin.com/in/kevinnguyen',
    x_profile: { url: 'https://x.com/kevinn' }
  }
];

export default function Home() {
  const [candidates, setCandidates] = useState<any[]>(MOCK_CANDIDATES);
  const [selectedCandidate, setSelectedCandidate] = useState<any>(null);
  const [isSearching, setIsSearching] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isPanelMinimized, setIsPanelMinimized] = useState(false);
  const [isHeaderVisible, setIsHeaderVisible] = useState(true);

  useEffect(() => {
    // Using mock data for now - API integration will come later
    // loadCandidates();
  }, []);

  const loadCandidates = async () => {
    try {
      const data = await api.getCandidates();
      setCandidates(data.candidates);
    } catch (error) {
      console.error('Failed to load candidates:', error);
    }
  };

  const handleDeepSearch = async () => {
    if (!searchQuery) return;

    setIsSearching(true);
    try {
      // Trigger deep search (mock or real)
      await api.discoverFromX(searchQuery, 100, 20);
      await loadCandidates();
    } catch (error) {
      console.error('Deep search failed:', error);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <main className="relative w-full h-screen overflow-hidden bg-black text-white">
      {/* 3D Scene - Full Screen */}
      <div className="absolute inset-0 z-0">
        <Scene candidates={candidates} onCandidateSelect={setSelectedCandidate} />
      </div>

      {/* UI Overlay Layer */}
      <div className="absolute inset-0 z-10 pointer-events-none">
        {/* Header Toggle Button */}
        {!isHeaderVisible && (
          <button
            onClick={() => setIsHeaderVisible(true)}
            className="absolute top-4 left-4 bg-black/50 hover:bg-black/70 text-white/60 hover:text-white px-3 py-2 rounded-lg text-sm backdrop-blur-md pointer-events-auto transition-all border border-white/10"
          >
            ☰ Search
          </button>
        )}

        {/* Header / Search Bar */}
        {isHeaderVisible && (
          <div className="absolute top-4 left-4 pointer-events-auto transition-all duration-300">
            <div className="flex items-center gap-3 p-3 bg-black/60 backdrop-blur-xl border border-white/20 rounded-lg shadow-2xl">
              <h1 className="text-lg font-bold tracking-tighter">
                GROK <span className="text-blue-500">TALENT</span>
              </h1>

              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search for talent..."
                  className="bg-white/10 border border-white/20 rounded-full px-4 py-2 w-56 text-sm text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 backdrop-blur-md transition-all"
                  onKeyDown={(e) => e.key === 'Enter' && handleDeepSearch()}
                />
                <button
                  onClick={handleDeepSearch}
                  disabled={isSearching}
                  className="absolute right-2 top-1/2 -translate-y-1/2 bg-blue-600 hover:bg-blue-500 text-white px-3 py-1 rounded-full text-xs font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSearching ? '...' : 'Go'}
                </button>
              </div>

              <button
                onClick={() => setIsHeaderVisible(false)}
                className="text-white/60 hover:text-white text-lg px-2"
                title="Hide search"
              >
                ✕
              </button>
            </div>
          </div>
        )}

        {/* Selected Candidate Detail Panel */}
        {selectedCandidate && (
          <div className={`absolute right-0 top-0 bottom-0 bg-black/90 backdrop-blur-xl border-l border-white/20 overflow-hidden pointer-events-auto transition-all duration-300 ease-in-out shadow-2xl ${isPanelMinimized ? 'w-16' : 'w-96'
            }`}>
            {isPanelMinimized ? (
              // Minimized view - vertical tab
              <div className="h-full flex flex-col items-center justify-center gap-4 py-8">
                <button
                  onClick={() => setIsPanelMinimized(false)}
                  className="text-white/60 hover:text-white transition-colors rotate-180 text-xl"
                  title="Expand panel"
                >
                  ◀
                </button>
                <div className="transform -rotate-90 whitespace-nowrap text-sm text-white/40 font-medium">
                  {selectedCandidate.name}
                </div>
                <button
                  onClick={() => setSelectedCandidate(null)}
                  className="text-white/40 hover:text-white transition-colors text-lg"
                  title="Close"
                >
                  ✕
                </button>
              </div>
            ) : (
              // Full view - SCROLLABLE
              <div className="h-full flex flex-col">
                {/* Fixed Header */}
                <div className="flex-shrink-0 flex items-center justify-between p-4 border-b border-white/10">
                  <h2 className="text-lg font-bold">Candidate Details</h2>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setIsPanelMinimized(true)}
                      className="text-gray-400 hover:text-white text-lg transition-colors"
                      title="Minimize panel"
                    >
                      ▶
                    </button>
                    <button
                      onClick={() => setSelectedCandidate(null)}
                      className="text-gray-400 hover:text-white text-xl transition-colors"
                      title="Close"
                    >
                      ✕
                    </button>
                  </div>
                </div>

                {/* Scrollable Content */}
                <div className="flex-1 overflow-y-auto p-6" style={{
                  scrollbarWidth: 'thin',
                  scrollbarColor: 'rgba(255, 255, 255, 0.3) transparent'
                }}>
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold bg-gradient-to-br from-blue-500 to-purple-600 border-2 border-white/30 shadow-lg">
                      {selectedCandidate.score?.total_score ? Math.round(selectedCandidate.score.total_score) : '?'}
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold">{selectedCandidate.name}</h3>
                      <p className="text-sm text-gray-300">{selectedCandidate.current_title}</p>
                      <p className="text-sm text-blue-400">{selectedCandidate.current_company}</p>
                    </div>
                  </div>

                  <div className="space-y-6">
                    <section>
                      <h4 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-3">Experience</h4>
                      <div className="space-y-3">
                        {selectedCandidate.experiences?.slice(0, 3).map((exp: any, i: number) => (
                          <div key={i} className="border-l-2 border-blue-500/50 pl-3 py-1">
                            <div className="text-sm font-semibold">{exp.title}</div>
                            <div className="text-xs text-gray-400">{exp.company}</div>
                          </div>
                        ))}
                      </div>
                    </section>

                    <section>
                      <h4 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-3">Skills</h4>
                      <div className="flex flex-wrap gap-2">
                        {selectedCandidate.github_profile?.top_languages?.map((lang: string) => (
                          <span key={lang} className="px-3 py-1 bg-white/10 rounded-full text-xs border border-white/20 hover:bg-white/20 transition-colors">
                            {lang}
                          </span>
                        ))}
                      </div>
                    </section>

                    <section>
                      <h4 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-3">Analysis</h4>
                      <p className="text-sm text-gray-300 leading-relaxed">
                        {selectedCandidate.notes || "No additional analysis available."}
                      </p>
                    </section>

                    <section>
                      <h4 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-3">Links</h4>
                      <div className="flex gap-3">
                        {selectedCandidate.linkedin_url && (
                          <a href={selectedCandidate.linkedin_url} target="_blank" rel="noreferrer"
                            className="flex-1 bg-[#0077b5] hover:bg-[#006396] py-2 rounded-lg text-center text-sm font-medium transition-colors">
                            LinkedIn
                          </a>
                        )}
                        {selectedCandidate.x_profile?.url && (
                          <a href={selectedCandidate.x_profile.url} target="_blank" rel="noreferrer"
                            className="flex-1 bg-white/10 hover:bg-white/20 py-2 rounded-lg text-center text-sm font-medium transition-colors border border-white/20">
                            X / Twitter
                          </a>
                        )}
                      </div>
                    </section>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Footer Info */}
        <div className="absolute bottom-4 left-4 pointer-events-auto">
          <div className="text-xs font-medium text-cyan-300 bg-blue-900/50 backdrop-blur-md px-3 py-2 rounded-lg border border-cyan-500/30">
            Brighter & closer fish = higher score • Golden crown = top tier (90+)
          </div>
        </div>
      </div>
    </main>
  );
}
