import React from 'react';
import { render } from 'react-dom';
import { HashRouter, Route, Switch } from 'react-router-dom'
import App from './App';
import Home from './components/content/home'
import FAQ from "./Pages/FAQ";
import Tutorial from "./Pages/Tutorial";
import outputExamples from "./Pages/outputExamples";

// import '../semantic/dist/semantic.min.css'

render((
  <HashRouter hashType="noslash">
    <App>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/home" component={Home} />
          <Route path="/FAQ" component={FAQ} />
          <Route path="/Tutorial" component={Tutorial} />
          <Route path="/OutputExamples" component={outputExamples} />
        {/*<Route path="/login" component={ Login }/>*/}
        {/*<Route path="/sample" component={ Results } />*/}
        {/*<Route path="/results" component={ Results }/>*/}
      </Switch>
    </App>
  </HashRouter>
), document.getElementById('root'))
