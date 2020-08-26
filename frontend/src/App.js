import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom'
import { Route, Link } from 'react-router-dom'
import watchlistList from './wactlistList'

import logo from './logo.svg';
import './App.css';

const  BaseLayout  = () => (
<div  className="container-fluid">
    <nav  className="navbar navbar-expand-lg navbar-light bg-light">
        <a  className="navbar-brand"  href="#">Watchlists</a>
        <button  className="navbar-toggler"  type="button"  data-toggle="collapse"  data-target="#navbarNavAltMarkup"  aria-controls="navbarNavAltMarkup"  aria-expanded="false"  aria-label="Toggle navigation">
        <span  className="navbar-toggler-icon"></span>
    </button>
    <div  className="collapse navbar-collapse"  id="navbarNavAltMarkup">
        <div  className="navbar-nav">
            <a  className="nav-item nav-link"  href="/">My Account</a>
            <a  className="nav-item nav-link"  href="/">Create a Watchlist</a>
        </div>
    </div>
    </nav>
    <div  className="content">
        <Route  path="/"  exact  component={watchlistList}  />
        {/* <Route  path="/watchlist/:pk"  component={WatchlistCreateUpdate}  />
        <Route  path="/watchlist/"  exact  component={WatchlistCreateUpdate}  /> */}
    </div>
</div>
)

class  App  extends  Component {
  render() {
      return (
      <BrowserRouter>
          <BaseLayout/>
      </BrowserRouter>
      );
  }
}


export default App;
