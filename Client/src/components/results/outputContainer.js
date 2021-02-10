/* eslint-disable react/button-has-type */
import React, { useEffect, useState } from 'react';
import { Grid, Label, Dropdown } from 'semantic-ui-react';
import { useHistory, withRouter } from 'react-router-dom';
import { fetchGene, fetchSample } from './fetchers';
import sample from './sample';
import ResultsTable from '../content/resultsTable';
import tissues from '../common/tissues';
import Tabs from '../common/tabs';

const OutputContainer = (props) => {
  const initialTissue = () => {
    // eslint-disable-next-line no-use-before-define
    if (location === 'sample') {
      return 'heart';
    // eslint-disable-next-line no-else-return
    } else if (props.location.data) {
      return props.location.data.tissue;
    } else return localStorage.tissue;
  }

  const { location } = 'sample';//props;
  //const { pathname } = location;
  const history = useHistory();
  const [selectedRow, selectRow] = useState(null)
  const [isFetched, setFetchStatus] = useState(false)
  const [selectedTissue, setNewTissue] = useState(initialTissue())
  const [samples, setSamples] = useState([]);
  const summary = {
    tissue: {
      text: 'test'
    },
    gene_not_in_db: 'test'
  }
  const onRowSelect = (e) => selectRow(e.target.id)

  const changeTissue = (e, { value }) => {
    // eslint-disable-next-line no-const-assign
    if (props.location.state === 'sample') location = undefined;
    setFetchStatus(false)
    setNewTissue(value)
  }

  useEffect(() => {
    console.log(history.location.data);
    //pathname.includes('results') ? fetchGene() : fetchSample();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  
  return (
    <div className="ui grid">
      <div
        className="sixteen wide tablet ten wide computer center aligned column"
        style={{ paddingRight: '0.2rem' }}
      >

        <div className="ui basic segment">
          <div className="ui center aligned segment" style={{ overflow: 'auto' }}>
            <ResultsTable tableData={sample} onRowSelect={onRowSelect} selectedRow={selectedRow} />
            {/*<br/><br/>*/}
          </div>
        </div>
      </div>

      <div className="computer only six wide centered column" style={{ paddingLeft: '0.1rem' }}>
        <div className="ui basic segment">
          <div className="ui segment">
            <Tabs data={sample} summaryData={summary} gene={selectedRow} style={{ width: '0', minWidth: '100%' }} />
          </div>
        </div>
      </div>
      <div className="ui grid" style={{ textAlign: 'center' }}>
        <label>Switch Tissue for your query</label>
        <span>&nbsp;&nbsp;</span>
        <Dropdown 
          name="tissue"
          options={tissues}
          onChange={changeTissue}
          defaultValue={selectedTissue}
          floating
          labeled
          button
          icon="exchange"
          className="icon"
        />
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
