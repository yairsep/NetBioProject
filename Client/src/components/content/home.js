import React, { useState, useEffect } from 'react';
import { Dropdown, Input, Button, Icon, Grid, Segment, Checkbox } from 'semantic-ui-react';
import { withRouter, useHistory } from 'react-router-dom';
import tissues from '../common/tissues';
import Uploader from '../form/uploader'
import GeneSearch from '../form/geneSearch'
const Home = (props) => {
  const [selectedTissue, setTissue] = useState('heart')
  const [submissionPerm, setSubmissionPerm] = useState(false)
  const [userName, setUserName] = useState('')
  const [inputFormat, setInputFormat] = useState('VCF')
  const [inputData, setInputData] = useState(['', []]);   //[fileName, Data]
  const [genomeVersion, setGenomeVersion] = useState('hg38')
  let history = useHistory()

  useEffect(() => {
    setSubmissionPerm(inputData[1].length > 0)
  })

  const onInputFormatSelect = (e, { value }) => {
    setInputFormat(value)
    setInputData(['', []])

    value !== 'VCF' ? setGenomeVersion('') : setGenomeVersion('hg38')
  }

  const onGeneResultSelect = (genes) => {
    setInputData(['', genes])
}

const onFileUpload = (e) => {
  const file = e.target.files[0]
  var fileName = file.name
  var reader = new FileReader();
  reader.onloadend = () => setInputData([fileName, reader.result])
  reader.readAsText(file)
}

  const onSubmit = (e) => {
    e.preventDefault()
    let genes = inputData[1]
    inputFormat === 'simpleFile'
      ? genes = genes.split(/\r\n|\n|\r/)
      : null
    
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
          <h1>Welcome to the Whateveristhename</h1>
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
                defaultSearchQuery="heart"
                defaultValue="heart"
                style={{ zIndex: '12' }}
              />
            </Grid.Column>
          </Grid.Row>

          <Grid.Row>
            <Grid.Column width={8}>
              <label htmlFor="organism">Upload your input Genes with one of the following:</label>
            </Grid.Column>
          </Grid.Row>
          
          <Segment placeholder size='big' style={{width: "100%"}}>
            <Grid stackable textAlign='center' columns={3} divided >
              <Grid.Column>
                <Checkbox
                  radio
                  value='VCF'
                  onChange={onInputFormatSelect}
                  checked={inputFormat === 'VCF'}
                  label='VCF File'
                />
                  {/* <Popup style={{display: 'inline-block'}} content={popups.vcf} position='top right' size={'small'} trigger={ <sup>&nbsp;&nbsp;&nbsp;&nbsp;?</sup> }/> */}
                <br /><br />
                <div>
                  <Uploader type="VCF" onFileUpload={onFileUpload} data={inputData} disabled={inputFormat !== 'VCF'}/>
                </div>
                <br />
                <div>
                  <Checkbox
                    radio
                    value='hg38'
                    onChange={onGenomeVersionSelect}
                    checked={genomeVersion === 'hg38'}
                    label='hg38'
                    disabled={inputFormat !== 'VCF'}
                  />
                  <Checkbox
                    radio
                    value='hg37'
                    onChange={onGenomeVersionSelect}
                    checked={genomeVersion === 'hg37'}
                    label='hg37'
                    disabled={inputFormat !== 'VCF'}
                  />
                </div>
              </Grid.Column>

              <Grid.Column>
                <Checkbox
                  radio
                  value='manual'
                  onChange={onInputFormatSelect}
                  checked={inputFormat === 'manual'}
                  label='Manual Search'
                  style={{ zIndex: '10' }}
                />
                <br />
                <GeneSearch onGeneSelect={onGeneResultSelect} disabled={inputFormat !== 'manual'} totalSelectedGenes={inputData[1]}/>
              </Grid.Column>

              <Grid.Column>
                <Checkbox
                  radio
                  value='simpleFile'
                  onChange={onInputFormatSelect}
                  checked={inputFormat === 'simpleFile'}
                  label='Simple Text File'
                />
                <br /><br />
                <div>
                  <Uploader type="simple" onFileUpload={onFileUpload} data={inputData} disabled={inputFormat !== 'simpleFile'}/>
                </div>
              </Grid.Column>
            </Grid>
          </Segment>

          <Grid.Row>
            <Button 
              color="blue" icon labelPosition="right" style={{margin: 'auto'}}
              disabled={!submissionPerm}
              onClick={onSubmit}>
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
