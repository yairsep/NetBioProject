import React from 'react';
import { Icon, Label, Menu, Table } from 'semantic-ui-react';
import { CSVDownload, CSVLink } from 'react-csv';
import { useLocation } from 'react-router-dom';
import tissues from './tissues';

const TabsTable = (props) => {
  const { content, data } = props;
  const headers = ['Property', 'Value'];
  const scores = data.map((i) => Number(i['Pathological_probability']));
  const mean = scores.reduce((acc, cur) => acc + cur) / data.length;

  const location = useLocation();
  const { pathname } = location;
  const totalQueryGenes = pathname.includes('results')
    ? JSON.parse(localStorage.getItem('pathoSearchData')).genes.length
    : NaN;
  const summary = {
    Tissue: tissues.find((tissue) => tissue['value'] === content['tissue'])[
      'text'
    ],
    'Total query genes': totalQueryGenes, //JSON.parse(localStorage.getItem('genes')).length,
    'Total unique genes': data.length,
    'Total unrecognized genes': content['gene_not_in_db'],
    'Max score': Math.max(...scores).toFixed(2),
    'Average score': mean.toFixed(2),
  };
  const csvData = [
    [
      'GeneName',
      'GeneID',
      '#Chr',
      'Pos',
      'Ref',
      'Alt',
      'Type',
      'Length',
      'PHRED',
      'PolyPhenVal',
      'SIFTval',
      'Pathological_probability',
    ],
    ...data.map((item) => [
      item['GeneName'],
      item['GeneID_y'],
      item['#Chr'],
      item['Pos'],
      item['Ref'],
      item['Alt'],
      item['Type'],
      item['Length'],
      item['PHRED'],
      item['PolyPhenVal'],
      item['SIFTval'],
      item['Pathological_probability'],
    ]),
  ];

  return (
    <Table celled columns="two" fixed striped compact>
      <Table.Header>
        <Table.Row>
          {headers.map((header) => (
            <Table.HeaderCell key={header}>{header}</Table.HeaderCell>
          ))}
        </Table.Row>
      </Table.Header>

      <Table.Body>
        <Table.Row>
          <Table.Cell>CSV Download Link</Table.Cell>
          <Table.Cell>
            <CSVLink data={csvData} target="_blank">
              Download
            </CSVLink>
          </Table.Cell>
        </Table.Row>
        {Object.keys(summary).map((key) => {
          if (!Number.isNaN(summary[key])) {
            return (
              <Table.Row key={key}>
                <Table.Cell>{key}</Table.Cell>
                <Table.Cell>{summary[key]}</Table.Cell>
              </Table.Row>
            )
          } 
          return null;
        })}
      </Table.Body>
    </Table>
  );
};

export default TabsTable;
