/* eslint-disable react/button-has-type */
import React, {useEffect, useState} from 'react';
import {useHistory, withRouter, useLocation} from 'react-router-dom';
import {fetchCadd} from './genomics_api';

const Cadd = () => {

    const location = useLocation()
    const {pathname} = location
    const history = useHistory();
    const [caddData, setCaddData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const data = await fetchCadd();
            setCaddData(data)
        }
        fetchData()
    }, [pathname, history]);

    return (

        <div>
            <h1>Cadd Api</h1>
            <div>
                {caddData}
            </div>
        </div>
    );
};

export default withRouter(Cadd);