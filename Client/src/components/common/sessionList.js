import React, { useState, useEffect } from 'react';
import { Table } from 'semantic-ui-react/dist/commonjs/collections/Table/Table';
import { Link } from 'react-router-dom';

const SessionList = (props) => {
  const { sessions, userName } = props

  return (
    sessions.length > 0 ? (
      <div className="ui middle aligned divided list">
        {sessions.map((item) => (
          <div className="item">
            <div className="content">
              <Link to={`/results/${localStorage.userName}/${item[0]}/${item[1]}`}>
                {item[0]}
              </Link>
            </div>
          </div>
        ))}
      </div>
    ) : (
      <div className="ui tiny header">
        You don`t appear to have any sessions yet.
        <br />
        <br />
      </div>
    )
  )
}

export default SessionList;
