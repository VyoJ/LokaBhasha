import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { BookOpen } from "lucide-react";

export default function LoginPage() {
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
            Welcome Back
          </h1>
          <form className="space-y-4">
            <div className="space-y-2">
              <label
                className="text-sm font-medium text-gray-700"
                htmlFor="email"
              >
                Email
              </label>
              <Input
                id="email"
                placeholder="Enter your email"
                required
                type="email"
              />
            </div>
            <div className="space-y-2">
              <label
                className="text-sm font-medium text-gray-700"
                htmlFor="password"
              >
                Password
              </label>
              <Input id="password" required type="password" />
            </div>
            <Button
              className="w-full bg-orange-600 text-white hover:bg-orange-700"
              type="submit"
            >
              Sign In
            </Button>
          </form>
          <div className="mt-4 text-center text-sm">
            <Link className="text-orange-600 hover:underline" href="#">
              Forgot password?
            </Link>
          </div>
          <div className="mt-6 text-center text-sm">
            Don't have an account?{" "}
            <Link className="text-orange-600 hover:underline" href="#">
              Sign up
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
