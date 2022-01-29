import React from 'react';
import './App.css';

import Nav from './secure/components/Nav';
import Menu from './secure/components/Menu';
import Dashboard from './secure/Dashboard';
import Users from './secure/Users';

import {BrowserRouter, Routes, Route} from 'react-router-dom';


function App() {
  return (
    <div className="App">

      <Nav />

      <div className="container-fluid">
        <div className="row">

          <Menu />

          <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4">

            <BrowserRouter>
              <Routes>
                <Route path={'/'} element={<Dashboard />} />
                <Route path={'/users'} element={<Users />} />
              </Routes>
            </BrowserRouter>

          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
