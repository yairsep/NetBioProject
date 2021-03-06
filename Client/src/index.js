import React from 'react';
import { render } from 'react-dom';
import { HashRouter, Route, Switch } from 'react-router-dom'
import App from './App';
import Home from './components/content/home'
import outputContainer from './components/results/outputContainer'
import historyContainer from './components/results/historyContainer'
// import '../semantic/dist/semantic.min.css'

render((
  <HashRouter hashType="noslash">
    <App>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/home" component={Home} />
        {/*<Route path="/login" component={ Login }/>*/}
        <Route path="/OutputExample" component={outputContainer} />
        <Route path="/findResult" component={historyContainer} />
        <Route path="/results" component={outputContainer} />
      </Switch>
    </App>
  </HashRouter>
), document.getElementById('root'))
