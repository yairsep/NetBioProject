import React, { useState, useEffect } from 'react';

const useForm = (initialValue) => {
  const [fields, setFields] = useState({ jobName: '', jobDescription: '', jobEmail: '' })

  const onFieldChange = (e) => setFields({ ...fields, [e.target.name]: e.target.value })

  return [
    onFieldChange,
    fields
  ]
}

export default useForm;
