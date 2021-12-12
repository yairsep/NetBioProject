import React from 'react';
import { Tab } from 'semantic-ui-react'
import TabsTable from './tabsTable';
import ShapImage from './shapImage';
import GOTab from './GOTab';
import Chart from './distributionChart';

const Tabs = (props) => {
  const { summaryData, gene, data, shapData } = props

  let panes;
  panes = [  
    {
      menuItem: 'Shap Graph',
      key: 'shap',
      render: () => <ShapImage shapData={shapData}/>

    },
    
    {
      menuItem: 'Distributions',
      key: 'distribution',
      render: () => <Chart data={data} />

    },

    {
      menuItem: 'Summary',
      key: 'summary',
      render: () => <TabsTable content={summaryData} data={data} />

    },

    {
      menuItem: 'Gene Ontology',
      key: 'go',
      render: () => <GOTab gene={gene} />

    }
  ]
  // } else {
  //   panes = [      
  //     {
  //       menuItem: 'Distributions',
  //       key: 'distribution',
  //       render: () => <Chart data={data} />
  
  //     },
  
  //     {
  //       menuItem: 'Summary',
  //       key: 'summary',
  //       render: () => <TabsTable content={summaryData} data={data} />
  
  //     },
  
  //     {
  //       menuItem: 'Gene Ontology',
  //       key: 'go',
  //       render: () => <GOTab gene={gene} />
  
  //     }
  //   ]
  // }

  return (
    <Tab panes={panes} />
  )
}

export default Tabs;
