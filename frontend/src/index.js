import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// index.js is the ENTRY POINT of the React application.
// Think of it as the "main()" function for the frontend.
//
// ReactDOM.createRoot() targets the <div id="root"> element in public/index.html.
// It then mounts (renders) our entire App component tree inside that div.
// Everything the user sees in the browser flows from this single render call.

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  // React.StrictMode is a development helper.
  // It runs extra checks and warnings to help you write better code.
  // It has NO effect in production builds.
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
