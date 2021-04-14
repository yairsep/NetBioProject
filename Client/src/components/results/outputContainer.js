/* eslint-disable react/button-has-type */
import React, { useEffect, useState } from 'react';
import { Grid, Label, Dropdown, Placeholder, Loader } from 'semantic-ui-react';
import { useHistory, withRouter, useLocation } from 'react-router-dom';
import { fetchGene, fetchSample } from './fetchers';
import ResultsTable from '../content/resultsTable';
import tissues from '../common/tissues';
import Tabs from '../common/tabs';
import { sendVcfFile } from '../Genomics/genomics_api';

const OutputContainer = (props) => {
  const initialTissue = () => {
    // eslint-disable-next-line no-use-before-define
    if (pathname.includes('Example')) {
      return 'heart';
    // eslint-disable-next-line no-else-return
    } else if (props.location.data) {
      return props.location.data.tissue;
    } else return localStorage.tissue;
  }

  const location = useLocation()
  const { pathname } = location
  const history = useHistory();
  const [selectedRow, selectRow] = useState(null)
  const [isFetched, setFetchStatus] = useState(false)
  const [selectedTissue, setNewTissue] = useState(initialTissue())
  const [results, setResults] = useState([]);
  const summary = {
    tissue: {
      text: 'test'
    },
    gene_not_in_db: 'test'
  }
  const onRowSelect = (e) => selectRow(e.target.id)

  const changeTissue = (e, { value }) => {
    //TODO: If Switch tissue in sample, this shouldn't be sample anymore
    // eslint-disable-next-line no-const-assign
    // if (props.location.state === 'sample') location = undefined;
    setFetchStatus(false)
    setNewTissue(value)
  }

  useEffect(() => {
    //TODO:Switch to sample from the algorithm run
    const fetchData = async () => {
      const { data } = history.location
      const vcfData = { genes: data.genes, tissue: data.tissue, inputFormat: data.inputFormat, genomeVersion: data.genomeVersion }
      const res = await (pathname.includes('results') ? sendVcfFile(vcfData) : fetchSample())
      console.log(res)
      setResults(res)
      setFetchStatus(true)
    }
    fetchData()
  }, [pathname, history, selectedTissue]);
  
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
          <div style={{ textAlign: 'center' }}>
            <Label size="big" style={{ lineHeight: '2em' }}>
              Switch tissue model
              <Label.Detail>
                <Dropdown 
                  name="tissue"
                  options={tissues}
                  onChange={changeTissue}
                  defaultValue={selectedTissue}
                  labeled
                  button
                  icon="exchange"
                  className="ui black icon"
                />
              </Label.Detail>
            </Label>
          </div>
        </div>

        <div className="computer only six wide centered column" style={{ paddingLeft: '0.1rem' }}>
          <div className="ui basic segment">
            <div className="ui segment">
              <Tabs data={results} summaryData={summary} gene={selectedRow} style={{ width: '0', minWidth: '100%' }} />
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
  );
};

export default withRouter(OutputContainer);

//  

// return (
//   <>
//     <Grid.Column width={10} />
//     <Grid.Column width={6} />
//   </>
// );
