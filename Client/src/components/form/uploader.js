import React, { useState, useEffect, useRef } from 'react';

const Uploader = (props) => {
  const inputFile = React.createRef()

  const openBrowser = (e) => {
    e.preventDefault()
    inputFile.current.click()
  }

  return (
    (props.data[0] !== '' && !props.disabled) ? (
      <div>
        <input type="file" ref={inputFile} className="ui file" onChange={props.onFileUpload} style={{ display: 'none' }} />
        <button className="ui centered large green button" onClick={openBrowser}>
          <i className="ui upload icon" />
          {props.data[0]}
        </button>
      </div>
    ) : (
      <div>
        <input type="file" ref={inputFile} className="ui file" onChange={props.onFileUpload} style={{ display: 'none' }} />
        <button className="ui icon large file-button button" onClick={openBrowser} disabled={props.disabled}>
          <i className="ui upload icon" />
          Upload {props.type} File
        </button>
      </div>
    )
  )
}

export default Uploader;
