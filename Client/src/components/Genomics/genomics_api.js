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

export const sendVcfFile = async (vcfFile) => {
  const req = await axios.post(`${baseUrl}/vcf`, vcfFile, {headers: {'Access-Control-Allow-Origin': '*'} }).then((response) => {
    console.log('Sent vcf file');
  });
}
