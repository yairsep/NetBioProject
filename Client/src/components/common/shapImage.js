import React, { useState, useEffect } from 'react';

const ShapImage = (props) => {
  const { shapData } = props

  const [isReady, setIsReay] = useState(false)

  useEffect(() => {
    setIsReay(shapData.isReady)
  }, [shapData])

  return (
    isReady 
      ? <img src={shapData.url} alt="shap chart" width="100%" /> 
      : <div>Sorry! Cannot load Shap graph right now!</div>
  )
}

export default ShapImage;
