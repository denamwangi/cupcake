import React, { Component } from 'react';
import './App.css';
import Givers from './givers.jsx';
import Receivers from './receivers.jsx';
import cupcakeLogo from './cupcake.jpg';
import Employee from './employee.jsx';

class DetailedCupcake extends Component {
  render() {
    return (
      <div>
        <div>
          <img src={cupcakeLogo} alt="cupcake" height="128" width="128"/>
        </div>
        <h1>Cupcake Leaderboard</h1>

        <div className="container detailed-container">
          <div className="row">
            <div className="col-sm-3 detailed-employee">
                <ul>
                    <li> for adjkdfksjhfs </li>
                    <li> for adjkdfksjhfs </li>
                    <li> for adjkdfksjhfs </li>
                </ul>
            </div>
            
            <div className="col-sm-6 detailed-employee">
                <Employee name={'ehfeng'} cupcakes={6}/>
            </div>
            <div className="col-sm-3 detailed-employee">
                <ul>
                    <li> for adjkdfksjhfs </li>
                    <li> for adjkdfksjhfs </li>
                    <li> for adjkdfksjhfs </li>
                </ul>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default DetailedCupcake;
