"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { BookOpen, Plus, Pencil, Trash2, Code } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Spinner } from "@/components/spinner";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface API {
  api_id: number;
  api_url: string;
  lang_id: number;
}

export default function AdminAPIs() {
  const router = useRouter();
  const [apis, setAPIs] = useState<API[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [currentAPI, setCurrentAPI] = useState<API | null>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      const userData = JSON.parse(storedUser);
      if (userData.email === "admin@admin.com") {
        fetchAPIs();
      } else {
        router.push("/admin/login");
      }
    } else {
      router.push("/admin/login");
    }
  }, [router]);

  const fetchAPIs = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:8000/apis/");
      const data = await response.json();
      setAPIs(data);
    } catch (error) {
      console.error("Failed to fetch APIs:", error);
    }
    setIsLoading(false);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const formData = new FormData(form);
    const apiData = {
      api_url: formData.get("api_url") as string,
      lang_id: parseInt(formData.get("lang_id") as string)
    };

    try {
      const url = currentAPI
        ? `http://localhost:8000/apis/${currentAPI.api_id}`
        : "http://localhost:8000/apis/";
      const method = currentAPI ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(apiData),
      });

      if (response.ok) {
        fetchAPIs();
        setIsDialogOpen(false);
        setCurrentAPI(null);
      } else {
        console.error("Failed to save API");
      }
    } catch (error) {
      console.error("Error saving API:", error);
    }
  };

  const handleDelete = async (api_id: number) => {
    if (window.confirm("Are you sure you want to delete this API?")) {
      try {
        const response = await fetch(`http://localhost:8000/apis/${api_id}`, {
          method: "DELETE",
        });

        if (response.ok) {
          fetchAPIs();
        } else {
          console.error("Failed to delete API");
        }
      } catch (error) {
        console.error("Error deleting API:", error);
      }
    }
  };

  if (isLoading) {
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
            href="/admin/modules"
          >
            Modules
          </Link>
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="/admin/resources"
          >
            Resources
          </Link>
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="/admin/apis"
          >
            APIs
          </Link>
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="/admin/analytics"
          >
            Analytics
          </Link>
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="/admin/settings"
          >
            Settings
          </Link>
        </nav>
      </header>
      <main className="flex-1 p-4 md:p-6 space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Manage APIs</h1>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={() => setCurrentAPI(null)}>
                <Plus className="mr-2 h-4 w-4" /> Add New API
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>
                  {currentAPI ? "Edit API" : "Add New API"}
                </DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="api_url">API URL</Label>
                  <Input
                    id="api_url"
                    name="api_url"
                    defaultValue={currentAPI?.api_url}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="lang_id">Language ID</Label>
                  <Input
                    id="lang_id"
                    name="lang_id"
                    type="number" 
                    defaultValue={currentAPI?.lang_id}
                    required
                  />
                </div>
                <Button type="submit">Save API</Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>
        <Card>
          <CardHeader>
            <CardTitle>APIs List</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>API ID</TableHead>
                  <TableHead>API URL</TableHead>
                  <TableHead>Language ID</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {apis.map((api) => (
                  <TableRow key={api.api_id}>
                    <TableCell>{api.api_id}</TableCell>
                    <TableCell>{api.api_url}</TableCell>
                    <TableCell>{api.lang_id}</TableCell>
                    <TableCell>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => {
                          setCurrentAPI(api);
                          setIsDialogOpen(true);
                        }}
                      >
                        <Pencil className="h-4 w-4" />
                        <span className="sr-only">Edit</span>
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleDelete(api.api_id)}
                      >
                        <Trash2 className="h-4 w-4" />
                        <span className="sr-only">Delete</span>
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </main>
      <footer className="py-6 text-center text-sm text-gray-500">
        © 2024 LokaBhasha. All rights reserved.
      </footer>
    </div>
  );
}
