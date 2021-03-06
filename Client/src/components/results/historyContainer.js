import React, { useEffect, useState } from 'react';
import { Label, Dropdown, Placeholder, Loader } from 'semantic-ui-react';
import { useHistory, withRouter, useLocation } from 'react-router-dom';
import ResultsTable from '../content/resultsTable';
import tissues from '../common/tissues';
import Tabs from '../common/tabs';
import { fetchHistory, fetchShapImgUrl } from '../Genomics/genomics_api';

const HistoryContainer = () => {
  const [selectedRow, selectRow] = useState(null)
  const [isFetched, setFetchStatus] = useState(false)
  const [selectedTissue, setSelectedTissue] = useState('Heart-Left-Ventricle')
  const [results, setResults] = useState([])
  const [shapData, setShapData] = useState({ url: '', isReady: false })
  const [timestamp, setTimestamp] = useState()

  const location = useLocation()

  const onRowSelect = (e) => selectRow(e.target.id)

  const summary = {
    tissue: selectedTissue,
    gene_not_in_db: NaN
  }

  useEffect(() => {
    const fetchData = async () => {
      let { pathname } = location
      pathname = pathname.split('/')
      const timestampFromPath = pathname[2]
      const tissue = pathname[3]
      setTimestamp(timestampFromPath)
      setSelectedTissue(tissue)
      const res = await fetchHistory(timestampFromPath, tissue)
      setResults(res[0])
      console.log(res)
      setShapData({
        isReady: true,
        url: fetchShapImgUrl(timestampFromPath, tissue)
      })

      setFetchStatus(true)
    }
    fetchData()
  }, [location])

  return (
    isFetched ? (
      <div className="ui grid">
        <div
          className="sixteen wide tablet ten wide computer center aligned column"
          style={{ paddingRight: '0.2rem' }}
        >

          <div className="ui basic segment">
            <div className="ui center aligned segment" style={{ overflow: 'auto' }}>
              <ResultsTable tableData={results} onRowSelect={onRowSelect} selectedRow={selectedRow} />
            </div>
          </div>
        </div>

        <div className="computer only six wide centered column" style={{ paddingLeft: '0.1rem' }}>
          <div className="ui basic segment">
            <div className="ui segment">
              <Tabs data={results} summaryData={summary} gene={selectedRow} style={{ width: '0', minWidth: '100%' }} shapData={shapData} />
            </div>
          </div>
        </div>
      </div>
    ) : (
      <div>
        <Placeholder fluid>
          <div className="ui grid">
            <div
              className="sixteen wide tablet nine wide computer centered column"
              style={{ paddingRight: '0.2rem' }}
            >
              <div className="ui basic segment">
                <div className="ui segment" style={{ height: '80vh', overflow: 'auto' }}>
                  <Placeholder>
                    <Loader active />
                  </Placeholder>
                </div>
              </div>
            </div>

            <div className="computer only seven wide centered column" style={{ paddingLeft: '0.1rem' }}>
              <div className="ui basic segment">
                <div className="ui segment" style={{ height: '40vh', overflow: 'auto' }}>
                  <Placeholder>
                    <Loader active />
                  </Placeholder>
                </div>
              </div>
            </div>
          </div>
        </Placeholder>
      </div>  
    )
  )
};

export default withRouter(HistoryContainer);
