//import React from 'react'
import axios from 'axios'

const baseUrl = 'https://netbio.bgu.ac.il/pathosearch-api';

export const fetchSample = async () => {
  const res = await axios.get(`${baseUrl}/sample`)
  return res.data
}

export const fetchGene = async ({ genes, genomeVersion, inputFormat, tissue }) => {
  const res = await axios.post(`${baseUrl}/api/genes`, { genes, genomeVersion, inputFormat, tissue })
  console.log(res.data.genes)
  // return res.data
  return await fetchSample()
}
