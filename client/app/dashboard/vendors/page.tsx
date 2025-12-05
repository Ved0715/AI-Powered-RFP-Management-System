"use client";

import { useState, useEffect } from "react";
import { Plus, Mail, Building2, ChevronLeft, ChevronRight, MoreHorizontal } from "lucide-react";
import Link from "next/link";

export default function VendorsPage() {
  const [vendors, setVendors] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const limit = 10; // Items per page

  useEffect(() => {
    async function fetchVendors() {
      setIsLoading(true);
      try {
        const skip = (page - 1) * limit;
        const res = await fetch(
          `http://localhost:8000/api/vendors/?skip=${skip}&limit=${limit}`
        );
        if (res.ok) {
          const data = await res.json();
          setVendors(data);
        }
      } catch (error) {
        console.error("Failed to fetch vendors", error);
      } finally {
        setIsLoading(false);
      }
    }
    fetchVendors();
  }, [page]);

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Vendors</h1>
          <p className="text-slate-500 mt-1">Manage your supplier database</p>
        </div>
        <Link
          href="/dashboard/vendors/add"
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          <Plus className="h-4 w-4" />
          Add Vendor
        </Link>
      </div>

      {/* Vendors List (Table) */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200">
              <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                Company
              </th>
              <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                Contact Person
              </th>
              <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                Email
              </th>
              <th className="px-6 py-4 text-sm font-semibold text-slate-700 text-right">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {isLoading ? (
              <tr>
                <td
                  colSpan={4}
                  className="px-6 py-12 text-center text-slate-500"
                >
                  Loading...
                </td>
              </tr>
            ) : vendors.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-6 py-12 text-center">
                  <div className="flex flex-col items-center justify-center">
                    <Building2 className="h-10 w-10 text-slate-300 mb-3" />
                    <p className="text-slate-500 font-medium">
                      No vendors found
                    </p>
                    <p className="text-sm text-slate-400">
                      Add a new vendor to get started
                    </p>
                  </div>
                </td>
              </tr>
            ) : (
              vendors.map((vendor) => (
                <tr key={vendor.id} className="hover:bg-slate-50 transition">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 rounded-lg bg-blue-50 flex items-center justify-center text-blue-600">
                        <Building2 className="h-5 w-5" />
                      </div>
                      <span className="font-medium text-slate-900">
                        {vendor.name}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-slate-600">
                    {vendor.contact_name || vendor.contact_person}
                  </td>
                  <td className="px-6 py-4 text-slate-600">
                    <div className="flex items-center gap-2">
                      <Mail className="h-4 w-4 text-slate-400" />
                      {vendor.email}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-slate-400 hover:text-slate-600 p-2 hover:bg-slate-100 rounded-lg transition">
                      <MoreHorizontal className="h-5 w-5" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Controls */}
      <div className="flex items-center justify-between mt-6">
        <p className="text-sm text-slate-500">
          Showing page{" "}
          <span className="font-medium text-slate-900">{page}</span>
        </p>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1 || isLoading}
            className="p-2 border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            <ChevronLeft className="h-5 w-5 text-slate-600" />
          </button>
          <button
            onClick={() => setPage((p) => p + 1)}
            disabled={vendors.length < limit || isLoading}
            className="p-2 border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            <ChevronRight className="h-5 w-5 text-slate-600" />
          </button>
        </div>
      </div>
    </div>
  );
}
