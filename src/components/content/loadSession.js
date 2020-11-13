import React, { useState, useEffect } from 'react';
import { Loader } from 'semantic-ui-react';
import SessionList from '../common/sessionList';
import { getSessions } from '../common/fetchers';

const LoadSession = (props) => {
  const { userName } = localStorage
  const [isFetched, setFetchStatus] = useState(false)
  const [sessions, setSessions] = useState([])


  // useEffect(() => {
  //     if (userName !== undefined && userName !== null) {
  //         const response = getSessions()
  //         console.log(response)
  //         setSessions(res.getSessions.message)
  //         setFetchStatus(true)
  //     }
  // }, [])

  return (
    <div className="ui segment centered very padded">
      <div className="ui header">Previous Sessions</div>
      { userName === undefined ? (
        <div>
          <p>You need to log in to see the sessions</p>
        </div>
      ) : (
        <div>
          {isFetched ? (
            <div>
              <p>
                For
                {userName}
              </p>
              <SessionList sessions={sessions} />
            </div>
          ) : (
            <Loader active />
          )}
        </div>
      )}
    </div>
  )
}

export default LoadSession;
