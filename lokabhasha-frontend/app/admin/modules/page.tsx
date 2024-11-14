"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { BookOpen, Plus, Pencil, Trash2 } from "lucide-react";
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

interface Module {
  id: number;
  lang_id: number;
  name: string;
  desc: string;
  pre_id?: number;
}

export default function AdminModules() {
  const router = useRouter();
  const [modules, setModules] = useState<Module[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [currentModule, setCurrentModule] = useState<Module | null>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      const userData = JSON.parse(storedUser);
      if (userData.email === "admin@admin.com") {
        fetchModules();
      } else {
        router.push("/admin/login");
      }
    } else {
      router.push("/admin/login");
    }
  }, [router]);

  const fetchModules = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:8000/modules/");
      const data = await response.json();
      const mappedModules = data.map((m: any) => ({
        id: m.m_id,
        lang_id: m.lang_id,
        name: m.name,
        desc: m.desc,
        pre_id: m.pre_id,
      }));
      setModules(mappedModules);
    } catch (error) {
      console.error("Failed to fetch modules:", error);
    }
    setIsLoading(false);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const formData = new FormData(form);

    const moduleData = {
      lang_id: 1, // Add proper language ID selection
      name: formData.get("name") as string,
      desc: formData.get("description") as string,
      pre_id: null, // Add if needed
    };

    try {
      const url = currentModule
        ? `http://localhost:8000/modules/${currentModule.id}`
        : "http://localhost:8000/modules/";
      const method = currentModule ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(moduleData),
      });

      if (response.ok) {
        const data = await response.json();
        fetchModules();
        setIsDialogOpen(false);
        setCurrentModule(null);
      } else {
        console.error("Failed to save module");
      }
    } catch (error) {
      console.error("Error saving module:", error);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this module?")) {
      try {
        const response = await fetch(`http://localhost:8000/modules/${id}`, {
          method: "DELETE",
        });

        if (response.ok) {
          fetchModules();
        } else {
          console.error("Failed to delete module");
        }
      } catch (error) {
        console.error("Error deleting module:", error);
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
            href="/admin/dashboard"
          >
            Analytics
          </Link>
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            href="/admin/apis"
          >
            Settings
          </Link>
        </nav>
      </header>
      <main className="flex-1 p-4 md:p-6 space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Manage Modules</h1>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={() => setCurrentModule(null)}>
                <Plus className="mr-2 h-4 w-4" /> Add New Module
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>
                  {currentModule ? "Edit Module" : "Add New Module"}
                </DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="name">Module Name</Label>
                  <Input
                    id="name"
                    name="name"
                    defaultValue={currentModule?.name}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="description">Description</Label>
                  <Input
                    id="description"
                    name="description"
                    defaultValue={currentModule?.desc}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="lang_id">Language</Label>
                  <Input
                    id="lang_id"
                    name="lang_id"
                    type="number"
                    defaultValue={currentModule?.lang_id || 1}
                    required
                  />
                </div>
                <Button type="submit">Save Module</Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>
        <Card>
          <CardHeader>
            <CardTitle>Modules List</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Description</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {modules.map((module) => (
                  <TableRow key={module.id}>
                    <TableCell>{module.name}</TableCell>
                    <TableCell>{module.desc}</TableCell>
                    <TableCell>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => {
                          setCurrentModule(module);
                          setIsDialogOpen(true);
                        }}
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleDelete(module.id)}
                      >
                        <Trash2 className="h-4 w-4" />
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
