"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { BookOpen } from "lucide-react";
import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { useToast } from "@/hooks/use-toast";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [language, setLanguage] = useState<number>(0);
  const router = useRouter();
  const { toast } = useToast();

  async function signup(
    email: string,
    password: string,
    username: string,
    language: number
  ) {
    const response = await axios.post("http://localhost:8000/auth/signup", {
      email,
      password,
      username,
      language,
    });

    if (response.data) {
      localStorage.setItem(
        "user",
        JSON.stringify({
          email,
          username,
          language,
          isLoggedIn: true,
        })
      );
      router.push("/dashboard");
    }

    return response.data;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await signup(email, password, username, language);
      toast({
        title: "Account created successfully!",
        description: "Welcome to LokaBhasha!",
      });
    } catch (error: any) {
      console.error("Signup failed:", error);
      toast({
        title: "Uh oh! Something went wrong.",
        description:
          error.response?.status === 400
            ? "Email might already be registered or check your inputs."
            : "Please try again later.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-orange-50">
      <header className="px-4 lg:px-6 h-14 flex items-center">
        <Link className="flex items-center justify-center" href="/">
          <BookOpen className="h-6 w-6 text-orange-500" />
          <span className="ml-2 text-2xl font-bold text-gray-900">
            LokaBhasha
          </span>
        </Link>
      </header>
      <main className="flex-1 flex items-center justify-center">
        <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
          <h1 className="text-2xl font-bold text-center mb-6 text-orange-700">
            Welcome!
          </h1>
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <Input
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
                required
                type="text"
              />
            </div>
            <div className="space-y-2">
              <Input
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
                type="email"
              />
            </div>
            <div className="space-y-2">
              <Input
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
                type="password"
              />
            </div>
            <div className="space-y-2">
              <Select
                onValueChange={(value) => setLanguage(parseInt(value))}
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select your preferred language" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1">Hindi</SelectItem>
                  <SelectItem value="2">Kannada</SelectItem>
                  <SelectItem value="3">Tamil</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button
              className="w-full bg-orange-600 text-white hover:bg-orange-700"
              type="submit"
            >
              Sign Up
            </Button>
          </form>
          <div className="mt-6 text-center text-sm">
            Have an account already?{" "}
            <Link className="text-orange-600 hover:underline" href="/login">
              Log In
            </Link>
          </div>
        </div>
      </main>
      <footer className="py-6 text-center text-sm text-gray-500">
        © 2024 LokaBhasha. All rights reserved.
      </footer>
    </div>
  );
}
