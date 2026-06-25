import { useEffect, useState } from 'react'
import { startAnalysis, pollJob } from '../api/client'
import type { JobResult } from '../api/client'

type Props = {
  sessionId: string
  onComplete: (result: JobResult['result']) => void
  onError: (msg: string) => void
}

const STATUS_LABELS: Record<string, string> = {
  pending: 'Starting...',
  fetching: 'Fetching transactions from your bank...',
  detecting: 'Detecting rent payment patterns...',
}

export default function Analyzing({ sessionId, onComplete, onError }: Props) {
  const [statusLabel, setStatusLabel] = useState('Starting...')

  useEffect(() => {
    let timer: ReturnType<typeof setTimeout>

    async function kickoff() {
      const jobId = await startAnalysis(sessionId)
      poll(jobId)
    }

    function poll(jobId: string) {
      timer = setTimeout(async () => {
        const job = await pollJob(jobId)
        setStatusLabel(STATUS_LABELS[job.status] ?? 'Working...')
        if (job.status === 'complete') {
          onComplete(job.result)
        } else if (job.status === 'error') {
          onError(job.error ?? 'Analysis failed.')
        } else {
          poll(jobId)
        }
      }, 2000)
    }

    kickoff().catch(() => onError('Failed to start analysis.'))
    return () => clearTimeout(timer)
  }, [sessionId, onComplete, onError])

  return (
    <div>
      <p>{statusLabel}</p>
    </div>
  )
}
