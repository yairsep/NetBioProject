import React from 'react';
import { render } from 'react-dom';
import { HashRouter, Route, Switch } from 'react-router-dom'
import App from './App';
import Home from './components/content/home'
import outputContainer from './components/results/outputContainer'
import Cadd from './components/Genomics/cadd';
import Trace from './components/Genomics/trace';
// import '../semantic/dist/semantic.min.css'

render((
  <HashRouter hashType="noslash">
    <App>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/home" component={Home} />
        {/*<Route path="/login" component={ Login }/>*/}
        <Route path="/cadd" component={Cadd} />
        <Route path="/trace" component={Trace} />
        <Route path="/OutputExample" component={outputContainer} />
        <Route path="/results" component={outputContainer} />
      </Switch>
    </App>
  </HashRouter>
), document.getElementById('root'))
