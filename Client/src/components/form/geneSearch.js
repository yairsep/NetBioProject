/* eslint-disable react/destructuring-assignment */
import React, { useState, useEffect } from 'react';
import { Dropdown, Header, Search } from 'semantic-ui-react'
import Select, { components } from 'react-select'
import generateGUID from '../common/utilities';

const GeneSearch = (props) => {
  const [searchValue, setSearchValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState([])
  const [selectedGenes, setGenes] = useState([])

  useEffect(() => {
    if (props.disabled) setSearchValue('')
    setGenes([])
  }, [props.disabled])

  useEffect(() => {
    setIsLoading(false);
  }, [results]);

  useEffect(() => {
    props.onGeneSelect(selectedGenes)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedGenes]);

  const url = (value) => `https://mygene.info/v2/query/?q=symbol:${value} OR symbol: ${value}* OR name:${ 
    value}* OR alias: ${value}* OR summary:${value}* OR ${value 
  }*&species=9606&fields=name,symbol,ensembl.gene,entrezgene,type_of_gene&limit=20`;

  const handleBarSelections = (data, e) => {
    if (e.action === 'select-option') setGenes([...selectedGenes, e.option.value])
    else if (e.action === 'remove-value') setGenes(selectedGenes.filter((x) => x !== e.removedValue))
    else if (e.action === 'clear') setGenes([])
  }

  const handleMenuClose = () => {
    setSearchValue('')
    setResults([])
  }

  const handleSearchChange = (value) => {
    setSearchValue(value)
    if (value !== '') {
      setIsLoading(true)
      fetch(url(value))
        .then((res) => res.json())
        .then((summary) => summary.hits.map(({ symbol, name }, i) => ({ key: i, description: name, name: symbol })))
        .then((genesArr) => genesArr.slice(0, 6))
        .then((slicedGenesArr) => setResults(slicedGenesArr))
    }
  }

  const options = results.map((item) => ({ key: item.key, text: item.description, value: item.name }))
  // content: (<Header content={item.name} subheader={item.description}/>)}))

  const optionHeader = ({ key, text, value }) => (
    <Header key={key} content={value} subheader={text} size="tiny" icon="dna" textAlign="left" />
  )

  // eslint-disable-next-line no-shadow
  const MultiValue = (props) => 
  // console.log(props)
    (
      <components.MultiValue {...props} key={generateGUID}>
        {props.data}
      </components.MultiValue>
    )

  const renderLabel = (label) => ({
    color: 'blue',
    content: label.text,
    icon: 'dna',
    size: 'mini'
  })

  return (
    <div className="ui grid">
      <div className="column" style={{ width: '100vh' }}>
        <br />
        <Select
          options={options}
          formatOptionLabel={optionHeader}
          components={{ MultiValue }}
          placeholder="Search Genes..."
          isLoading={isLoading}
          isMulti="true"
          onChange={handleBarSelections}
          isDisabled={props.disabled}
          onInputChange={handleSearchChange}
          onMenuClose={handleMenuClose}
          value={props.totalSelectedGenes}
        />

      </div>
    </div>

  )
}

export default GeneSearch;
