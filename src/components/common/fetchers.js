
export const postSessionVcf = async (tissue, vcf) => {
  const response = await fetch(`http://netbio.bgu.ac.il/trace-api/api/v1/vcf/${tissue}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vcf
    })
  })

  return await response.json();
};

export const postSessionGenes = async (tissue, genes) => {
  const response = await fetch(`http://netbio.bgu.ac.il/trace-api/api/v1/genes/${tissue}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      genes
    })
  })

  return await response.json();
};

export const getRandomSession = async () => {
  const response = await fetch('http://netbio.bgu.ac.il/trace-api/sample', {
    headers: { 'Content-Type': 'application/json' }
  }).catch((e) => {
    console.log(e)
  });
  return await response.json();
}

// export const getSession = async () => {
//
//         const {tissue} = props.match.params
//         const {genes} = props.match.params
//         const response =
//             await fetch(`http://netbio.bgu.ac.il/trace-api/api/v1/genes/${genes}/tissue/${tissue}`, {
//                 headers: {'Content-Type': 'application/json'}
//             }).catch((e) => {
//                 console.log(e)
//             });
//         return await response.json();
//
// };


// export const getSessions = async () => {
//
//     const response =
//         await fetch(`https://example.com/session/load-sessions/${userName}`, {
//             headers: {'Content-Type': 'application/json'}
//         }).catch((e) => {
//             console.log(e)
//         });
//
//     return await response.json();
// }
