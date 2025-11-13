import React, { useState } from 'react'

export type RiskLevel = 'conservative' | 'balanced' | 'aggressive'

export interface AllocationRequest {
  amount: number
  risk: RiskLevel
}

interface Props {
  onAllocate: (req: AllocationRequest) => void
}

const AllocationForm: React.FC<Props> = ({ onAllocate }) => {
  const [amount, setAmount] = useState<number>(1000)
  const [risk, setRisk] = useState<RiskLevel>('balanced')

  const submit = (e: React.FormEvent) => {
    e.preventDefault()
    onAllocate({ amount, risk })
  }

  return (
    <form className="allocation-form" onSubmit={submit}>
      <h2>Allocation Calculator</h2>
      <label>
        Amount to invest (USD)
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(Number(e.target.value))}
          min={0}
        />
      </label>

      <label>
        Risk profile
        <select value={risk} onChange={(e) => setRisk(e.target.value as RiskLevel)}>
          <option value="conservative">Conservative</option>
          <option value="balanced">Balanced</option>
          <option value="aggressive">Aggressive</option>
        </select>
      </label>

      <button type="submit">Generate allocation</button>
    </form>
  )
}

export default AllocationForm
