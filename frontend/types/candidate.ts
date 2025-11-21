export interface SocialProfile {
  platform: string;
  username: string;
  url: string;
  followers: number;
  engagement_score: number;
}

export interface Experience {
  company: string;
  title: string;
  start_date?: string;
  end_date?: string;
  duration_months: number;
  description?: string;
  is_faang: boolean;
  is_frontier_lab: boolean;
  is_top_tech: boolean;
}

export interface Education {
  institution: string;
  degree?: string;
  field?: string;
  start_year?: number;
  end_year?: number;
  is_top_university: boolean;
}

export interface GitHubStats {
  username: string;
  url: string;
  followers: number;
  public_repos: number;
  total_stars: number;
  contributions_last_year: number;
  top_languages: string[];
  notable_projects: Array<{
    name: string;
    stars: number;
    description: string;
    url: string;
  }>;
}

export interface CandidateScore {
  total_score: number;
  faang_score: number;
  frontier_labs_score: number;
  top_tech_score: number;
  github_score: number;
  x_engagement_score: number;
  research_score: number;
  education_score: number;
  experience_score: number;
  open_source_score: number;
  leadership_score: number;
}

export interface Candidate {
  id: string;
  name: string;
  email?: string;
  x_profile?: SocialProfile;
  github_profile?: GitHubStats;
  linkedin_url?: string;
  current_title?: string;
  current_company?: string;
  experiences: Experience[];
  total_years_experience: number;
  education: Education[];
  publications: any[];
  score: CandidateScore;
  priority_tier: 'low' | 'medium' | 'high' | 'top';
  discovered_from?: string;
  discovery_date: string;
  last_updated: string;
  notes?: string;
}
