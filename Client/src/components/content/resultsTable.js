/* eslint-disable camelcase */
/* eslint-disable radix */
/* eslint-disable no-use-before-define */
import React, { useState, useEffect } from 'react'
import { Table, Icon, Pagination, Dropdown } from 'semantic-ui-react'
import tissues from '../common/tissues'
import resultsHeaders from '../../config/resultsHeaders'
import sample from '../results/sample'

const ResultsTable = (props) => {
  // eslint-disable-next-line react/destructuring-assignment
  const numOfPages = Math.ceil(props.tableData.length / 16);

  //const scoreList = props.tableData.map((item) => item['Pathological_probability']).sort((a, b) => a - b);
  //const numOfOccs = (value) => scoreList.reduce((occs, el) => occs + (el === value), 0);

  //Returns the order rank of the score. if there are duplicates of the score, it returns the average rank of the score
  //const getRank = (score) => ((scoreList.indexOf(score) + 1 + scoreList.indexOf(score) + numOfOccs(score)) * numOfOccs(score) / 2) / numOfOccs(score)

  const toggleArrow = (attr) => {
    if (sortStatus.column === attr) {
      if (sortStatus.direction === 'ascending') return ' ▲';
      return ' ▼';
    }
    return '';
  }

  const [sortStatus, setSortStatus] = useState({ column: '', direction: '', data: [] })

  const [currPage, setPage] = useState(1)

  const sortData = (data, prop) => data.sort((a, b) => ((a[prop] < b[prop]) ? -1 : (a[prop] > b[prop]) ? 1 : 0))

  const handleSort = (e) => {
    const clickedColumn = e.target.id;
    (sortStatus.column !== clickedColumn)
      ? setSortStatus({ data: sortData(sortStatus.data, clickedColumn), column: clickedColumn, direction: 'ascending' })
      : (sortStatus.direction === 'ascending'
        ? setSortStatus({ ...sortStatus, data: sortStatus.data.reverse(), direction: 'descending' })
        : setSortStatus({ ...sortStatus, data: sortStatus.data.reverse(), direction: 'ascending' }))
  }

  const getSliceRng = () => ((parseInt(currPage)) - 1) * 16

  useEffect(() => {
    if (props.tableData.length === 0) {
      const percentiledData = props.tableData.map((item) => ({ ...item }))//, Pathological_probability: Number((getRank(item['Pathological_probability']) / scoreList.length * 100).toFixed(2))
      setSortStatus({ column: 'Pathological_probability', direction: 'descending', data: sortData(percentiledData, 'Pathological_probability').reverse() })
    } else {
      const percentiledData = sample.map((item) => ({ ...item }))//, Pathological_probability: Number((getRank(item['Pathological_probability']) / scoreList.length * 100).toFixed(2))
      setSortStatus({ column: 'Pathological_probability', direction: 'descending', data: sortData(percentiledData, 'Pathological_probability').reverse() })
    }
  }, [])

  return (
    <div>
      <Table sortable celled selectable textAlign="center" display="inline-block" overflow="scroll">
        <Table.Header>
          <Table.Row>
            {resultsHeaders.map(({ attr, value }) => (
              <Table.HeaderCell
                key={attr}
                sorted={sortStatus.column === { attr } ? sortStatus.direction : null}
                onClick={handleSort}
                id={attr}
              >
                {value + toggleArrow(attr)}
              </Table.HeaderCell>
            ))}
          </Table.Row>
        </Table.Header>

        <Table.Body>
          {sortStatus.data.slice(getSliceRng(), (getSliceRng() + 16))
            .map(({ GeneName, GeneID_y, Chr, Pos, Ref, Alt, Type, Length, SITFval, PolyPhenVal, PHRED, Pathological_probability }) => (
              <Table.Row positive={GeneName === props.selectedRow} onClick={props.onRowSelect} key={`${GeneName}_${Math.random()}`}>
                <Table.Cell id={GeneName}>{GeneName}</Table.Cell>
                <Table.Cell id={GeneName}>{GeneID_y}</Table.Cell>
                <Table.Cell id={GeneName}>{Chr}</Table.Cell>
                <Table.Cell id={GeneName}>{Pos}</Table.Cell>
                <Table.Cell id={GeneName}>{Ref}</Table.Cell>
                <Table.Cell id={GeneName}>{Alt}</Table.Cell>
                <Table.Cell id={GeneName}>{Type}</Table.Cell>
                <Table.Cell id={GeneName}>{Length}</Table.Cell>
                <Table.Cell id={GeneName}>{ SITFval || 'none' }</Table.Cell>
                <Table.Cell id={GeneName}>{ PolyPhenVal || 'none'}</Table.Cell>
                <Table.Cell id={GeneName}>{PHRED}</Table.Cell>
                <Table.Cell id={GeneName}>{Pathological_probability}</Table.Cell>
              </Table.Row>
            ))}
        </Table.Body>  
      </Table>
      <Pagination
        activePage={currPage}
        ellipsisItem={{ content: <Icon name="ellipsis horizontal" />, icon: true, type: 'ellipsisItem' }}
        firstItem={{ content: <Icon name="angle double left" />, icon: true, type: 'firstItem' }}
        lastItem={{ content: <Icon name="angle double right" />, icon: true, type: 'lastItem' }}
        prevItem={{ content: <Icon name="angle left" />, icon: true, type: 'prevItem' }}
        nextItem={{ content: <Icon name="angle right" />, icon: true, type: 'nextItem' }}
        totalPages={numOfPages}
        onPageChange={(_e, data) => setPage(data.activePage)}
      />
    </div>
  ); 
}

export default ResultsTable;

// currPage < numOfPages ? setPage(e.target.innerText) : ''
