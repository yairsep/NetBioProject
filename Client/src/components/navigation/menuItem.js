import React from 'react';
import { NavLink } from 'react-router-dom';

const MenuItem = (props) => {
  const { item } = props;

  return item.href ? (
  //Link Out of the page
    <a href={item.href} rel="external" title={item.title} className="ui item link">{item.name}</a>
  )
  //ChangeContent
    : (
      <NavLink to={{ pathname: `/${item.link}`, state: 'sample' }} activeClassName="active" className="ui item link">
        {item.name}
      </NavLink>
    );
};

export default MenuItem;
