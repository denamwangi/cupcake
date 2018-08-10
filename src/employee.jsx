import React, { Component } from 'react';
import './App.css';
import cupcakeLogo from './cupcake.jpg'

class Employee extends Component {
  render() {
    let {cupcakes, name} = this.props;
    let pic = 'https://github.com/getsentry/sentry.io/raw/master/src/_assets/img/people/'+name+'.jpg'

    return (
        <div>
            <div className="person-avatar">
                <img src={pic} className="rounded-circle img-fluid" alt='dena'/>
                <span>
                    <p className="cupcake-count">{cupcakes}</p>
                    <img src={cupcakeLogo} alt="cupcake" height="64" width="64"/>
                </span>
            </div>
        </div>
    );
  }
}

export default Employee;
