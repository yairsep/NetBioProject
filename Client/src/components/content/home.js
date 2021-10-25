import React, { useState, useEffect } from 'react';
import { Dropdown, Button, Icon, Grid, Segment, Checkbox } from 'semantic-ui-react';
import { withRouter, useHistory } from 'react-router-dom';
import tissues from '../common/tissues';
import Uploader from '../form/uploader'
import GeneSearch from '../form/geneSearch'

const Home = () => {
  const [selectedTissue, setTissue] = useState('Heart')
  const [submissionPerm, setSubmissionPerm] = useState(false)
  // const [userName, setUserName] = useState('')
  const [inputFormat, setInputFormat] = useState('VCF')
  const [inputData, setInputData] = useState(['', []]); //[fileName, Data]
  const [genomeVersion, setGenomeVersion] = useState('GRCh38')
  const history = useHistory()
  
  useEffect(() => {
    setSubmissionPerm(inputData[1].length > 0)
  }, [inputData])

  const onInputFormatSelect = (e, { value }) => {
    setInputFormat(value)
    setInputData(['', []])

    value !== 'VCF' ? setGenomeVersion('') : setGenomeVersion('GRCh38')
  }

  const onGeneResultSelect = (genes) => {
    setInputData(['', genes])
  }

  const onFileUpload = (e) => {
    const file = e.target.files[0]
    const fileName = file.name
    const reader = new FileReader();
    reader.onloadend = () => setInputData([fileName, reader.result])
    console.log('reader:', reader.readAsText(file));
  }

  const onSubmit = (e) => {
    e.preventDefault()
    let genes = inputData[1]
    genes = inputFormat === 'VCF'
      ? genes.split(/\r\n|\n|\r/)
      : null
    console.log('genes:', genes);

    localStorage.removeItem('gene')
    localStorage.removeItem('tissuePathoSearch')
    localStorage.removeItem('timeSig')
    localStorage.removeItem('pathoSearchData')
    
    history.push({
      pathname: '/results',
      data: { tissue: selectedTissue, genes, inputFormat, genomeVersion }
    })
  }

  const onGenomeVersionSelect = (e, { value }) => {
    setGenomeVersion(value)
  }

  return (
    <div className="ui ui raised padded container segment">
      <form className="ui form" id="homeForm">

        <div className="ui dividing header">
          <h1>Welcome to TRACEvar</h1>
          <p>Need a header about something</p>
        </div>

        <Grid>
          <Grid.Row>
            <Grid.Column width={6}>
              <label htmlFor="organism">Select Tissue Model:</label>
            </Grid.Column>

            <Grid.Column width={8}>
              <Dropdown
                name="tissue"
                options={tissues}
                onChange={(e, { value }) => setTissue(value)}
                placeholder="Choose an organism"
                fluid
                selection
                defaultSearchQuery="Heart"
                defaultValue="Heart"
                style={{ zIndex: '12' }}
              />
            </Grid.Column>
          </Grid.Row>

          <Grid.Row>
            <Grid.Column width={8}>
              <label htmlFor="organism">Upload your input Genes with one of the following:</label>
            </Grid.Column>
          </Grid.Row>

          <Segment placeholder size="big" style={{ width: '100%' }}>
            <Grid stackable textAlign="center" columns={3} divided>
              <Grid.Column>
                <Checkbox
                  radio
                  value="VCF"
                  onChange={onInputFormatSelect}
                  checked={inputFormat === 'VCF'}
                  label="VCF File"
                />
                {/* <Popup style={{display: 'inline-block'}} content={popups.vcf} position='top right' size={'small'} trigger={ <sup>&nbsp;&nbsp;&nbsp;&nbsp;?</sup> }/> */}
                <br /><br />
                <div>
                  <Uploader type="VCF" onFileUpload={onFileUpload} data={inputData} disabled={inputFormat !== 'VCF'} />
                </div>
                <br />
                <div>
                  <Checkbox
                    radio
                    value="GRCh38"
                    onChange={onGenomeVersionSelect}
                    checked={genomeVersion === 'GRCh38'}
                    label="GRCh38"
                    disabled={inputFormat !== 'VCF'}
                  />
                  <Checkbox
                    radio
                    value="GRCh37"
                    onChange={onGenomeVersionSelect}
                    checked={genomeVersion === 'GRCh37'}
                    label="GRCh37"
                    disabled={inputFormat !== 'VCF'}
                  />
                </div>
              </Grid.Column>

              <Grid.Column>
                <Checkbox
                  radio
                  value="manual"
                  onChange={onInputFormatSelect}
                  checked={inputFormat === 'manual'}
                  label="Manual Search"
                  style={{ zIndex: '10' }}
                  disabled //Remove when the option will be available
                />
                <br />
                <GeneSearch onGeneSelect={onGeneResultSelect} disabled={inputFormat !== 'manual'} totalSelectedGenes={inputData[1]} />
              </Grid.Column>

              <Grid.Column>
                <Checkbox
                  radio
                  value="simpleFile"
                  onChange={onInputFormatSelect}
                  checked={inputFormat === 'simpleFile'}
                  label="Simple Text File"
                  disabled //Remove when the option will be available
                />
                <br /><br />
                <div>
                  <Uploader type="simple" onFileUpload={onFileUpload} data={inputData} disabled={inputFormat !== 'simpleFile'} />
                </div>
              </Grid.Column>
            </Grid>
          </Segment>

          <Grid.Row>
            <Button 
              color="blue"
              icon
              labelPosition="right"
              style={{ margin: 'auto' }}
              disabled={!submissionPerm}
              onClick={onSubmit}
            >
              Submit new job
              <Icon name="check circle" />
            </Button>
          </Grid.Row>
        </Grid>
      </form>
    </div>
  )
};

export default withRouter(Home);
