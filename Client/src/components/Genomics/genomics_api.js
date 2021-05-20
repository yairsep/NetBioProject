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
  return res.data
}

export const fetchShap = async (timestamp) => {
  console.log('fetching shap')
  const res = await axios.post(`${baseUrl}/shap`, { timestamp })
  console.log('my res.data', res.data)
  return res.data
}

export const fetchShapImgUrl = (timestamp) => `${baseUrl}/shap?timestamp=${timestamp}`;

export const fetchHistory = async (timestamp) => {
  const res = await axios.get(`${baseUrl}/history?timestamp=${timestamp}`)
  return res.data
}
