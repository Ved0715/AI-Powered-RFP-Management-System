"use client";

import { useState, useEffect } from "react";
import { Plus, Mail, Building2 } from "lucide-react";
import Link from "next/link";

export default function VendorsPage() {
  const [vendors, setVendors] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchVendors() {
      try {
        const res = await fetch("http://localhost:8000/api/vendors/");
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
  }, []);

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

      {/* Vendors Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {isLoading ? (
          <div className="col-span-full text-center py-12">Loading...</div>
        ) : vendors.length === 0 ? (
          <div className="col-span-full text-center py-12 bg-white rounded-xl border border-slate-200">
            <Building2 className="h-12 w-12 text-slate-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-slate-900">
              No vendors yet
            </h3>
            <p className="text-slate-500 mb-6">
              Add your first vendor to get started
            </p>
            <Link
              href="/dashboard/vendors/add"
              className="text-blue-600 font-medium hover:underline"
            >
              Add Vendor
            </Link>
          </div>
        ) : (
          vendors.map((vendor) => (
            <div
              key={vendor.id}
              className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-blue-50 rounded-lg">
                  <Building2 className="h-6 w-6 text-blue-600" />
                </div>
              </div>

              <h3 className="text-lg font-bold text-slate-900 mb-1">
                {vendor.name}
              </h3>
              <p className="text-sm text-slate-500 mb-4">
                {vendor.contact_name}
              </p>

              <div className="flex items-center gap-2 text-sm text-slate-600">
                <Mail className="h-4 w-4" />
                {vendor.email}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
