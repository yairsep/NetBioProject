import axios from 'axios'

const baseUrl = 'http://localhost:5000';

export const fetchCadd = async () => {
    const res = await axios.get(`${baseUrl}/cadd`)
    return res.data
}

export const fetchTrace = async () => {
    const res = await axios.get(`${baseUrl}/trace`)
    return res.data
}