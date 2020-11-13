import React, { useState, useEffect } from 'react';
import { List, Label, Tab } from 'semantic-ui-react'
import TabsTable from './tabsTable';
import GOTab from './GOTab';
import Chart from './distributionChart';

const Tabs = (props) => {
  const { summaryData, gene, data } = props

  const panes = [
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

  return (
    <Tab panes={panes} />
  )
}

export default Tabs;
