import { useEffect, useState, useCallback } from 'react'
import { usePlaidLink } from 'react-plaid-link'
import { createLinkToken, exchangeToken } from '../api/client'

type Props = {
  onConnected: (sessionId: string) => void
}

export default function ConnectBank({ onConnected }: Props) {
  const [linkToken, setLinkToken] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    createLinkToken()
      .then(setLinkToken)
      .catch(() => setError('Failed to initialize bank connection.'))
  }, [])

  const onSuccess = useCallback(async (publicToken: string) => {
    try {
      const sessionId = await exchangeToken(publicToken)
      onConnected(sessionId)
    } catch {
      setError('Failed to connect bank account.')
    }
  }, [onConnected])

  const { open, ready } = usePlaidLink({ token: linkToken ?? '', onSuccess })

  if (error) return <p style={{ color: 'red' }}>{error}</p>

  return (
    <div>
      <h1>Rental Verification</h1>
      <p>Connect your bank account to detect rent payments from the last 24 months.</p>
      <button onClick={() => open()} disabled={!ready}>
        Connect Bank Account
      </button>
    </div>
  )
}
