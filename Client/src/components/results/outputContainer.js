/* eslint-disable react/button-has-type */
import React, { useEffect, useState } from 'react';
import { Label, Dropdown, Placeholder, Loader } from 'semantic-ui-react';
import { useHistory, withRouter, useLocation } from 'react-router-dom';
import ResultsTable from '../content/resultsTable';
import tissues from '../common/tissues';
import sampleTissues from '../common/sampleTissues';
import Tabs from '../common/tabs';
import { sendVcfFile, fetchSample, fetchShap, fetchShapImgUrl, updateShap } from '../Genomics/genomics_api';


const OutputContainer = (props) => {
  const location = useLocation()
  const { pathname } = location

  const initialTissue = () => {
    // eslint-disable-next-line no-use-before-define
    if (pathname.includes('Example')) {
      return 'brain';
    // eslint-disable-next-line no-else-return
    } else if (props.location.data) {
      return props.location.data.tissue;
    } else return localStorage.getItem('tissuePathoSearch');
  }

  const history = useHistory();
  const [selectedRow, selectRow] = useState(0)
  const [isFetched, setFetchStatus] = useState(false)
  const [isError, setError] = useState(null)
  const [selectedTissue, setNewTissue] = useState(initialTissue())
  const [results, setResults] = useState([])
  const [time, setTime] = useState()
  const [genomeVersion, setGenomeVersion] = useState("GRCh37")
  const [shapData, setShapData] = useState({ url: '', isReady: false })
  const [selectedGene, selectGene] = useState()
  let { data } = history.location
  if (!data && pathname.includes('results')) JSON.parse(localStorage.getItem('pathoSearchData'))

  const summary = {
    tissue: data?.tissue || selectedTissue,
    gene_not_in_db: 'test'
  }

  const checkImage = path =>
    new Promise(resolve => {
        const img = new Image();
        img.onload = () => resolve(true);
        img.onerror = () => resolve(false);

        img.src = path;
  });

  const onRowSelect = (e, rowIdx) => {
    setShapData({
      isReady: false,
    })
    const makeShapUpdate = async() =>{
      selectGene(e.target.id)
      selectRow(rowIdx)
      console.log("^^^^^^^^^^^^^^^^^^")
      console.log(rowIdx)
      // setTime(timeStamp)
      console.log(rowIdx)
      const path = fetchShapImgUrl(time, selectedTissue, rowIdx)
      const imgExists = await checkImage(path)
      if (imgExists){
        setShapData({
          url: path,
          isReady: true,
        })
      }
      else{
        await updateShap(time ,selectedTissue, genomeVersion, rowIdx)
        setShapData({
          url: fetchShapImgUrl(time, selectedTissue, rowIdx),
          isReady: true,
        })
      } 
        // localStorage.setItem('shap', fetchShapImgUrl(fullRes[1].time))
    }
    makeShapUpdate()
  }

  const changeTissue = (e, { value }) => {
    // eslint-disable-next-line no-const-assign
    // if (props.location.state === 'sample') location = undefined;
    setFetchStatus(false)
    setNewTissue(value)
    if (!data) {
      data = JSON.parse(localStorage.getItem('pathoSearchData'))
    }
    if (data) {
      console.log('Start removing from localStorage')
      localStorage.removeItem('gene')
      localStorage.removeItem('tissuePathoSearch')
      localStorage.removeItem('timeSig')
      localStorage.removeItem('pathoSearchData')
      if(pathname.includes('results')){
        history.push({
          pathname: `/results/${value}`,
          data: { tissue: value, genes: data.genes, inputFormat: data.inputFormat, genomeVersion: data.genomeVersion }
        })
      }
    }
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        let vcfData = {}
        if (data) {
          vcfData = { genes: data.genes, tissue: data.tissue, inputFormat: data.inputFormat, genomeVersion: data.genomeVersion }
          localStorage.setItem('pathoSearchData', JSON.stringify(data))
        }

        const fullRes = await (pathname.includes('results') ? sendVcfFile(vcfData) : fetchSample(selectedTissue))
        console.log("********************")
        console.log(fullRes)
        let res

        if (pathname.includes('results')) {
          // eslint-disable-next-line prefer-destructuring
          res = fullRes[0]
          console.log(`time changed to:${fullRes[1].time}`)
          setTime(fullRes[1].time)
          try {
            await fetchShap(fullRes[1].time, vcfData.tissue, vcfData.genomeVersion)
            setShapData({
              url: fetchShapImgUrl(fullRes[1].time, vcfData.tissue, selectedRow),
              isReady: true,
            })
            // localStorage.setItem('shap', fetchShapImgUrl(fullRes[1].time))
          } catch {
            console.log("can't fetch shap image")
          }
          localStorage.setItem('gene', JSON.stringify(res))
          localStorage.setItem('tissuePathoSearch', selectedTissue)
          localStorage.setItem('timeSig', fullRes[1].time)
          localStorage.setItem('selectedRow', selectedRow)
        } else {
          res = fullRes
          console.log('res', res)
          setShapData({
            url: fetchShapImgUrl('sample', selectedTissue, selectedRow),
            isReady: true,
          })
        }
        setResults(res)
        setFetchStatus(true)
      } catch (err) {
        console.log(`Error: ${err}`)
        setError(err)
        setFetchStatus(false)
      }
    }
    if (localStorage.getItem('gene') && pathname.includes('results')) {
      setResults(JSON.parse(localStorage.getItem('gene')))
      console.log(results)
      setTime(localStorage.getItem('timeSig'))
      setShapData({
        isReady: true,
        url: fetchShapImgUrl(localStorage.getItem('timeSig'), localStorage.getItem('tissuePathoSearch'), localStorage.getItem('selectedRow'))
      })
      setFetchStatus(true)
      // eslint-disable-next-line react-hooks/exhaustive-deps
      data = JSON.parse(localStorage.getItem('pathoSearchData')) //Probably can erase this
    } else {
      fetchData()
    }
  }, [pathname, history, selectedTissue]);
  
  return (
    isError == null && isFetched ? (
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

          <div className="ui basic segment">
            <div className="ui center aligned segment">
              {time && pathname.includes('results') 
                && (
                  <>
                    <p>
                      You can come back to your results at <a href={`https://netbio.bgu.ac.il/tracevar/#findResult/${time}/${selectedTissue}`} target="_blank" rel="noreferrer">this link.</a>
                      {/* You can come back to your results at <a href={`http://localhost:8080/#findResult/${time}/${selectedTissue}`} target="_blank" rel="noreferrer">this link.</a> */}
                    </p>
                    <p>
                      Please keep it for future use!
                    </p>
                  </>
                )}
            </div>
          </div>
            <div style={{ textAlign: 'center' }}>
              <Label size="big" style={{ lineHeight: '2em' }}>
                Switch tissue model
                <Label.Detail>
                  <Dropdown 
                    name="tissue"
                    options={pathname.includes('results') ? tissues : sampleTissues}
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
              <Tabs data={results} summaryData={summary} gene={selectedGene} style={{ width: '0', minWidth: '100%' }} shapData={shapData} />
              {/* {shap && <img src={fetchShapImgUrl(time)} alt="shap chart" width="100%" />} */}
            </div>
          </div>
        </div>
      </div>
    )
      : isError == null ? (
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
        : (
          <div>
            <h1>{`${isError}`}</h1>
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
