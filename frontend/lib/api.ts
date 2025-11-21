import { Candidate } from '@/types/candidate';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';

export const api = {
  // Candidates
  async getCandidates(params?: {
    tier?: string;
    min_score?: number;
    company?: string;
    limit?: number;
    offset?: number;
  }): Promise<{ success: boolean; candidates: Candidate[]; count: number }> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString());
        }
      });
    }

    const response = await fetch(`${API_BASE}/api/candidates?${queryParams}`);
    return response.json();
  },

  async getCandidate(id: string): Promise<{ success: boolean; candidate: Candidate }> {
    const response = await fetch(`${API_BASE}/api/candidates/${id}`);
    return response.json();
  },

  async createCandidate(data: Partial<Candidate>): Promise<{ success: boolean; candidate_id: string }> {
    const response = await fetch(`${API_BASE}/api/candidates`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },

  async updateCandidate(id: string, data: Partial<Candidate>): Promise<{ success: boolean }> {
    const response = await fetch(`${API_BASE}/api/candidates/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },

  async deleteCandidate(id: string): Promise<{ success: boolean }> {
    const response = await fetch(`${API_BASE}/api/candidates/${id}`, {
      method: 'DELETE',
    });
    return response.json();
  },

  async getTopCandidates(limit: number = 20): Promise<{ success: boolean; candidates: Candidate[] }> {
    const response = await fetch(`${API_BASE}/api/candidates/top?limit=${limit}`);
    return response.json();
  },

  async discoverFromX(query: string, min_likes: number = 100, min_retweets: number = 20) {
    const response = await fetch(`${API_BASE}/api/candidates/discover/x`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, min_likes, min_retweets }),
    });
    return response.json();
  },

  async discoverFromGitHub(query: string, min_followers: number = 100) {
    const response = await fetch(`${API_BASE}/api/candidates/discover/github`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, min_followers }),
    });
    return response.json();
  },

  // Search
  async searchCandidates(params: {
    q?: string;
    tier?: string;
    min_score?: number;
    company?: string;
    limit?: number;
    offset?: number;
  }) {
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        queryParams.append(key, value.toString());
      }
    });

    const response = await fetch(`${API_BASE}/api/search/candidates?${queryParams}`);
    return response.json();
  },

  async getStats() {
    const response = await fetch(`${API_BASE}/api/search/stats`);
    return response.json();
  },

  async getCandidatesByTier() {
    const response = await fetch(`${API_BASE}/api/search/by-tier`);
    return response.json();
  },
};
