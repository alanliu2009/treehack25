import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from "react";


function App() {
  // usestate for setting a javascript
  // object for storing and using data
  // const [data, setdata] = useState({
  //   name: "",
  //   age: 0,
  //   date: "",
  //   programming: "",
  // });
  const [test, settest] = useState({
    text: ""
  })

  // Using useEffect for single rendering
  useEffect(() => {
      // Using fetch to fetch the api from 
      // flask server it will be redirected to proxy
      fetch("/hello").then((res)=> {
        console.log(res);
      });
      // fetch("/hello").then((res) =>
      //     res.json().then((data) => {
      //         // Setting a data from api
      //         setdata({
      //             text: data.text
      //         });
      //     })
      // );
  }, []);

  return (
      <div className="App">
          <header className="App-header">
              <h1>React and flask</h1>
              {/* Calling a data from setdata for showing */}
              {/* <p>{data.name}</p> */}

          </header>
      </div>
  );
}
export default App;
