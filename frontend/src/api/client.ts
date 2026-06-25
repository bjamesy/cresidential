import axios from 'axios'

const api = axios.create()

export async function createLinkToken(): Promise<string> {
  const res = await api.post('/plaid/create-link-token')
  return res.data.link_token
}

export async function exchangeToken(publicToken: string): Promise<string> {
  const res = await api.post('/plaid/exchange-token', { public_token: publicToken })
  return res.data.session_id
}

export async function startAnalysis(sessionId: string): Promise<string> {
  const res = await api.post('/transactions/analyze', { session_id: sessionId })
  return res.data.job_id
}

export async function pollJob(jobId: string): Promise<JobResult> {
  const res = await api.get(`/jobs/${jobId}`)
  return res.data
}

export type RentCandidate = {
  description: string
  amount_range: [number, number]
  typical_amount: number
  first_payment: string
  last_payment: string
  occurrences: number
  cadence: string
  confidence_score: number
  transactions: { date: string; amount: number; description: string }[]
}

export type JobResult = {
  job_id: string
  status: 'pending' | 'fetching' | 'detecting' | 'complete' | 'error'
  result?: {
    period: { start: string; end: string }
    total_transactions_analyzed: number
    candidates: RentCandidate[]
  }
  error?: string
}
