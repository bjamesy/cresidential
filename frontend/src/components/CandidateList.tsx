import { RentCandidate } from '../api/client'

type Props = {
  period: { start: string; end: string }
  total: number
  candidates: RentCandidate[]
}

export default function CandidateList({ period, total, candidates }: Props) {
  return (
    <div>
      <h2>Detected Rent Payment Candidates</h2>
      <p>
        Analyzed {total} transactions from {period.start} to {period.end}.
      </p>

      {candidates.length === 0 ? (
        <p>No recurring rent-like payments detected.</p>
      ) : (
        candidates.map((c, i) => (
          <div key={i} style={{ border: '1px solid #ccc', padding: '1rem', marginBottom: '1rem' }}>
            <h3>{c.description || '(unknown payee)'}</h3>
            <table>
              <tbody>
                <tr><td>Typical amount</td><td>${c.typical_amount.toFixed(2)}</td></tr>
                <tr><td>Amount range</td><td>${c.amount_range[0].toFixed(2)} – ${c.amount_range[1].toFixed(2)}</td></tr>
                <tr><td>Occurrences</td><td>{c.occurrences}</td></tr>
                <tr><td>Period</td><td>{c.first_payment} → {c.last_payment}</td></tr>
                <tr><td>Cadence</td><td>{c.cadence}</td></tr>
                <tr><td>Confidence</td><td>{(c.confidence_score * 100).toFixed(0)}%</td></tr>
              </tbody>
            </table>
          </div>
        ))
      )}
    </div>
  )
}
