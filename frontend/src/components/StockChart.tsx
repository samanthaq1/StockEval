import React from 'react'
import Plot from 'react-plotly.js'

const StockChart: React.FC = () => {
  // Sample data: simple y = x line
  const x = Array.from({ length: 201 }, (_, i) => i - 100)
  const y = x

  return (
    <div>
      <h2>Sample Stock Chart</h2>
      <Plot
        data={[
          {
            x,
            y,
            type: 'scatter',
            mode: 'lines+markers',
            marker: { color: 'blue' },
            name: 'y = x'
          }
        ]}
        layout={{ width: 700, height: 400, title: 'Price (sample data)' }}
      />
    </div>
  )
}

export default StockChart
