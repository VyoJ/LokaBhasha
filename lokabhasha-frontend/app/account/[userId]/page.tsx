"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { BookOpen, ArrowLeft, Trash } from "lucide-react";
import { Spinner } from "@/components/spinner";
import axios from "axios";

interface User {
  u_id: number;
  username: string;
  email: string;
  pref_lang: number | null;
}

export default function AccountPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    const storedUser = localStorage.getItem("user")!;
    if (storedUser) {
      const userData = JSON.parse(storedUser);
      if (userData.isLoggedIn && userData.id) {
        setUser({
          u_id: userData.id,
          username: userData.name,
          email: userData.email,
          pref_lang: userData.lang,
        });
        const userId = userData.id;
        fetch(`http://localhost:8000/users/${userId}`)
          .then((res) => res.json())
          .then((data) => setUser(data))
          .catch(() => router.push("/"));
      } else {
        router.push("/login");
      }
    } else {
      router.push("/login");
    }
  }, []);

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setUser((prev) => (prev ? { ...prev, [name]: value } : null));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const storedUser = localStorage.getItem("user");
    if (!storedUser || !user) return;

    const userData = JSON.parse(storedUser);
    const userId = userData.id;

    try {
      const { data } = await axios.put(`http://localhost:8000/users/${userId}`, {
        username: user.username,
        email: user.email,
        pref_lang: user.pref_lang,
      });
      
      localStorage.setItem("user", JSON.stringify({
        ...userData,
        name: data.username,
        email: data.email,
        lang: data.pref_lang
      }));
      
      setUser(data);
      setIsEditing(false);
    } catch (error) {
      console.error("Failed to update user:", error);
    }
  };

  const handleDelete = async () => {
    const storedUser = localStorage.getItem("user");
    if (!storedUser) return;

    const userId = JSON.parse(storedUser).id;

    try {
      await axios.delete(`http://localhost:8000/users/${userId}`);
      localStorage.clear();
      router.push("/");
    } catch (error) {
      console.error("Failed to delete user:", error);
    }
  };

  if (!user) {
    return <Spinner />;
  }

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
        <div className="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow">
          <h1 className="text-3xl font-bold text-orange-700 mb-6">
            Account Details
          </h1>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="username">Username</Label>
              <Input
                type="text"
                id="username"
                name="username"
                value={user.username}
                onChange={handleInputChange}
                disabled={!isEditing}
              />
            </div>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                type="email"
                id="email"
                name="email"
                value={user.email}
                onChange={handleInputChange}
                disabled={!isEditing}
              />
            </div>
            <div>
              <Label htmlFor="pref_lang">Preferred Language ID</Label>
              <Input
                type="number"
                id="pref_lang"
                name="pref_lang"
                value={user.pref_lang || ""}
                onChange={handleInputChange}
                disabled={!isEditing}
              />
            </div>
            {isEditing ? (
              <div className="flex justify-end space-x-2">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsEditing(false)}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  className="bg-orange-500 hover:bg-orange-600"
                >
                  Save Changes
                </Button>
              </div>
            ) : (
              <div className="flex justify-end space-x-2">
                <Button type="button" onClick={() => setIsEditing(true)}>
                  Edit Profile
                </Button>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button variant="destructive">
                      <Trash className="h-4 w-4 mr-2" />
                      Delete Account
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>
                        Are you sure you want to delete your account?
                      </AlertDialogTitle>
                      <AlertDialogDescription>
                        This action cannot be undone. This will permanently
                        delete your account and remove your data from our
                        servers.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                      <AlertDialogAction
                        onClick={handleDelete}
                        className="bg-red-600 hover:bg-red-700"
                      >
                        Yes, delete my account
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            )}
          </form>
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
