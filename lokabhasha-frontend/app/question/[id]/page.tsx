"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { BookOpen, Mic, Play, Square } from "lucide-react";

export default function QuestionPage() {
  const { id } = useParams();
  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isRecording, setIsRecording] = useState(false);

  useEffect(() => {
    const fetchQuestion = async () => {
      try {
        const response = await fetch(`/api/question/${id}`);
        const data = await response.json();
        setQuestion(data.question);
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching question:", error);
        setIsLoading(false);
      }
    };

    fetchQuestion();
  }, [id]);

  const handlePlay = () => {
    setIsPlaying(true);
    const utterance = new SpeechSynthesisUtterance(question);
    utterance.onend = () => setIsPlaying(false);
    speechSynthesis.speak(utterance);
  };

  const handleRecord = () => {
    if (isRecording) {
      setIsRecording(false);
      // Stop recording logic here
    } else {
      setIsRecording(true);
      // Start recording logic here
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-orange-50">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-white">
        <Link className="flex items-center justify-center" href="/">
          <BookOpen className="h-6 w-6 text-orange-500" />
          <span className="ml-2 text-2xl font-bold text-gray-900">
            LokaBhasha
          </span>
        </Link>
      </header>
      <main className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="max-w-3xl w-full space-y-8">
          <h1 className="text-3xl font-bold tracking-tighter text-center text-orange-700">
            Practice Your Speaking
          </h1>
          {isLoading ? (
            <p className="text-center text-gray-700">Loading question...</p>
          ) : (
            <div className="bg-white p-8 rounded-lg shadow-lg space-y-6">
              <p className="text-xl text-gray-800 text-center">{question}</p>
              <div className="flex justify-center space-x-4">
                <Button
                  onClick={handlePlay}
                  disabled={isPlaying}
                  className="bg-orange-600 hover:bg-orange-700 text-white"
                >
                  {isPlaying ? (
                    <Square className="mr-2 h-4 w-4" />
                  ) : (
                    <Play className="mr-2 h-4 w-4" />
                  )}
                  {isPlaying ? "Playing" : "Listen"}
                </Button>
                <Button
                  onClick={handleRecord}
                  className={`${
                    isRecording
                      ? "bg-red-600 hover:bg-red-700"
                      : "bg-orange-600 hover:bg-orange-700"
                  } text-white`}
                >
                  <Mic className="mr-2 h-4 w-4" />
                  {isRecording ? "Stop" : "Record"}
                </Button>
              </div>
              {isRecording && (
                <div className="flex justify-center items-center space-x-2">
                  <div className="w-2 h-2 bg-red-600 rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-red-600 rounded-full animate-pulse delay-75"></div>
                  <div className="w-2 h-2 bg-red-600 rounded-full animate-pulse delay-150"></div>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
      <footer className="py-6 w-full shrink-0 items-center px-4 md:px-6 border-t bg-white">
        <p className="text-xs text-center text-gray-500">
          © 2024 LokaBhasha. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
