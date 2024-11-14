"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import { Spinner } from "@/components/spinner";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BookOpen, Users, BookOpenCheck, Brain, BarChart } from "lucide-react";

interface AdminAnalytics {
  daily_responses: number;
  most_active_language: string;
  active_language_responses: number;
  today_signups: number;
  overall_avg_latency: number;
}

export default function AdminDashboard() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [analytics, setAnalytics] = useState<AdminAnalytics | null>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      const userData = JSON.parse(storedUser);
      if (userData.email === "admin@admin.com") {
        setUser(userData);
        fetchAnalytics();
      } else {
        router.push("/login");
      }
    } else {
      router.push("/login");
    }
    setIsLoading(false);
  }, [router]);

  const fetchAnalytics = async () => {
    try {
      const response = await fetch("http://localhost:8000/admin-analytics");
      const data = await response.json();
      setAnalytics(data);
    } catch (error) {
      console.error("Failed to fetch analytics:", error);
    }
  };

  if (isLoading || !analytics) {
    return <Spinner />;
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-white shadow-sm">
        <Link
          className="flex items-center justify-center"
          href="/admin/dashboard"
        >
          <BookOpen className="h-6 w-6 text-orange-500" />
          <span className="ml-2 text-2xl font-bold text-gray-900">
            LokaBhasha Admin
          </span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="#"
          >
            Modules
          </Link>
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="#"
          >
            Resources
          </Link>
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="#"
          >
            Analytics
          </Link>
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="#"
          >
            Settings
          </Link>
        </nav>
      </header>
      <main className="flex-1 p-4 md:p-6 space-y-6">
        <h1 className="text-2xl font-bold text-gray-900">Welcome Admin! Here are the platform's usage stats</h1>
        <div className="grid gap-8 md:grid-cols-1 lg:grid-cols-2 p-2">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                New Users Today
              </CardTitle>
              <Users className="h-8 w-8 text-orange-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {analytics.today_signups}
              </div>
              <p className="text-xs text-muted-foreground">New signups today</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Daily Responses
              </CardTitle>
              <BookOpenCheck className="h-8 w-8 text-orange-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {analytics.daily_responses}
              </div>
              <p className="text-xs text-muted-foreground">Responses today</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Most Active Language
              </CardTitle>
              <Brain className="h-8 w-8 text-orange-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {analytics.most_active_language}
              </div>
              <p className="text-xs text-muted-foreground">
                {analytics.active_language_responses} responses
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Avg Response Time
              </CardTitle>
              <BarChart className="h-8 w-8 text-orange-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {analytics.overall_avg_latency.toFixed(2)}ms
              </div>
              <p className="text-xs text-muted-foreground">Overall average</p>
            </CardContent>
          </Card>
        </div>
      </main>
      <footer className="py-6 text-center text-sm text-gray-500">
        © 2024 LokaBhasha. All rights reserved.
      </footer>
    </div>
  );
}
