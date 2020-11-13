import React from 'react';
import MenuItem from './menuItem';
import InjectionText from '../common/injectionText'

const MenuWrapper = (props) => {
  const { items, injectionText } = props;
  const content = items.map((item, i) => <MenuItem key={i} item={item} />);

  return (
    <div className="ui vertical menu">
      <div className="header item">
        <h3 className="ui header">Trace</h3>
        {/*<InjectionText >*/}
        {/*{injectionText}*/}
        {/*</InjectionText>*/}
      </div>
      { content }
    </div>
  );
};

export default MenuWrapper;
