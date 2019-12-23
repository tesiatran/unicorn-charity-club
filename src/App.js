import React from "react";
import "./App.css";
import { Component } from "react";
import Sidebar from "./components/SideBar-Profile/SideBarProfile";
import Header from "./components/Header/Header";
import Navbar from "./components/Navbar/Navbar";
import Projects from "./components/Projects/Projects";
import Spotlight from "./components/Spotlight/Spotlight";
import Homepage from "./components/Homepage/Homepage";
import Friends from "./components/Friends/Friends";
import Yearbook from "./components/Yearbook/Yearbook";
import Footer from "./components/Footer/Footer";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Menu from "./components/Menu/Menu";
import Mobile_logo from "./image/Logo-mobile.png";
import Desktop_logo from "./image/desktop_logo.png";
import Mobile_toolbar from "./components/Mobile_toolbar/Mobile_toolbar";
import Login from "./components/Login/Login";
import ChildForm from "./components/MyChildren/ChildForm";
import Register from "./components/Register/Register";
import firebaseapi from "./config/firebaseapi";
import Account from "./components/Account/Account";
//import UnicornHeart from "../src/site_media/Bottom Menu_Home_Unicorn Heart.png"
//import Toolbar from './components/Toolbar/Toolbar';
//import sideDrawer from './components/SideDrawer/SideDrawer';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: {}
    };
  }
  componentDidMount() {
    this.authlistener();
  }
  authlistener() {
    firebaseapi.auth().onAuthStateChanged(user => {
      // console.log(user);
      if (user) {
        this.setState({ user });
        //  localStorage.setItem('user', user.uid);
      } else {
        this.setState({ user: null });
        //   localStorage.removeItem('user');
      }
    });
  }

  render() {
    return (
      <Router>
        {this.state.user ? (
          <div className="App">
            <div className="content-wrapper">
              <Header />
              <Navbar />

              <div className="container">
                <Switch>
                  <Route path="/" exact component={Homepage} />
                  <Route path="/Projects" component={Projects} />
                  <Route path="/Spotlight" component={Spotlight} />
                  <Route path="/Friends" component={Friends} />
                  <Route path="/Yearbook" component={Yearbook} />
                  <Route path="/Account" component={Account} />
                </Switch>
                <Sidebar />
              </div>
            </div>
            <Footer />{" "}
          </div>
        ) : (
          <div className="App">
            <Login />{" "}
          </div>
        )}
      </Router>
    );
  }
}

export default App;
