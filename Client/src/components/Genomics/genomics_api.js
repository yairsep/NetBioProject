import axios from 'axios'
const prod = true
// const baseUrl = 'http://localhost:5000';
const baseUrl = prod ? 'https://netbio.bgu.ac.il/pathosearch-api' : 'http://localhost:5000'

export const fetchCadd = async () => {
  const res = await axios.get(`${baseUrl}/cadd`)
  return res.data
}

export const fetchTrace = async () => {
  const res = await axios.get(`${baseUrl}/trace`)
  return res.data
}

export const fetchSample = async (selectedTissue) => {
  console.log('FetchSample')
  const res = await axios.get(`${baseUrl}/sample/${selectedTissue}`)
  return res.data
}

export const sendVcfFile = async (vcfFile) => {
  console.log('vcfFile:', vcfFile)
  const res = await axios.post(`${baseUrl}/vcf`, vcfFile)
  return res.data
}

export const fetchShap = async (timestamp, tissue, genomeVersion) => {
  console.log('fetching shap')
  const res = await axios.post(`${baseUrl}/shap`, { timestamp, tissue, genomeVersion })
  console.log('my res.data', res.data)
  return res.data
}

export const updateShap = async (timeStamp, tissue, genomeVersion, rowNum) => {
  console.log('fetching shap')
  const res = await axios.post(`${baseUrl}/updateShap`, {timeStamp ,tissue, genomeVersion, rowNum })
  console.log('my res.data', res.data)
  return res.data
}

export const fetchShapImgUrl = (timestamp, tissue) => `${baseUrl}/shap?timestamp=${timestamp}&tissue=${tissue}`;

export const fetchHistory = async (timestamp, tissue) => {
  const res = await axios.get(`${baseUrl}/history?timestamp=${timestamp}&tissue=${tissue}`)
  return res.data
}
