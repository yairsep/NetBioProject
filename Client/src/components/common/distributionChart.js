/* eslint-disable react/destructuring-assignment */
import React, { useState, useEffect } from 'react';
import { Chart } from 'react-google-charts';

const DistributionChart = (props) => {
  useEffect(() => {

  })

  const distribution = props.data.reduce((acc, curr) => {
    const idx = acc.findIndex((item) => item[0] === curr['Pathological_probability'])
    idx === -1 ? acc = acc.concat([[curr['Pathological_probability'], 1]]) : acc[idx][1] += 1;
    return acc;
  }, [])
  // Builds an 2d-array with [score, numOfGenes]. like : [ [2, 21], [6, 15], ...  ]

  const bubblesData = [['geneName', 'Pathological_probability'], ...props.data.map((item) => [item['GeneName'], parseFloat(item['Pathological_probability'])])]
  console.log(bubblesData)
  return (
    <div>
      <Chart
        chartType="Histogram"
        loader={<div>Loading Charts</div>}
        height={200}
        data={bubblesData}
        options={{
          title: 'Score Distribution',
          bar: { gap: 0 },
          hAxis: { title: 'Score',
            viewWindow: {
              min: 0,
              max: 1  
            },
            ticks: [0.1, 0.2, 0.4, 0.6, 0.8, 1] },
          vAxis: { title: '#Genes' },
          // series: {0: { curveType: 'function' },},
          legend: 'none',
          // animation: {
          //     startup: true,
          //     easing: 'out',
          //     duration: 1500,
          // },
          // is3D: true
        }}
      />

      <Chart
        chartType="ScatterChart"
        height={430}
        data={bubblesData}
        options={{
          title: 'Scattering Chart',
          hAxis: { title: 'Genes', textPosition: 'none' },
          vAxis: { title: 'Score', minValue: 0, maxValue: 1 },
          legend: 'none',
          animation: {
            startup: true,
            easing: 'linear',
            duration: 1500,
          },
          pointSize: 2
        }}
      />
    </div>
  )
}

export default DistributionChart;
