import React, { useState, useEffect } from 'react';
import { Loader, Segment } from 'semantic-ui-react'

const ShapImage = (props) => {
  const { shapData } = props

  const [isReady, setIsReay] = useState(false)
  const [source, setSource] = useState(shapData.url);

  useEffect(() => {
    setIsReay(shapData.isReady)
  }, [shapData])



  return (
    isReady 
      ?      <img key={new Date().getTime()} src={shapData.url} alt="shap chart" width="100%" />
      :       <div style={{marginTop:'25px', display: 'flex',alignItems: 'center',justifyContent: 'center',}}><Loader active inline size='large'>Loading Shap...</Loader></div>
  )
}

export default ShapImage;
