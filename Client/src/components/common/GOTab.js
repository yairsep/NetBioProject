import React, { useState, useEffect } from 'react';
import { Card } from 'semantic-ui-react'

const GOTab = (props) => {
  const { gene } = props
  const [entrez, setEntrez] = useState('N/A')
  const [ensembl, setEnsembl] = useState('N/A')
  const [description, setDescription] = useState(null)
  const [isLoading, setLoading] = useState(false)

  useEffect(() => {
    if (gene !== null) {
      setLoading(true)
      fetch(`http://mygene.info/v3/query?q=symbol:${gene}&fields=entrezgene,ensembl.gene`)
        .then((res) => res.json())
        .then((json) => {
          const hits = json['hits'];
          ((hits !== undefined && hits.length > 0 && hits[0].hasOwnProperty('ensembl')) ? setEnsembl(hits[0]['ensembl']['gene']) : setEnsembl('N/A'));
          ((hits !== undefined && hits.length > 0 && hits[0].hasOwnProperty('entrezgene')) ? setEntrez(hits[0]['entrezgene']) : setEntrez('N/A'));
          setDescription(null)
        });
      setLoading(false)
    }
  }, [gene]);

  useEffect(() => {
    if (ensembl !== 'N/A') {
      setLoading(true)
      fetch(`https://mygene.info/v3/gene/${ensembl}?fields=summary`)
        .then((res) => res.json())
        .then((json) => setDescription(json['summary']));
    }
    setLoading(false)
  }, [ensembl]);

  return (
    gene === null ? (
      <>
        <br />
        <i>Select Gene from the table</i>
      </>
    ) : (
      isLoading ? (
        <Card style={{ width: '100%' }}>
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <div className="ui active intermediate text loader">
            <p>Please wait...</p>
          </div>
        </Card>
      ) : (
        <Card style={{ width: '100%' }}>
          <Card.Content>
            <Card.Header>
              {gene}
              <br />
            </Card.Header>
            <Card.Description>
              Ensembl : 
              {' '}
              {ensembl}
              <br />
              <br />
              Entrez : 
              {' '}
              {entrez}
              <br />
              <br />
              {description}
            </Card.Description>
          </Card.Content>
        </Card>
      ))
  )
}

export default GOTab;
