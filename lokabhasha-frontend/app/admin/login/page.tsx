"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { BookOpen, ShieldAlert } from "lucide-react";
import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { useToast } from "@/hooks/use-toast";

export default function AdminLoginPage() {
  const router = useRouter();
  const { toast } = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  async function login(email: string, password: string) {
    const response = await axios.post("http://localhost:8000/auth/login", {
      email,
      password,
    });
    if (response.data) {
      localStorage.setItem(
        "user",
        JSON.stringify({
          email,
          isLoggedIn: true,
        })
      );
    }

    return response.data;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await login(formData.email, formData.password);
      toast({
        title: "Successfully logged in!",
        description: "Welcome back!",
      });
      router.push("/admin/dashboard");
    } catch (error: any) {
      console.error("Login failed:", error);
      if (error.response?.status === 400) {
        toast({
          title: "Uh oh! Something went wrong.",
          description: "Check your email, password or try again.",
        });
      } else {
        toast({
          variant: "destructive",
          title: "Error",
          description: "Something went wrong",
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.id]: e.target.value,
    }));
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-white shadow-sm">
        <Link className="flex items-center justify-center" href="/">
          <BookOpen className="h-6 w-6 text-orange-500" />
          <span className="ml-2 text-2xl font-bold text-gray-900">
            LokaBhasha
          </span>
        </Link>
      </header>
      <main className="flex-1 flex items-center justify-center">
        <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
          <div className="flex items-center justify-center mb-4">
            <ShieldAlert className="h-8 w-8 text-orange-500" />
          </div>
          <h1 className="text-2xl font-bold text-center mb-6 text-gray-900">
            Admin Login
          </h1>
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <label
                className="text-sm font-medium text-gray-700"
                htmlFor="email"
              >
                Email
              </label>
              <Input
                id="email"
                placeholder="Enter your admin email id"
                required
                type="email"
                value={formData.email}
                onChange={handleChange}
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <label
                className="text-sm font-medium text-gray-700"
                htmlFor="password"
              >
                Password
              </label>
              <Input
                id="password"
                required
                type="password"
                value={formData.password}
                onChange={handleChange}
                disabled={isLoading}
              />
            </div>
            <Button
              className="w-full bg-gray-900 text-white hover:bg-gray-800"
              type="submit"
              disabled={isLoading}
            >
              {isLoading ? "Signing in..." : "Sign In"}
            </Button>
          </form>
        </div>
      </main>
      <footer className="py-6 text-center text-sm text-gray-500">
        © 2024 LokaBhasha. All rights reserved.
      </footer>
    </div>
  );
}
