import React, { useEffect } from 'react';
import { Grid } from 'semantic-ui-react';
import { useHistory, withRouter } from 'react-router-dom';
import { fetchGene, fetchSample } from './fetchers';

const OutputContainer = (props) => {
  const { location } = props;
  const { pathname } = location;
  const history = useHistory();

  useEffect(() => {
    console.log(history.location.data);
    pathname.includes('results') ? fetchGene() : fetchSample();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <Grid.Column width={10} />
      <Grid.Column width={6} />
    </>
  );
};

export default withRouter(OutputContainer);
