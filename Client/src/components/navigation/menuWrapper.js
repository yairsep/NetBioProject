import React from 'react';
import MenuItem from './menuItem';
import InjectionText from '../common/injectionText'

const MenuWrapper = (props) => {
  const { items, injectionText } = props;
  // eslint-disable-next-line react/no-array-index-key
  const content = items.map((item, i) => <MenuItem key={i} item={item} />);

  return (
    <div className="ui vertical menu">
      <div className="header item">
        <h3 className="ui header">Patho Search</h3>
        {/*<InjectionText >*/}
        {/*{injectionText}*/}
        {/*</InjectionText>*/}
      </div>
      { content }
    </div>
  );
};

export default MenuWrapper;
