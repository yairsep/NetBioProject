import React, { useState, useEffect } from 'react';
import { Dropdown, Input, Button, Icon } from 'semantic-ui-react';
import { withRouter } from 'react-router-dom';
import tissues from '../common/tissues';


const Home = (props) => {
  const [selectedTissue, setTissue] = useState('heart');
  const [submissionPerm, setSubmissionPerm] = useState(false)
  const [userName, setUserName] = useState('')

  useEffect(() => {
    setSubmissionPerm(userName.length > 0)
  });

  const onTissueSelect = (e, { value }) => setTissue(value);

  return (

    <div className="ui ui raised padded container segment">
      <form className="ui form" id="homeForm">

        <div className="ui dividing header">
          <h1>Welcome to the Boilerplate</h1>
          <p>Here we are making some good stuff</p>
        </div>

        <div className="ui grid">
          <div className="row">
            <div className="six wide column">
              <label htmlFor="organism">Select Tissue:</label>

            </div>
            <div className="eight wide column">
              <Dropdown
                name="tissue"
                options={tissues}
                onChange={(e, { value }) => setTissue(value)}
                placeholder="Choose an organism"
                fluid
                selection
                defaultSearchQuery="heart"
                defaultValue="heart"
              />
            </div>
          </div>

          <div className="row">
            <div className="six wide column">
              <label htmlFor="organism">Enter your name:</label>

            </div>
            <div className="eight wide column">
              <Input
                onChange={(e, { value }) => setUserName(value)}
                placeholder="Your name..."
                fluid
              />
            </div>
          </div>


          <div className="row">
            <Button
              color="blue"
              icon
              labelPosition="right"
              style={{ margin: 'auto' }}
              disabled={!submissionPerm}
              // onClick={onSubmit}
            >
              Submit new job
              <Icon name="check circle" />
            </Button>
          </div>

        </div>
      </form>
    </div>
  )
};

export default withRouter(Home);
