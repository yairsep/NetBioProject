import React, { useState, useEffect } from 'react'
import { Table, Icon, Pagination, Dropdown } from 'semantic-ui-react'
import tissues from '../common/tissues'
import resultsHeaders from '../../config/resultsHeaders'

const ResultsTable = (props) => {
  const numOfPages = Math.ceil(props.tableData.length / 16);

  const scoreList = props.tableData.map((item) => item['Meta_MLP']).sort((a, b) => a - b);
  const numOfOccs = (value) => scoreList.reduce((occs, el) => occs + (el === value), 0);

  //Returns the order rank of the score. if there are duplicates of the score, it returns the average rank of the score
  const getRank = (score) => ((scoreList.indexOf(score) + 1 + scoreList.indexOf(score) + numOfOccs(score)) * numOfOccs(score) / 2) / numOfOccs(score)

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
    const percentiledData = props.tableData.map((item) => ({ ...item, percentile: Number((getRank(item['Meta_MLP']) / scoreList.length * 100).toFixed(2)), score: Number(item['Meta_MLP']) }))
    setSortStatus({ column: 'score', direction: 'descending', data: sortData(percentiledData, 'score').reverse() })
  }, [])

  return (

    <Table sortable celled fixed selectable textAlign="center">
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
            </Table.HeaderCell
            >
          ))}
        </Table.Row>
      </Table.Header>

      <Table.Body>
        {sortStatus.data.slice(getSliceRng(), (getSliceRng() + 16))
          .map(({ Symbol, Meta_MLP, MIM_morbid_accession, Ensembl, percentile }) => (
            <Table.Row positive={Symbol === props.selectedRow} onClick={props.onRowSelect} key={`${Symbol}_${Math.random()}`}>
              <Table.Cell id={Symbol}>{Symbol}</Table.Cell>
              <Table.Cell id={Symbol}>{Ensembl}</Table.Cell>
              <Table.Cell id={Symbol}> 
                {' '}
                {MIM_morbid_accession.length > 0 ? (
                  <>
                    <label>{MIM_morbid_accession}</label> 
                    {' '}
                    <a href={`https://www.omim.org/${MIM_morbid_accession}`} target="_blank"><Icon link name="external alternate" /></a>
                  </>
                ) : <>N/A</>}
                {' '}
              </Table.Cell>
              <Table.Cell id={Symbol}>{percentile}</Table.Cell>
              <Table.Cell id={Symbol}>{parseFloat(Meta_MLP).toFixed(4)}</Table.Cell>
            </Table.Row>
          ))}
      </Table.Body>
      <br />
      <Table.Footer fullWidth>
        <Table.Row verticalAlign="middle">
          <Pagination
            activePage={currPage}
            ellipsisItem={{ content: <Icon name="ellipsis horizontal" />, icon: true, type: 'ellipsisItem' }}
            firstItem={{ content: <Icon name="angle double left" />, icon: true, type: 'firstItem' }}
            lastItem={{ content: <Icon name="angle double right" />, icon: true, type: 'lastItem' }}
            prevItem={{ content: <Icon name="angle left" />, icon: true, type: 'prevItem' }}
            nextItem={{ content: <Icon name="angle right" />, icon: true, type: 'nextItem' }}
            totalPages={numOfPages}
            onPageChange={(e, data) => setPage(data.activePage)}
          />

        </Table.Row>
      </Table.Footer>

    </Table>

  )
}

export default ResultsTable;
// currPage < numOfPages ? setPage(e.target.innerText) : ''
