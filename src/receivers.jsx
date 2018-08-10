import React, { Component } from 'react';
import './App.css';
import cupcakeLogo from './cupcake.jpg'
import Employee from './employee.jsx';

class Receivers extends Component {
  render() {
    return (
        <div>
        <h2>Receivers</h2>
        <div className="container">
            <div className="row">
                <div className="col-sm-3">
                    <Employee name={'dcramer-pet'} cupcakes={9}/>
                </div>
                <div className="col-sm-3">
                    <Employee name={'lindseyschwarze-pet'}  cupcakes={9}/>
                </div>

            </div>
        </div>
        </div>
    );
  }
}

export default Receivers;
