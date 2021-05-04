/* eslint-disable react/button-has-type */
import React, { useEffect, useState } from 'react';
import { Grid, Label, Dropdown, Placeholder, Loader } from 'semantic-ui-react';
import { useHistory, withRouter, useLocation } from 'react-router-dom';
import ResultsTable from '../content/resultsTable';
import tissues from '../common/tissues';
import Tabs from '../common/tabs';
import { sendVcfFile, fetchSample } from '../Genomics/genomics_api';

const OutputContainer = (props) => {

  const location = useLocation()
  const { pathname } = location

  
  const initialTissue = () => {
    // eslint-disable-next-line no-use-before-define
    if (pathname.includes('Example')) {
      return 'Heart-Left-Ventricle';
    // eslint-disable-next-line no-else-return
    } else if (props.location.data) {
      return props.location.data.tissue;
    } else return localStorage.getItem('tissuePathoSearch');
  }


  const history = useHistory();
  const [selectedRow, selectRow] = useState(null)
  const [isFetched, setFetchStatus] = useState(false)
  const [selectedTissue, setNewTissue] = useState(initialTissue())
  const [results, setResults] = useState([])
  const [time, setTime] = useState()
  console.log("THIS IS OUTSIDE");
  let { data } = history.location
  if (!data && pathname.includes('results')) JSON.parse(localStorage.getItem('pathoSearchData'))

  const summary = {
    tissue: data?.tissue || selectedTissue,
    gene_not_in_db: 'test'
  }

  const onRowSelect = (e) => selectRow(e.target.id)

  const changeTissue = (e, { value }) => {
    //TODO: If Switch tissue in sample, this shouldn't be sample anymore
    // eslint-disable-next-line no-const-assign
    // if (props.location.state === 'sample') location = undefined;
    setFetchStatus(false)
    setNewTissue(value)
    // console.log(data)
    if (!data) {
      data = JSON.parse(localStorage.getItem('pathoSearchData'))
    }
    if (data) {
      console.log("Start removing from localStorage")
      localStorage.removeItem('gene')
      localStorage.removeItem('tissuePathoSearch')
      localStorage.removeItem('timeSig')
      localStorage.removeItem('pathoSearchData')

      history.push({
        pathname: `/results/${value}`,
        data: { tissue: value, genes: data.genes, inputFormat: data.inputFormat, genomeVersion:data.genomeVersion }
      })
    }
  }


  useEffect(() => {
    const fetchData = async () => {
      console.log("THIS IS INSIDE")
      let vcfData = {}
      if (data) {
        vcfData = { genes: data.genes, tissue: data.tissue, inputFormat: data.inputFormat, genomeVersion: data.genomeVersion }
        localStorage.setItem('pathoSearchData', JSON.stringify(data))
      }

      const fullRes = await (pathname.includes('results') ? sendVcfFile(vcfData) : fetchSample())
      let res
      pathname.includes('results') ? res = fullRes[0] : res = fullRes

      pathname.includes('results') && setTime(fullRes[1].time)

      console.log('res', res)
      setResults(res)
      setFetchStatus(true)

      if (pathname.includes('results')) {
        localStorage.setItem('gene', JSON.stringify(res))
        localStorage.setItem('tissuePathoSearch', selectedTissue)
        localStorage.setItem('timeSig', fullRes[1].time)
      }
    }

    if (localStorage.getItem('gene') && pathname.includes('results')) {
      setResults(JSON.parse(localStorage.getItem('gene')))
      console.log(results)
      setFetchStatus(true)
      setTime(localStorage.getItem('timeSig'))
      data = JSON.parse(localStorage.getItem('pathoSearchData'))
    } else {
      fetchData()
    }
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
              {time && pathname.includes('results') && <p>You can come back to your results in https://netbio.bgu.ac.il/PathoSearch/findResult/{time}</p>}
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
