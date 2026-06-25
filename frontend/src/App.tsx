import { useState, useCallback } from 'react'
import ConnectBank from './components/ConnectBank'
import Analyzing from './components/Analyzing'
import CandidateList from './components/CandidateList'
import { JobResult } from './api/client'

type State =
  | { step: 'idle' }
  | { step: 'analyzing'; sessionId: string }
  | { step: 'results'; result: NonNullable<JobResult['result']> }
  | { step: 'error'; message: string }

export default function App() {
  const [state, setState] = useState<State>({ step: 'idle' })

  const onConnected = useCallback((sessionId: string) => {
    setState({ step: 'analyzing', sessionId })
  }, [])

  const onComplete = useCallback((result: JobResult['result']) => {
    if (result) setState({ step: 'results', result })
  }, [])

  const onError = useCallback((message: string) => {
    setState({ step: 'error', message })
  }, [])

  if (state.step === 'idle') {
    return <ConnectBank onConnected={onConnected} />
  }

  if (state.step === 'analyzing') {
    return <Analyzing sessionId={state.sessionId} onComplete={onComplete} onError={onError} />
  }

  if (state.step === 'results') {
    return (
      <CandidateList
        period={state.result.period}
        total={state.result.total_transactions_analyzed}
        candidates={state.result.candidates}
      />
    )
  }

  return <p style={{ color: 'red' }}>Error: {state.message}</p>
}
