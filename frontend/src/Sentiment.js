import { useState } from "react";
import { Progress } from "@/components/ui/progress";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FaceFrown, FaceSmile, FaceMeh } from "lucide-react";

export default function SentimentAnalysis() {
  const [sentiment, setSentiment] = useState(75); // Example sentiment value

  const getSentimentIcon = (value) => {
    if (value > 66) return <FaceSmile className="text-green-500 w-8 h-8" />;
    if (value > 33) return <FaceMeh className="text-yellow-500 w-8 h-8" />;
    return <FaceFrown className="text-red-500 w-8 h-8" />;
  };

  const getSentimentColor = (value) => {
    if (value > 66) return "bg-green-500";
    if (value > 33) return "bg-yellow-500";
    return "bg-red-500";
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100 p-4">
      <Card className="w-full max-w-md shadow-lg rounded-2xl p-6 bg-white">
        <CardHeader className="flex items-center gap-3">
          <CardTitle>Zoom Call Sentiment Analysis</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col items-center gap-4">
          {getSentimentIcon(sentiment)}
          <div className={`w-full h-4 rounded-lg ${getSentimentColor(sentiment)}`}>
            <Progress value={sentiment} className="h-4 rounded-lg" />
          </div>
          <p className="text-lg font-semibold">Sentiment Score: {sentiment}%</p>
        </CardContent>
      </Card>
    </div>
  );
}

