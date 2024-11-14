"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import axios from "axios";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Spinner } from "@/components/spinner";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  BookOpen,
  Brain,
  ChevronDown,
  Globe,
  MessageCircle,
  User,
  BarChart2,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const LANGUAGE_CODES: { [key: number]: string } = {
  1: "Hindi",
  2: "Kannada",
  3: "Tamil",
};

const getLanguageName = (langId: number | null): string => {
  if (!langId) return "Not Selected";
  return LANGUAGE_CODES[langId] || `Language ${langId}`;
};

interface ModuleProgress {
  module_id: number;
  lang_id: number;
  language_name: string;
  module_name: string;
  total_questions: number;
  answered_questions: number;
  module_status: string;
  completion_percentage: number;
}

interface OverallProgress {
  total_questions: number;
  completed_questions: number;
  overall_completion_percentage: number;
}

interface UserProgress {
  module_progress: ModuleProgress[];
  overall_progress: OverallProgress;
}

interface User {
  u_id: number;
  email: string;
  name: string;
  lang: number;
}

interface UserAnalytics {
  total_responses: number;
  correct_responses: number;
  wrong_responses: number;
}

export default function UserDashboard() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedModule, setSelectedModule] = useState<ModuleProgress | null>(
    null
  );
  const [analytics, setAnalytics] = useState<UserAnalytics | null>(null);
  const [progress, setProgress] = useState<UserProgress | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      const userData = JSON.parse(storedUser);
      if (userData.isLoggedIn && userData.id) {
        setUser({
          u_id: userData.id,
          email: userData.email,
          name: userData.name,
          lang: userData.lang,
        });
        fetchUserData(userData.id);
      } else {
        router.push("/login");
      }
    } else {
      router.push("/login");
    }
  }, [router]);

  const fetchUserData = async (userId: number) => {
    try {
      setIsLoading(true);
      const [analyticsRes, progressRes] = await Promise.all([
        axios.get(`http://localhost:8000/user-analytics/${userId}`),
        axios.get(`http://localhost:8000/user-progress/${userId}`),
      ]);
      setAnalytics(analyticsRes.data);
      setProgress(progressRes.data);
    } catch (error) {
      console.error("Failed to fetch user data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    router.push("/login");
  };

  const handleStartLesson = async (moduleId: number) => {
    if (!user) return;

    try {
      const response = await axios.get(
        `http://localhost:8000/modules/${moduleId}/next-question/${user.u_id}`
      );
      const nextQuestion = response.data;
      router.push(`/modules/${moduleId}/questions/${nextQuestion.q_id}`);
    } catch (error) {
      console.error("Failed to fetch next question:", error);
      toast({
        title: "Uh oh! Something went wrong.",
        description: "Try again later.",
      });
    }
  };

  const filteredModules =
    progress?.module_progress.filter(
      (module) => user && module.lang_id === user.lang
    ) || [];

  if (isLoading || !user) {
    return <Spinner />;
  }

  return (
    <div className="flex flex-col min-h-screen bg-orange-50">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-white border-b border-orange-100">
        <Link className="flex items-center justify-center" href="#">
          <BookOpen className="h-6 w-6 text-orange-500" />
          <span className="ml-2 text-2xl font-bold text-gray-900">
            LokaBhasha
          </span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6 items-center">
          <DropdownMenu>
            <Link href={`/resources/${user.lang}`}>Resources</Link>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="flex items-center gap-2">
                <User className="h-4 w-4" />
                <span>Profile</span>
                <ChevronDown className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <Link href={`/account/${user.u_id}`}>
                <DropdownMenuLabel>My Account</DropdownMenuLabel>
              </Link>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={handleLogout}>Logout</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </nav>
      </header>
      <main className="flex-1 p-6 md:p-10 space-y-8">
        <section>
          <h1 className="text-3xl font-bold text-orange-700 mb-4">
            Welcome back, {user.name}!
          </h1>
          <p className="text-gray-700">
            Continue your journey in mastering {getLanguageName(user.lang)}.
          </p>
        </section>
        <section id="modules" className="space-y-6">
          <h2 className="text-2xl font-semibold text-orange-600">
            Your Learning Modules
          </h2>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredModules.map((module) => (
              <Card
                key={`${module.lang_id}-${module.module_name}`}
                className="hover:shadow-lg transition-shadow"
              >
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-lg font-medium">
                    {module.module_name.toUpperCase()}
                  </CardTitle>
                  <Globe className="h-5 w-5 text-orange-500" />
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <Progress
                      value={module.completion_percentage}
                      className="w-full"
                    />
                    <p className="text-sm text-gray-500">
                      {module.completion_percentage}% Complete
                    </p>
                    <p className="text-xs text-gray-400">
                      {module.answered_questions} of {module.total_questions}{" "}
                      questions completed
                    </p>
                    <Button
                      className="w-full bg-orange-500 hover:bg-orange-600"
                      onClick={() => setSelectedModule(module)}
                    >
                      {module.module_status === "Not Started"
                        ? "Start Learning"
                        : "Continue Learning"}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        <section id="analytics" className="space-y-6">
          <h2 className="text-2xl font-semibold text-orange-600">
            Your Progress Analytics
          </h2>
          <Card>
            <CardHeader>
              <CardTitle>Learning Overview</CardTitle>
              <CardDescription>
                Your language learning journey at a glance
              </CardDescription>
            </CardHeader>
            <CardContent className="flex justify-around py-6">
              <div className="text-center">
                <BarChart2 className="h-10 w-10 text-orange-500 mx-auto mb-2" />
                <p className="text-2xl font-bold text-gray-900">
                  {analytics?.total_responses || 0}
                </p>
                <p className="text-sm text-gray-500">Total Responses</p>
              </div>
              <div className="text-center">
                <Brain className="h-10 w-10 text-orange-500 mx-auto mb-2" />
                <p className="text-2xl font-bold text-gray-900">
                  {analytics?.correct_responses || 0}
                </p>
                <p className="text-sm text-gray-500">Correct Answers</p>
              </div>
              <div className="text-center">
                <MessageCircle className="h-10 w-10 text-orange-500 mx-auto mb-2" />
                <p className="text-2xl font-bold text-gray-900">
                  {analytics?.wrong_responses || 0}
                </p>
                <p className="text-sm text-gray-500">Need Improvement</p>
              </div>
            </CardContent>
          </Card>
        </section>
      </main>
      <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t bg-white">
        <p className="text-xs text-gray-500">
          © 2024 LokaBhasha. All rights reserved.
        </p>
        <nav className="sm:ml-auto flex gap-4 sm:gap-6">
          <Link className="text-xs hover:underline underline-offset-4" href="#">
            Terms of Service
          </Link>
          <Link className="text-xs hover:underline underline-offset-4" href="#">
            Privacy
          </Link>
        </nav>
      </footer>
      {selectedModule && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>{selectedModule.module_name}</CardTitle>
              <CardDescription>
                Ready to continue your learning?
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <p>
                You're {selectedModule.completion_percentage}% through this
                module. Keep up the great work!
              </p>
              <div className="flex justify-end space-x-2">
                <Button
                  variant="outline"
                  onClick={() => setSelectedModule(null)}
                >
                  Close
                </Button>
                <Button
                  className="bg-orange-500 hover:bg-orange-600"
                  onClick={() => handleStartLesson(selectedModule.module_id)}
                >
                  Start Lesson
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
