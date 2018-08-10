import React, { Component } from 'react';
import './App.css';
import cupcakeLogo from './cupcake.jpg'
import Employee from './employee.jsx';

class Givers extends Component {
  render() {
    return (

        <div>
        <h2>Givers</h2>
        <div className="container">
            <div className="row">
                <div className="col-sm-3">
                    <Employee name={'daniel-pet'} cupcakes={8}/>
                </div>
                <div className="col-sm-3">
                    <Employee name={'colleenorourke-pet'} cupcakes={6}/>
                </div>

            </div>
        </div>
        </div>
    );
  }
}

export default Givers;
