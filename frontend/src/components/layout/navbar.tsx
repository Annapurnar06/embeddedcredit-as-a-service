"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Menu, X, ChevronDown } from "lucide-react";

const navLinks = [
  {
    label: "Platform",
    href: "#platform",
    children: [
      { label: "How It Works", href: "#how-it-works" },
      { label: "Tool Stack", href: "#tools" },
      { label: "Segments", href: "#segments" },
      { label: "Compliance", href: "#compliance" },
    ],
  },
  { label: "Use Cases", href: "#use-cases" },
  { label: "Pricing", href: "#pricing" },
];

export function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-lg border-b border-border/50">
      <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
              <span className="text-white font-bold text-sm">EC</span>
            </div>
            <span className="font-semibold text-foreground text-lg hidden sm:block">
              EmbeddedCredit
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) =>
              link.children ? (
                <div key={link.label} className="relative">
                  <button
                    onClick={() => setDropdownOpen(!dropdownOpen)}
                    className="flex items-center gap-1 px-3 py-2 text-sm text-muted-foreground hover:text-foreground transition-colors rounded-lg hover:bg-muted cursor-pointer"
                  >
                    {link.label}
                    <ChevronDown className="h-3.5 w-3.5" />
                  </button>
                  {dropdownOpen && (
                    <div className="absolute top-full left-0 mt-1 w-48 bg-white rounded-lg border border-border shadow-lg py-1">
                      {link.children.map((child) => (
                        <a
                          key={child.label}
                          href={child.href}
                          className="block px-4 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
                          onClick={() => setDropdownOpen(false)}
                        >
                          {child.label}
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                <a
                  key={link.label}
                  href={link.href}
                  className="px-3 py-2 text-sm text-muted-foreground hover:text-foreground transition-colors rounded-lg hover:bg-muted"
                >
                  {link.label}
                </a>
              )
            )}
          </div>

          <div className="hidden md:flex items-center gap-3">
            <Link href="/dashboard">
              <Button variant="ghost" size="sm">
                Lender Login
              </Button>
            </Link>
            <Button size="sm">Request Demo</Button>
          </div>

          <button
            className="md:hidden p-2 rounded-lg hover:bg-muted cursor-pointer"
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>

        {mobileOpen && (
          <div className="md:hidden border-t border-border py-4 space-y-1">
            {navLinks.map((link) => (
              <div key={link.label}>
                <a
                  href={link.href}
                  className="block px-3 py-2 text-sm text-muted-foreground hover:text-foreground rounded-lg hover:bg-muted"
                  onClick={() => setMobileOpen(false)}
                >
                  {link.label}
                </a>
                {link.children?.map((child) => (
                  <a
                    key={child.label}
                    href={child.href}
                    className="block px-6 py-1.5 text-sm text-muted-foreground hover:text-foreground"
                    onClick={() => setMobileOpen(false)}
                  >
                    {child.label}
                  </a>
                ))}
              </div>
            ))}
            <div className="pt-3 border-t border-border flex flex-col gap-2 px-3">
              <Link href="/dashboard">
                <Button variant="outline" size="sm" className="w-full">
                  Lender Login
                </Button>
              </Link>
              <Button size="sm" className="w-full">
                Request Demo
              </Button>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
}
