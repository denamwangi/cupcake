import React, { Component } from 'react';
import './App.css';
import Givers from './givers.jsx';
import Receivers from './receivers.jsx';
import cupcakeLogo from './cupcake.jpg';


class App extends Component {
  render() {
    return (
      <div>
        <div>
          <img src={cupcakeLogo} alt="cupcake" height="128" width="128"/>
        </div>
        <h1>Cupcake Leaderboard</h1>
        <div className="container main-container">
          <div className="row">
            <div className="col-sm-6">
              <Givers/>
            </div>
            <div className="col-sm-6">
              <Receivers/>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
