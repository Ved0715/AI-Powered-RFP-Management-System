"use client";

import { useEffect, useState } from "react";
import { FileText, Users, Mail, TrendingUp } from "lucide-react";
import { StatCard } from "@/components/reusable";

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalRFPs: 0,
    totalVendors: 0,
    totalProposals: 0,
    activeRFPs: 0,
  });

  useEffect(() => {}, []);

  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-900 mb-8 m-4">Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total RFPs"
          value={stats.totalRFPs}
          icon={FileText}
        />
        <StatCard
          title="Total Vendors"
          value={stats.totalVendors}
          icon={Users}
        />
        <StatCard
          title="Total Proposals"
          value={stats.totalProposals}
          icon={Mail}
        />
        <StatCard
          title="Active RFPs"
          value={stats.activeRFPs}
          icon={TrendingUp}
        />
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Proposals */}
      </div>
    </div>
  );
}
