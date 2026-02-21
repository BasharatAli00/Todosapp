"use client";

import React, { useState } from "react";
import Link from "next/link";
import api from "../../lib/api";


const RegisterPage = () => {
  // Form state
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    first_name: "",
    last_name: "",
    password: "",
    phone_number: "",
    role: "user",
  });

  // Handle input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Handle submit (for now, just log)
 const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  try {
    // POST data to FastAPI
    const response = await api.post("/auth/user_auth", {
      Email: formData.email,
      Username: formData.username,
      First_name: formData.first_name,
      Last_name: formData.last_name,
      Password: formData.password,
      Is_active: true,       // hidden but always true
      Role: formData.role,    // selectable
      phone_number: formData.phone_number,
    });

    if (response.status === 201) {
      alert("User registered successfully! Redirecting to login...");
      // Redirect to login page
      window.location.href = "/login";
    }
  } catch (error: any) {
    console.error(error);
    alert(
      error.response?.data?.detail ||
        "Failed to register. Please check the details."
    );
  }
};

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-purple-400 to-pink-400">
      <div className="bg-gray-50 rounded-lg shadow-lg p-8 w-full max-w-md text-gray-900">
        <h2 className="text-2xl font-bold mb-6 text-center">Register</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded"
            required
          />
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded"
            required
          />
          <input
            type="text"
            name="first_name"
            placeholder="First Name"
            value={formData.first_name}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded"
            required
          />
          <input
            type="text"
            name="last_name"
            placeholder="Last Name"
            value={formData.last_name}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded"
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded"
            required
          />
          <input
            type="text"
            name="phone_number"
            placeholder="Phone Number"
            value={formData.phone_number}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded"
          />
          <select
            name="role"
            value={formData.role}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded"
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
          <button
            type="submit"
            className="w-full bg-purple-500 text-white p-2 rounded hover:bg-purple-600 transition"
          >
            Register
          </button>
        </form>
        <p className="text-sm mt-4 text-center">
          Already have an account?{" "}
          <Link href="/login" className="text-purple-600 hover:underline">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
