import React from 'react'
import HeaderButton from './headerButton';
import lab_header from '../../static/trace_lab_header.png'

const Header = ({ headerButtons }) => (
  <div className="header-image">
    <a href="#form-container" tabIndex="1" className="accessibility-aid skip-link" />
    <a href="http://netbio.bgu.ac.il" rel="external">
      <img
        src={lab_header}
        style={{ width: '100%' }}
        alt="The logo of the lab and the link to the main lab site"
      />
    </a>
    <div style={{ top: '0.4%', right: '0.5%', position: 'absolute' }}>
      {headerButtons.map((button, key) => <HeaderButton key={key} {...button} />)}
    </div>
  </div>
)

export default Header;
