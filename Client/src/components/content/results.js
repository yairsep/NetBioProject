/* eslint-disable block-scoped-var */
/* eslint-disable no-var */
/* eslint-disable vars-on-top */
import React, { useState, useEffect } from 'react';
import { Dropdown, Label, Loader, Placeholder } from 'semantic-ui-react';
import { Table } from 'semantic-ui-react/dist/commonjs/collections/Table/Table';
import { withRouter } from 'react-router-dom';
import Uploader from '../form/uploader';
import Tabs from '../common/tabs';
import ResultsTable from './resultsTable'
import tissues from '../common/tissues';
// eslint-disable-next-line import/named
import { getRandomSession, getSession, postSession, postSessionGenes, postSessionVcf } from '../common/fetchers';

const Results = (props) => {
  const initialTissue = () => {
    if (props.location.state === 'sample') { return 'heart'; }
    if (props.location.data) { return props.location.data.tissue; }
    return localStorage.tissue;
  }

  const [summary, setSummary] = useState();
  const [resultsData, setData] = useState();
  const [isError, setError] = useState(false)
  const [isFetched, setFetchStatus] = useState(false)
  const [selectedRow, selectRow] = useState(null)
  const [selectedTissue, setNewTissue] = useState(initialTissue())

  useEffect(() => {
    const fetchResults = async () => {
      // console.log('props', props)
      // console.log('localStorage', localStorage)
      // console.log('selectedTissue',selectedTissue)

      let response;

      if (props.location.state === 'sample') { //In case of Sample
        response = await getRandomSession()
        console.log('sample', response)
      } else {
        //Configuration part

        var genes; var 
          inputFormat;
        if (props.location.data) { //In case of new request
          genes = props.location.data.genes
          inputFormat = props.location.data.inputFormat
        } else {
          genes = JSON.parse(localStorage.getItem('genes')) //In case of old request (refreshed page, etc)
          inputFormat = localStorage.getItem('inputFormat')
        }

        //Fetching part
        if (inputFormat === 'VCF') {
          console.log('conf', selectedTissue, genes, inputFormat)
          response = await postSessionVcf(selectedTissue, genes)
          console.log('response', response)
        } else {
          console.log('conf', selectedTissue, genes, inputFormat)
          response = await postSessionGenes(selectedTissue, genes)
          console.log('response', response)
        }
      }

      if (response.genes) {
        setData(response.genes)
        setSummary(response.summary)
        setFetchStatus(true)
        console.log('great success')
        //Saving configuration for the case of re-render
        localStorage.setItem('tissue', selectedTissue)
        localStorage.setItem('inputFormat', inputFormat)
        if (props.location.state === 'sample') { localStorage.setItem('genes', JSON.stringify(response.genes.map((g) => g['Ensembl']))) } else localStorage.setItem('genes', JSON.stringify(genes))
      } else {
        setError(true)
      }
    }
    fetchResults()
  }, [selectedTissue]);

  const changeTissue = (e, { value }) => {
    if (props.location.state === 'sample') props.location.state = undefined;
    setFetchStatus(false)
    setNewTissue(value)
  }

  const onRowSelect = (e) => selectRow(e.target.id)

  return (
    isError ? (
      <div className="twelve wide right floated column">
        <div className="ui segment centered very padded">
          <p>
            Unfortunately, something went wrong.
            <br />
            If the problem persists please send us an email at:
            <a href="mailto:estiyl@bgu.ac.il">estiyl@bgu.ac.il</a>
          </p>
        </div>
      </div>
    ) : (
      isFetched ? (
        <div>
          <div className="ui grid">
            <div
              className="sixteen wide tablet ten wide computer center aligned column"
              style={{ paddingRight: '0.2rem' }}
            >
              <div className="ui basic segment">
                <div className="ui center aligned segment" style={{ overflow: 'auto' }}>

                  <ResultsTable tableData={resultsData} onRowSelect={onRowSelect} selectedRow={selectedRow} />
                  {/*<br/><br/>*/}

                </div>
              </div>

              {/* <div style={{ textAlign: 'center' }}>
                <label>Switch Tissue for your query</label>
                <span>&nbsp;&nbsp;</span>
                <Dropdown name="tissue"
                options={tissues}
                onChange={changeTissue}
                defaultValue={selectedTissue}
                floating
                labeled
                button
                icon='exchange'
                className='icon'
                />
                <Label size="big" style={{ lineHeight: '2em' }}>
                  Switch tissue for your query
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
              </div> */}
            </div>

            <div className="computer only six wide centered column" style={{ paddingLeft: '0.1rem' }}>
              <div className="ui basic segment">
                <div className="ui segment">
                  <Tabs data={resultsData} summaryData="summary" gene={selectedRow} style={{ width: '0', minWidth: '100%' }} />
                </div>
              </div>
            </div>
          </div>
          <br />
          <div className="ui center aligned text container">

            {/*<JobLink userName={localStorage.userName} jobTime={localStorage.Time} jobName={localStorage.jobName}/>*/}
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
  )
}

export default withRouter(Results);
