"use client";

import { useState, useEffect } from "react";
import {
  Plus,
  Mail,
  Building2,
  ChevronLeft,
  ChevronRight,
  Pencil,
  Trash2,
  Copy,
  Phone,
  Loader2,
} from "lucide-react";
import Link from "next/link";
import { AddVendorSheet } from "@/components/AddVendorSheet";
import { EditVendorSheet } from "@/components/EditVendorSheet";
import { Button } from "@/components/ui/button";

export default function VendorsPage() {
  const [vendors, setVendors] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const limit = 10; // Items per page


  const handleVendorUpdated = (updatedVendor: any) => {
  setVendors(vendors.map(v => v.id === updatedVendor.id ? updatedVendor : v));
};



  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this vendor?")) return;

    try {
      const res = await fetch(`http://localhost:8000/api/vendors/${id}`, {
        method: "DELETE",
      });
      if (res.ok) {
        setVendors(vendors.filter((v) => v.id !== id));
      } else {
        alert("Failed to delete vendor");
      }
    } catch (error) {
      console.error("Error deleting:", error);
    }
  };

  const handleVendorAdded = (newVendor: any) => {
    setVendors([newVendor, ...vendors]);
  };

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

        <AddVendorSheet onVendorAdded={handleVendorAdded} />
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
              <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                Phone
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
                  colSpan={5}
                  className="px-6 py-12 text-center text-slate-500"
                >
                  Loading...
                </td>
              </tr>
            ) : vendors.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center">
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
                <tr
                  key={vendor.id}
                  className="group hover:bg-slate-50 transition-colors duration-200"
                >
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-4">
                      <div className="h-10 w-10 rounded-full bg-linear-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white font-bold text-sm shadow-sm">
                        {vendor.name.substring(0, 2).toUpperCase()}
                      </div>
                      <div>
                        <span className="font-semibold text-slate-900 block">
                          {vendor.name}
                        </span>
                        <span className="text-xs text-slate-500">
                          ID: {vendor.id.slice(0, 8)}...
                        </span>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-slate-900 font-medium">
                      {vendor.contact_person || "N/A"}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div
                      className="flex items-center gap-2 text-sm text-slate-600 bg-slate-50 px-3 py-1.5 rounded-lg w-fit cursor-pointer hover:bg-slate-100 transition-colors group/copy"
                      onClick={() => {
                        navigator.clipboard.writeText(vendor.email);
                      }}
                      title="Click to copy email"
                    >
                      <Mail className="h-3.5 w-3.5 text-slate-400" />
                      {vendor.email}
                      <Copy className="h-3 w-3 text-slate-300 opacity-0 group-hover/copy:opacity-100 transition-opacity ml-1" />
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div
                      className="flex items-center gap-2 text-sm text-slate-600 bg-slate-50 px-3 py-1.5 rounded-lg w-fit cursor-pointer hover:bg-slate-100 transition-colors group/copy"
                      onClick={() => {
                        if (vendor.phone)
                          navigator.clipboard.writeText(vendor.phone);
                      }}
                      title="Click to copy phone"
                    >
                      <Phone className="h-3.5 w-3.5 text-slate-400" />
                      {vendor.phone || "N/A"}
                      {vendor.phone && (
                        <Copy className="h-3 w-3 text-slate-300 opacity-0 group-hover/copy:opacity-100 transition-opacity ml-1" />
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <EditVendorSheet 
                          vendor={vendor} 
                          onVendorUpdated={handleVendorUpdated} 
                        />
                      <button
                        onClick={() => handleDelete(vendor.id)}
                        className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
                        title="Delete Vendor"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
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
