import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  BookOpen,
  Brain,
  Globe,
  Languages,
  Lightbulb,
  MessageCircle,
} from "lucide-react";

export default function Homepage() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-4 lg:px-6 h-14 flex items-center">
        <Link className="flex items-center justify-center" href="#">
          <BookOpen className="h-6 w-6 text-orange-500" />
          <span className="ml-2 text-2xl font-bold text-gray-900">
            LokaBhasha
          </span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="#"
          >
            Features
          </Link>
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="#"
          >
            Pricing
          </Link>
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="#"
          >
            About
          </Link>
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="#"
          >
            Contact
          </Link>
        </nav>
      </header>
      <main className="flex-1">
        <section className="w-full py-6 sm:py-12 md:py-24 lg:py-32 xl:py-48 bg-orange-50">
          <div className="px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none text-orange-700">
                    Master Indian Languages with AI
                  </h1>
                  <p className="max-w-[600px] text-gray-700 md:text-xl">
                    Learn Hindi, Tamil, Bengali, and more with our cutting-edge
                    AI-powered platform. Immerse yourself in Indian culture
                    through language.
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <Link href="/login">
                    <Button className="bg-orange-600 text-white hover:bg-orange-700">
                      Get Started
                    </Button>
                  </Link>
                  <Link href="#features">
                    <Button variant="outline">Learn More</Button>
                  </Link>
                </div>
              </div>
              <div className="flex items-center justify-center">
                <div className="relative w-[300px] h-[300px] sm:w-[400px] sm:h-[400px]">
                  <Globe className="absolute top-0 left-0 w-full h-full text-orange-300" />
                  <Languages className="absolute top-1/4 left-1/4 w-1/2 h-1/2 text-orange-500" />
                </div>
              </div>
            </div>
          </div>
        </section>
        <section
          id="features"
          className="w-full py-12 md:py-24 lg:py-32 bg-white"
        >
          <div className="px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-center mb-12 text-orange-700">
              Why Choose LokaBhasha?
            </h2>
            <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
              <div className="flex flex-col items-center text-center">
                <Brain className="h-12 w-12 text-orange-500 mb-4" />
                <h3 className="text-xl font-bold mb-2">AI-Powered Learning</h3>
                <p className="text-gray-700">
                  Personalized lessons adapted to your learning style and pace.
                </p>
              </div>
              <div className="flex flex-col items-center text-center">
                <MessageCircle className="h-12 w-12 text-orange-500 mb-4" />
                <h3 className="text-xl font-bold mb-2">
                  Interactive Conversations
                </h3>
                <p className="text-gray-700">
                  Practice speaking with our advanced language models.
                </p>
              </div>
              <div className="flex flex-col items-center text-center">
                <Lightbulb className="h-12 w-12 text-orange-500 mb-4" />
                <h3 className="text-xl font-bold mb-2">Cultural Insights</h3>
                <p className="text-gray-700">
                  Gain deep understanding of Indian culture through language.
                </p>
              </div>
            </div>
          </div>
        </section>
        <section className="w-full py-12 md:py-24 lg:py-32 bg-orange-50">
          <div className="px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-orange-700">
                  Start Your Language Journey Today
                </h2>
                <p className="max-w-[900px] text-gray-700 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Join thousands of learners mastering Indian languages with
                  LokaBhasha. Sign up now and get your first lesson free!
                </p>
              </div>
              <div className="w-full max-w-sm space-y-2">
                <form className="flex space-x-2">
                  <Input
                    className="max-w-lg flex-1"
                    placeholder="Enter your email"
                    type="email"
                  />
                  <Button
                    className="bg-orange-600 text-white hover:bg-orange-700"
                    type="submit"
                  >
                    Sign Up
                  </Button>
                </form>
                <p className="text-xs text-gray-500">
                  By signing up, you agree to our{" "}
                  <Link
                    className="underline underline-offset-2 hover:text-orange-600"
                    href="#"
                  >
                    Terms & Conditions
                  </Link>
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t">
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
    </div>
  );
}
