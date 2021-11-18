//import React from 'react'
import axios from 'axios'

const baseUrl = 'https://netbio.bgu.ac.il/pathosearch-api';

export const fetchGene = async (props) => {
  console.log(props)
}

export const fetchSample = async (sampleTissue) => {
  const res = await axios.get(`${baseUrl}/sample/${sampleTissue}`)
  return res.data
}
