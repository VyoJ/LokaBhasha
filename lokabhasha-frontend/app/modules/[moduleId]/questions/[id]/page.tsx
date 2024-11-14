"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  BookOpen,
  Mic,
  Play,
  Square,
  ArrowLeft,
  ArrowRight,
} from "lucide-react";
import { Spinner } from "@/components/spinner";
import { useToast } from "@/hooks/use-toast";

// Add this type definition at the top of the file
type Question = {
  q_id: number;
  m_id: number;
  question: string;
  exp_ans: string;
  category: string;
};

// Add new type for response
type ResponseCreate = {
  response_asr: string;
  response_translate: string; 
  latency: number;
};

export default function QuestionPage() {
  const { id, moduleId } = useParams();
  const router = useRouter();
  const [question, setQuestion] = useState<Question | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [hasNext, setHasNext] = useState(true);
  const [hasPrevious, setHasPrevious] = useState(true);
  const [user, setUser] = useState<{ id: number } | null>(null);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(
    null
  );
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
  const [transcribedText, setTranscribedText] = useState<string>("");
  const audioRef = useRef<HTMLAudioElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      const userData = JSON.parse(storedUser);
      if (userData.isLoggedIn && userData.id) {
        setUser(userData);
      } else {
        router.push("/login");
      }
    } else {
      router.push("/login");
    }
  }, [router]);

  const checkNextQuestion = async () => {
    if (!user) return;
    try {
      const response = await fetch(
        `http://localhost:8000/modules/${moduleId}/next-question/${user.id}`
      );
      setHasNext(response.ok);
    } catch (error) {
      setHasNext(false);
    }
  };

  const fetchQuestion = async (questionId: string) => {
    if (!user) return;
    try {
      const response = await fetch(
        `http://localhost:8000/questions/${questionId}`
      );
      if (!response.ok) {
        throw new Error("Question not found");
      }
      const data = await response.json();
      setQuestion(data);
      setIsLoading(false);

      await checkNextQuestion();

      fetch(`http://localhost:8000/questions/${parseInt(questionId) - 1}`)
        .then((res) => setHasPrevious(res.ok))
        .catch(() => setHasPrevious(false));
    } catch (error) {
      console.error("Error fetching question:", error);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      fetchQuestion(id as string);
    }
  }, [id, moduleId, user]);

  const handleNext = async () => {
    if (!user) return;
    try {
      const response = await fetch(
        `http://localhost:8000/modules/${moduleId}/next-question/${user.id}`
      );
      if (!response.ok) {
        throw new Error("No more questions");
      }
      const nextQuestion = await response.json();
      if (!nextQuestion || typeof nextQuestion.id === "undefined") {
        throw new Error("Invalid question ID received");
      }
      router.push(`/modules/${moduleId}/questions/${nextQuestion.id}`);
    } catch (error) {
      console.error("Error fetching next question:", error);
      setHasNext(false);
    }
  };

  const handlePrevious = () => {
    const previousId = parseInt(id as string) - 1;
    router.push(`/modules/${moduleId}/questions/${previousId}`);
  };

  const handlePlay = async () => {
    if (!question) return;
    setIsPlaying(true);
    try {
      const response = await fetch("http://localhost:8000/text-to-speech", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: question.exp_ans }),
      });

      if (!response.ok) {
        throw new Error(`Failed to convert text to speech: ${response.status}`);
      }

      const data = await response.json();
      console.log("Received audio data:", data.audio);

      if (!data.audio) {
        throw new Error("No audio data received");
      }

      const base64ToArrayBuffer = (base64: string): ArrayBuffer => {
        const binaryString = window.atob(base64);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
          bytes[i] = binaryString.charCodeAt(i);
        }
        return bytes.buffer;
      };

      const determineMimeType = (base64: string): string => {
        if (base64.startsWith("UklGR")) {
          return "audio/wav";
        }
        return "audio/mpeg";
      };

      const mimeType = determineMimeType(data.audio);
      console.log("Using MIME type:", mimeType);
      const arrayBuffer = base64ToArrayBuffer(data.audio);
      const audioBlob = new Blob([arrayBuffer], { type: mimeType });
      const audioUrl = URL.createObjectURL(audioBlob);

      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        audioRef.current.play().catch((err) => {
          console.error("Audio playback failed:", err);
          setIsPlaying(false);
        });
      }

      audioRef.current!.onended = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };
    } catch (error) {
      console.error("Error playing audio:", error);
      setIsPlaying(false);
    }
  };

  const sendAudioToBackend = async (audioBlob: Blob) => {
    if (!user || !question) return;
    
    const startTime = Date.now();
    const formData = new FormData();
    formData.append("audio", audioBlob);
  
    try {
      // Get transcription
      const transcribeResponse = await fetch("http://localhost:8000/speech-to-text", {
        method: "POST",
        body: formData,
      });
  
      if (!transcribeResponse.ok) {
        throw new Error("Failed to convert speech to text");
      }
  
      const transcribeData = await transcribeResponse.json();
      setTranscribedText(transcribeData.transcribed);
  
      // Compare answers
      const compareResponse = await fetch("http://localhost:8000/compare-answers", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          expected_answer: question.exp_ans,
          user_answer: transcribeData.transcribed
        })
      });
  
      if (!compareResponse.ok) {
        throw new Error("Failed to compare answers");
      }
  
      const compareData = await compareResponse.json();
      const latency = Date.now() - startTime;
  
      // Create response with conditional translation
      const responseData: ResponseCreate = {
        response_asr: transcribeData.transcribed,
        response_translate: compareData.is_similar ? question.exp_ans : "",
        latency: latency
      };
  
      const createResponse = await fetch(
        `http://localhost:8000/responses/?user_id=${user.id}&question_id=${question.q_id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(responseData)
        }
      );
  
      if (!createResponse.ok) {
        throw new Error("Failed to save response");
      }
  
    } catch (error) {
      console.error("Error processing audio:", error);
      toast({
        title: "Error",
        description: "Failed to process audio. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleRecord = async () => {
    if (isRecording) {
      mediaRecorderRef.current?.stop();
      setIsRecording(false);
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;
        const audioChunks: Blob[] = [];

        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          stream.getTracks().forEach((track) => track.stop());
          await sendAudioToBackend(audioBlob);
        };

        mediaRecorder.start();
        setIsRecording(true);
      } catch (error) {
        console.error("Error starting recording:", error);
        toast({
          title: "Error",
          description:
            "Failed to start recording. Please check your microphone permissions.",
          variant: "destructive",
        });
      }
    }
  };

  useEffect(() => {
    return () => {
      if (mediaRecorderRef.current && isRecording) {
        mediaRecorderRef.current.stop();
        setIsRecording(false);
      }
    };
  }, [isRecording]);

  if (isLoading || !user) {
    return <Spinner />;
  }

  return (
    <div className="flex flex-col min-h-screen bg-orange-50">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-white">
        <Link className="flex items-center justify-center" href="/">
          <BookOpen className="h-6 w-6 text-orange-500" />
          <span className="ml-2 text-2xl font-bold text-gray-900">
            LokaBhasha
          </span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link
            className="text-sm font-medium hover:text-orange-500 transition-colors"
            href="/dashboard"
          >
            <ArrowLeft className="h-4 w-4 inline-block mr-2" />
            Back to Dashboard
          </Link>
        </nav>
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
              <p className="text-xl text-gray-800 text-center">
                {question?.exp_ans}
              </p>
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
              <div className="flex justify-between mt-6">
                <Button
                  onClick={handlePrevious}
                  disabled={!hasPrevious}
                  className="bg-gray-600 hover:bg-gray-700 text-white"
                >
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Previous
                </Button>
                <Button
                  onClick={handleNext}
                  disabled={!hasNext}
                  className="bg-gray-600 hover:bg-gray-700 text-white"
                >
                  {hasNext ? (
                    <>
                      Next
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </>
                  ) : (
                    "Module Done!"
                  )}
                </Button>
              </div>
              {isRecording && (
                <div className="flex justify-center items-center space-x-2">
                  <div className="w-2 h-2 bg-red-600 rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-red-600 rounded-full animate-pulse delay-75"></div>
                  <div className="w-2 h-2 bg-red-600 rounded-full animate-pulse delay-150"></div>
                </div>
              )}
              {transcribedText && (
                <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-medium text-gray-900">Your Answer:</h3>
                  <p className="text-gray-700">{transcribedText}</p>
                </div>
              )}
              <audio
                ref={audioRef}
                onEnded={() => setIsPlaying(false)}
                onError={(e) => {
                  console.error("Audio playback error:", e);
                  setIsPlaying(false);
                }}
              />
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
