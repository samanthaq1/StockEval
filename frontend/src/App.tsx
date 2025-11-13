import React, { useState } from 'react'
import AllocationForm, { AllocationRequest } from './components/AllocationForm'
import StockChart from './components/StockChart'

type AllocationItem = {
  ticker: string
  percent: number
  amount: number
}

type AllocationResponse = {
  requested: AllocationRequest
  allocations: AllocationItem[]
  created_at: string
}

const App: React.FC = () => {
  const [lastRequest, setLastRequest] = useState<AllocationRequest | null>(null)
  const [lastResponse, setLastResponse] = useState<AllocationResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAllocate = async (req: AllocationRequest) => {
    setLastRequest(req)
    setLoading(true)
    setError(null)
    try {
      // Use environment variable for backend URL, default to localhost for dev
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'
      const res = await fetch(`${backendUrl}/api/allocate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req),
      })
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
      const data = (await res.json()) as AllocationResponse
      setLastResponse(data)
    } catch (e: any) {
      setError(e.message || String(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>StockEval — Frontend Prototype</h1>
      </header>
      <main>
        <section className="left">
          <AllocationForm onAllocate={handleAllocate} />
        </section>
        <section className="right">
          <StockChart />
          {loading && <div>Loading allocation...</div>}
          {error && <div style={{ color: 'red' }}>Error: {error}</div>}
          {lastResponse && (
            <div className="summary">
              <h3>Allocation result</h3>
              <pre>{JSON.stringify(lastResponse, null, 2)}</pre>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
