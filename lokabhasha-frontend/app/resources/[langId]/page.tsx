"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  BookOpen,
  ArrowLeft,
  FileText,
  Video,
  Headphones,
  LinkIcon,
  Loader2,
} from "lucide-react";
import axios from "axios";

type ResourceInDB = {
  lang_id: number;
  resource_id: number;
  url: string;
  type: string;
  format: string;
};

const getResources = async (langId: number): Promise<ResourceInDB[]> => {
  try {
    const { data } = await axios.get(`http://localhost:8000/resources/`);
    return data.filter((resource: ResourceInDB) => resource.lang_id === langId);
  } catch (error) {
    throw new Error("Failed to fetch resources");
  }
};

const getLanguageName = (langId: number): string => {
  const languages: { [key: number]: string } = {
    1: "Hindi",
    2: "Kannada",
    3: "Tamil",
  };
  return languages[langId] || "Unknown Language";
};

const ResourceIcon = ({ type }: { type: string }) => {
  switch (type) {
    case "document":
      return <FileText className="h-6 w-6 text-blue-500" />;
    case "audio":
      return <Headphones className="h-6 w-6 text-green-500" />;
    case "video":
      return <Video className="h-6 w-6 text-red-500" />;
    default:
      return <LinkIcon className="h-6 w-6 text-purple-500" />;
  }
};

export default function LanguageResourcesPage() {
  const params = useParams();
  const langId = Number(params.langId);
  const [resources, setResources] = useState<ResourceInDB[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadResources = async () => {
      setIsLoading(true);
      try {
        const data = await getResources(langId);
        setResources(data);
        setError(null);
      } catch (err) {
        setError("Failed to load resources. Please try again later.");
        setResources([]);
      } finally {
        setIsLoading(false);
      }
    };

    if (langId) {
      loadResources();
    }
  }, [langId]);

  return (
    <div className="flex flex-col min-h-screen bg-orange-50">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-white border-b border-orange-100">
        <Link className="flex items-center justify-center" href="/dashboard">
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
      <main className="flex-1 p-6 md:p-10">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-orange-700 mb-6">
            {getLanguageName(langId)} Resources
          </h1>
          {isLoading ? (
            <div className="flex justify-center items-center h-64">
              <Loader2 className="h-8 w-8 animate-spin text-orange-500" />
            </div>
          ) : error ? (
            <div className="text-center text-red-500">{error}</div>
          ) : (
            <div className="grid gap-6 md:grid-cols-2">
              {resources.map((resource) => (
                <Card
                  key={resource.resource_id}
                  className="hover:shadow-lg transition-shadow"
                >
                  <CardHeader className="flex flex-row items-center gap-4">
                    <ResourceIcon type={resource.type} />
                    <div>
                      <CardTitle className="text-lg">
                        {resource.type.charAt(0).toUpperCase() +
                          resource.type.slice(1)}
                      </CardTitle>
                      <CardDescription>
                        {resource.format.toUpperCase()}
                      </CardDescription>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <Button
                      asChild
                      className="w-full bg-orange-500 hover:bg-orange-600"
                    >
                      <Link
                        href={resource.url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        Open Resource
                      </Link>
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
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
    </div>
  );
}
