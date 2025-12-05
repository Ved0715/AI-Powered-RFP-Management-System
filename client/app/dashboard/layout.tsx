"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { LayoutDashboard, FileText, Users, Mail, LogOut} from "lucide-react"

export default function DashboardLayout({children,}: {children: React.ReactNode;}) {
    const pathname = usePathname();

    const navLinks =[
        {href: "/dashboard", icon: LayoutDashboard, label: "Dashboard"},
        { href: "/dashboard/rfps", icon: FileText, label: "RFPs" },
        { href: "/dashboard/vendors", icon: Users, label: "Vendors" },
        { href: "/dashboard/proposals", icon: Mail, label: "Proposals" },
    ]

    return (
        <div className="flex min-h-screen bg-slate-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200">
        {/* Logo */}
        {/* Navigation Links */}
        {/* Logout Button */}
      </aside>

      {/* Main Content */}
      <div className="flex-1">
        {/* Top Navbar */}
        <header className="bg-white border-b border-slate-200">
          {/* Breadcrumbs, User menu */}
        </header>

        {/* Page Content */}
        <main className="p-8">{children}</main>
      </div>
    </div>

    )
}