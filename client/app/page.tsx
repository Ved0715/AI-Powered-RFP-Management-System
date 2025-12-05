"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  Zap,
  Mail,
  Brain,
  BarChart3,
  ArrowRight,
  CheckCircle2,
  TrendingUp,
} from "lucide-react";

// Animated Card Component
const FeatureCard = ({
  children,
  delay = 0,
}: {
  children: React.ReactNode;
  delay?: number;
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay, duration: 0.4 }}
      whileHover={{ y: -8 }}
      className="group relative overflow-hidden rounded-2xl border border-slate-200 bg-white p-8 shadow-sm transition-all hover:shadow-xl hover:shadow-indigo-500/10"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-blue-500/5 opacity-0 transition-opacity group-hover:opacity-100" />
      <div className="relative z-10">{children}</div>
    </motion.div>
  );
};

export default function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 z-50 w-full border-b border-slate-200/60 bg-white/90 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-700 to-blue-700 shadow-lg shadow-indigo-700/30">
              <Zap className="h-5 w-5 text-white" />
            </div>
            <span className="text-2xl font-bold text-slate-900">RFP AI</span>
          </div>

          <div className="hidden items-center gap-8 md:flex">
            <a
              href="#features"
              className="text-slate-600 transition hover:text-slate-900 font-medium"
            >
              Features
            </a>
            <a
              href="#how-it-works"
              className="text-slate-600 transition hover:text-slate-900 font-medium"
            >
              How It Works
            </a>
            <Link
              href="/dashboard"
              className="rounded-xl bg-indigo-700 px-6 py-2.5 font-semibold text-white transition-all hover:bg-indigo-800 hover:shadow-lg hover:shadow-indigo-700/40"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen overflow-hidden bg-gradient-to-b from-slate-50 via-white to-slate-50 pt-32">
        {/* Subtle Grid Background */}
        <div className="absolute inset-0 bg-grid-slate-200/50 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))]" />

        <div className="relative z-10 mx-auto max-w-7xl px-6">
          <div className="mx-auto max-w-4xl text-center">
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="mb-8 inline-flex items-center gap-2 rounded-full border border-indigo-200 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700"
            >
              <Zap className="h-4 w-4" />
              Powered by OpenAI & CrewAI
            </motion.div>

            {/* Heading */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="mb-6 text-6xl font-bold leading-tight text-slate-900 md:text-7xl lg:text-8xl"
            >
              AI-Powered <br className="hidden md:block" />
              <span className="bg-gradient-to-r from-indigo-700 to-blue-700 bg-clip-text text-transparent">
                RFP Management
              </span>
            </motion.h1>

            {/* Subheading */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="mx-auto mb-12 max-w-2xl text-xl leading-relaxed text-slate-600"
            >
              Automate vendor management, parse proposals with AI, and get
              intelligent recommendations. Cut procurement time by{" "}
              <span className="font-bold text-indigo-700">80%</span>.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="flex flex-col items-center justify-center gap-4 sm:flex-row"
            >
              <Link
                href="/dashboard"
                className="group inline-flex items-center gap-2 rounded-2xl bg-indigo-700 px-8 py-4 text-lg font-bold text-white shadow-xl shadow-indigo-700/30 transition-all hover:bg-indigo-800 hover:scale-105 hover:shadow-2xl hover:shadow-indigo-700/40"
              >
                <span>Start Free Trial</span>
                <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Link>
              <a
                href="#demo"
                className="inline-flex items-center gap-2 rounded-2xl border-2 border-slate-300 bg-white px-8 py-4 text-lg font-bold text-slate-700 transition-all hover:border-slate-400 hover:shadow-xl"
              >
                Watch Demo
              </a>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
              className="mx-auto mt-20 grid max-w-3xl grid-cols-3 gap-8"
            >
              <div className="text-center">
                <div className="mb-2 text-5xl font-bold text-indigo-700">
                  80%
                </div>
                <div className="text-sm font-medium text-slate-600">
                  Time Saved
                </div>
              </div>
              <div className="text-center">
                <div className="mb-2 text-5xl font-bold text-blue-700">95%</div>
                <div className="text-sm font-medium text-slate-600">
                  Accuracy
                </div>
              </div>
              <div className="text-center">
                <div className="mb-2 text-5xl font-bold text-indigo-700">
                  4x
                </div>
                <div className="text-sm font-medium text-slate-600">Faster</div>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Subtle Decorative Blurs */}
        <div className="absolute -left-40 bottom-0 h-80 w-80 rounded-full bg-indigo-400 opacity-10 blur-3xl" />
        <div className="absolute -right-40 top-40 h-80 w-80 rounded-full bg-blue-400 opacity-10 blur-3xl" />
      </section>

      {/* Features Section */}
      <section id="features" className="relative bg-white py-32">
        <div className="mx-auto max-w-7xl px-6">
          <div className="mb-16 text-center">
            <h2 className="mb-4 text-5xl font-bold text-slate-900">
              Powerful Features
            </h2>
            <p className="text-xl text-slate-600">
              Everything you need to streamline procurement
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            <FeatureCard delay={0}>
              <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-700 shadow-lg shadow-indigo-700/30">
                <Brain className="h-7 w-7 text-white" />
              </div>
              <h3 className="mb-3 text-2xl font-bold text-slate-900">
                AI RFP Generation
              </h3>
              <p className="leading-relaxed text-slate-600">
                Describe your needs in plain English. AI generates structured
                RFPs with requirements, budget, and deadlines.
              </p>
            </FeatureCard>

            <FeatureCard delay={0.1}>
              <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-700 shadow-lg shadow-blue-700/30">
                <Mail className="h-7 w-7 text-white" />
              </div>
              <h3 className="mb-3 text-2xl font-bold text-slate-900">
                Email Integration
              </h3>
              <p className="leading-relaxed text-slate-600">
                Send RFPs via email and automatically receive vendor responses.
                SMTP/IMAP for seamless communication.
              </p>
            </FeatureCard>

            <FeatureCard delay={0.2}>
              <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-700 shadow-lg shadow-indigo-700/30">
                <Zap className="h-7 w-7 text-white" />
              </div>
              <h3 className="mb-3 text-2xl font-bold text-slate-900">
                Smart Parsing
              </h3>
              <p className="leading-relaxed text-slate-600">
                AI extracts pricing, delivery time, terms, and warranty from
                vendor emails automatically.
              </p>
            </FeatureCard>

            <FeatureCard delay={0.3}>
              <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-700 shadow-lg shadow-blue-700/30">
                <BarChart3 className="h-7 w-7 text-white" />
              </div>
              <h3 className="mb-3 text-2xl font-bold text-slate-900">
                Multi-Agent Analysis
              </h3>
              <p className="leading-relaxed text-slate-600">
                CrewAI agents (Cost, Quality, Compliance) collaborate to analyze
                and recommend the best vendor.
              </p>
            </FeatureCard>

            <FeatureCard delay={0.4}>
              <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-700 shadow-lg shadow-indigo-700/30">
                <TrendingUp className="h-7 w-7 text-white" />
              </div>
              <h3 className="mb-3 text-2xl font-bold text-slate-900">
                Real-time Dashboard
              </h3>
              <p className="leading-relaxed text-slate-600">
                Track RFPs, proposals, and vendor performance in one beautiful
                dashboard with instant insights.
              </p>
            </FeatureCard>

            <FeatureCard delay={0.5}>
              <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-700 shadow-lg shadow-blue-700/30">
                <CheckCircle2 className="h-7 w-7 text-white" />
              </div>
              <h3 className="mb-3 text-2xl font-bold text-slate-900">
                Intelligent Scoring
              </h3>
              <p className="leading-relaxed text-slate-600">
                Each proposal gets an AI score (0-100) based on cost, quality,
                and compliance for data-driven decisions.
              </p>
            </FeatureCard>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-indigo-700 to-blue-700 py-32">
        <div className="absolute inset-0 bg-grid-white/10 [mask-image:linear-gradient(0deg,rgba(0,0,0,0.8),rgba(0,0,0,0.4))]" />

        <div className="relative z-10 mx-auto max-w-4xl px-6 text-center">
          <h2 className="mb-6 text-5xl font-bold text-white md:text-6xl">
            Ready to Transform Your Procurement?
          </h2>
          <p className="mb-10 text-xl text-indigo-100">
            Join modern companies using AI to streamline their RFP process
          </p>
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 rounded-2xl bg-white px-8 py-4 text-lg font-bold text-indigo-700 shadow-2xl transition-all hover:scale-105 hover:shadow-white/20"
          >
            Get Started Free
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 py-12 text-slate-400 border-t border-slate-800">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <div className="mb-4 flex items-center justify-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-700 to-blue-700">
              <Zap className="h-5 w-5 text-white" />
            </div>
            <span className="text-2xl font-bold text-white">RFP AI</span>
          </div>
          <p className="text-sm">© 2025 RFP AI. Powered by OpenAI & CrewAI.</p>
        </div>
      </footer>
    </div>
  );
}
