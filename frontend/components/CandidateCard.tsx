import { Candidate } from '@/types/candidate';
import Link from 'next/link';

interface CandidateCardProps {
  candidate: Candidate;
}

const getTierColor = (tier: string) => {
  switch (tier) {
    case 'top':
      return 'bg-purple-500/20 text-purple-300 border-purple-500/30';
    case 'high':
      return 'bg-blue-500/20 text-blue-300 border-blue-500/30';
    case 'medium':
      return 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30';
    default:
      return 'bg-white/10 text-gray-300 border-white/20';
  }
};

const getTierBadge = (tier: string) => {
  const emojis: Record<string, string> = { top: '🏆', high: '🔥', medium: '⚡', low: '📌' };
  return emojis[tier] || '📌';
};

export default function CandidateCard({ candidate }: CandidateCardProps) {
  const tierColor = getTierColor(candidate.priority_tier);
  const tierBadge = getTierBadge(candidate.priority_tier);

  return (
    <Link href={`/candidate/${candidate.id}`}>
      <div className="border border-white/10 rounded-lg p-6 hover:border-white/20 hover:bg-white/5 transition-all duration-200 bg-black cursor-pointer group">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-xl font-semibold text-white group-hover:text-white/90">{candidate.name}</h3>
            {candidate.current_title && (
              <p className="text-sm text-gray-400 mt-1">{candidate.current_title}</p>
            )}
            {candidate.current_company && (
              <p className="text-sm font-medium text-gray-300 mt-1">{candidate.current_company}</p>
            )}
          </div>
          <div className={`px-3 py-1 rounded-full text-xs font-medium border ${tierColor}`}>
            {tierBadge} {candidate.priority_tier.toUpperCase()}
          </div>
        </div>

        <div className="mb-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-sm font-medium text-gray-400">Score:</span>
            <div className="flex-1 bg-white/10 rounded-full h-2">
              <div
                className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all"
                style={{ width: `${candidate.score.total_score}%` }}
              />
            </div>
            <span className="text-sm font-semibold text-white">
              {candidate.score.total_score.toFixed(1)}
            </span>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {candidate.github_profile && (
            <span className="px-2 py-1 bg-white text-black text-xs rounded-md font-medium">
              GitHub: {candidate.github_profile.total_stars}⭐
            </span>
          )}
          {candidate.x_profile && (
            <span className="px-2 py-1 bg-white text-black text-xs rounded-md font-medium">
              X: {candidate.x_profile.followers} followers
            </span>
          )}
          {candidate.total_years_experience > 0 && (
            <span className="px-2 py-1 bg-blue-500/20 text-blue-300 text-xs rounded-md border border-blue-500/30">
              {candidate.total_years_experience}+ years
            </span>
          )}
        </div>

        <div className="flex flex-wrap gap-1">
          {candidate.experiences.slice(0, 3).map((exp, idx) => (
            <span
              key={idx}
              className={`px-2 py-1 text-xs rounded-md ${
                exp.is_frontier_lab
                  ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                  : exp.is_faang
                  ? 'bg-green-500/20 text-green-300 border border-green-500/30'
                  : exp.is_top_tech
                  ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                  : 'bg-white/5 text-gray-400 border border-white/10'
              }`}
            >
              {exp.company}
            </span>
          ))}
        </div>
      </div>
    </Link>
  );
}
