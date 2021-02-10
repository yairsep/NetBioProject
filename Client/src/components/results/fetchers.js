//import React from 'react'
import axios from 'axios'

const baseUrl = 'https://netbio.bgu.ac.il/chananproject';

export const fetchGene = (props) => (null)

export const fetchSample = async () => {
  console.log('ssssss')
  const res = await axios.get(`${baseUrl}/sample`)
  console.log(res)
  return res.data
}
