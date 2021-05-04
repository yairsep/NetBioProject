import React from 'react'
import { Icon, Label, Menu, Table } from 'semantic-ui-react'
import { CSVDownload, CSVLink } from 'react-csv';
import tissues from './tissues';

const TabsTable = (props) => {
  const { content, data } = props
  const headers = ['Property', 'Value']
  const scores = data.map((i) => Number(i['Meta_MLP']))
  const mean = (scores.reduce((acc, cur) => acc + cur)) / data.length

  const summary = {
    'Tissue': tissues.find((tissue) => tissue['value'] === content['tissue'])['text'],
    'Total query genes': 3, //JSON.parse(localStorage.getItem('genes')).length,
    'Total unique genes': data.length,
    'Total unrecognized genes': content['gene_not_in_db'],
    'Max score': Math.max(...scores).toFixed(2),
    'Average score': mean.toFixed(2)
  }
  const csvData = [['geneName', 'score', 'OMIM', 'ensembl'], ...data.map((item) => [item['Symbol'], item['Meta_MLP'], item['MIM_morbid_accession'], item['id']])]

  return (
    <Table celled columns="two" fixed striped compact>

      <Table.Header>
        <Table.Row>
          { headers.map((header) => <Table.HeaderCell key={header}>{header}</Table.HeaderCell>)}
        </Table.Row>
      </Table.Header>

      <Table.Body>
        <Table.Row>
          <Table.Cell>CSV Download Link</Table.Cell>
          <Table.Cell><CSVLink data={csvData} target="_blank">Download</CSVLink></Table.Cell>
        </Table.Row>
        {Object.keys(summary).map((key) => (
          <Table.Row key={key}>
            <Table.Cell>{key}</Table.Cell>
            <Table.Cell>{summary[key]}</Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>

    </Table>
  )
}

export default TabsTable;
