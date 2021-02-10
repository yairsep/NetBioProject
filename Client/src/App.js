import React, { useState, useEffect } from 'react';
import { withRouter } from 'react-router-dom'
import MenuWrapper from './components/navigation/menuWrapper'
import Footer from './components/common/footer'
import Header from './components/common/header'
import headerItems from './config/headerItems'
import MenuItems from './config/menuItems'

const App = (props) => {
  const [serverRunning, setServerStatus] = useState(0);

  useEffect(() => {
    setServerStatus(1)
  },
  []);

  const { children } = props;
  // eslint-disable-next-line react/destructuring-assignment
  console.log(props.location.pathname);
  return (serverRunning === 1) ? (
    <div>
    
      <Header headerButtons={headerItems} />
      {/*eslint-disable-next-line react/destructuring-assignment*/}
      {props.location.pathname.substring(0, 8) === '/results' || props.location.pathname === '/OutputExample' ? (
        <div>
          {children}
        </div>
      ) : (
        <div className="ui grid container">
          <div className="two wide left floated column">
            <MenuWrapper items={MenuItems} />
          </div>
          <div className="twelve wide right floated column">
            {children}
          </div>
        </div>
      )}
      <Footer />
    </div>
  ) : (
    <div>
      <Header headerButtons={headerItems} />

      <div className="ui grid">
        <div className="two wide left floated column">
          <MenuWrapper items={MenuItems} />
        </div>
        <div className="twelve wide right floated column">
          <div className="ui segment centered very padded">
            <p>
              Unfortunately, our servers are currently
              down.
              <br />
              If the problem persists please send us an email at:
              <a href="mailto:estiyl@bgu.ac.il">estiyl@bgu.ac.il</a>
            </p>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  )
}

export default withRouter(App);
