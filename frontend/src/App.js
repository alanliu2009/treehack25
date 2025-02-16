// import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from "react";
// import SentimentAnalysis from './Sentiment';



// import { useState } from "react";
import { Progress } from "./components/progress.jsx";
import { Card, CardContent, CardHeader, CardTitle } from "./components/card.jsx";
// import { Progress } from "@/components/progress";
// import { Card, CardContent, CardHeader, CardTitle } from "@/components/card";
import { Frown, Smile, Meh } from "lucide-react";

function App() {
  const [sentiment, setSentiment] = useState(15); // Example sentiment value
  // IFFFF LOADING, should try and get a diff UI going up here
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  console.log("IN FUNC test");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/process_video");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const result = await response.text();
        console.log("testing new response")
        console.log(result.text());
        const intResult = parseInt(result);
        setSentiment(intResult); // Update the state with Flask API response
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []); // Empty dependency array ensures it runs once when component mounts


  const getSentimentIcon = (value) => {
    if (value > 66) return <Smile className="text-green-500 w-8 h-8" />;
    if (value > 33) return <Meh className="text-yellow-500 w-8 h-8" />;
    return <Frown className="text-red-500 w-8 h-8" />;
  };

  const getSentimentColor = (value) => {
    if (value > 66) return "bg-green-500";
    if (value > 33) return "bg-yellow-500";
    return "bg-red-500";
  };

  return (
    <div className="App flex justify-center items-center min-h-screen bg-gray-100 p-4">

      <Card className="card w-full max-w-md shadow-lg rounded-2xl p-6 bg-white">
        <CardHeader className="cardheader flex items-center gap-3">
          <CardTitle className="title">here's how your meeting went :)</CardTitle>
        </CardHeader>
        <CardContent className="cardcontent flex flex-col items-center gap-4">
          {getSentimentIcon(sentiment)}
          <div className={`sentiment w-full h-4 rounded-lg ${getSentimentColor(sentiment)}`}>
            {/* <Progress value={sentiment} className="h-4 rounded-lg" /> */}
            <progress value={sentiment}  max={100} barClassName="my-progress" />
          </div>
          <p className="sent-text text-lg font-semibold">Sentiment Score: {sentiment}%</p>
        </CardContent>
      </Card>
    </div>
  );
}


export default App;
