/* eslint-disable react/button-has-type */
import React, {useEffect, useState} from 'react';
import {useHistory, withRouter, useLocation} from 'react-router-dom';
import {fetchTrace} from './genomics_api';

const Trace = () => {

    const location = useLocation()
    const {pathname} = location
    const history = useHistory();
    const [TraceData, setTraceData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const data = await fetchTrace();
            setTraceData(data)
        }
        fetchData()
    }, [pathname, history]);

    return (
        <div>
            <h1>Trace Api</h1>
            <p>{TraceData}</p>
        </div>
    );
};

export default withRouter(Trace);