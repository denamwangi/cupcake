import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import './index.css';
import App from './App';
import DetailedCupcake from './detailedCupcake.jsx';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(

    <Router>
        <div className="App">
            <div>
                <Route exact path="/" component={App}/>
                <Route exact path="/eric" component={DetailedCupcake}/>
            </div>
        </div>
    </Router>
,
     document.getElementById('root'));
registerServiceWorker();
