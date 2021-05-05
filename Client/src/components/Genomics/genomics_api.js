import axios from 'axios'

const baseUrl = 'http://localhost:5000';
// const baseUrl = 'https://netbio.bgu.ac.il/pathosearch-api';

export const fetchCadd = async () => {
  const res = await axios.get(`${baseUrl}/cadd`)
  return res.data
}

export const fetchTrace = async () => {
  const res = await axios.get(`${baseUrl}/trace`)
  return res.data
}

export const fetchSample = async () => {
  console.log('FetchSample')
  const res = await axios.get(`${baseUrl}/sample`)
  return res.data
}

export const sendVcfFile = async (vcfFile) => {
  console.log('vcfFile:', vcfFile)
  const res = await axios.post(`${baseUrl}/vcf`, vcfFile)
  console.log('my res.data', res.data)
  console.log('my res', res)
  return res.data
}
