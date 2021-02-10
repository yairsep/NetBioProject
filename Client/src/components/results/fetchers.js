//import React from 'react'
import axios from 'axios'

const baseUrl = 'https://netbio.bgu.ac.il/pathosearch-api';

export const fetchGene = (props) => (null)

export const fetchSample = async () => {
  const res = await axios.get(`${baseUrl}/sample`)
  return res.data
}
