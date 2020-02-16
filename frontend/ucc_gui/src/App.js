import React, { Component } from "react";

import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import baseReducer from "./reducers/reducer"
import { Provider } from 'react-redux';
import { createStore } from 'redux';
import UCC_App from "./containers/UCC_App";
const store = createStore(baseReducer);

class App extends Component {
  render() {
    return (
        <Provider store={store}>
            <UCC_App/>
        </Provider>
    );
  }
}

export default App;