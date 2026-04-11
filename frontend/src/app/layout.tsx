import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "EmbeddedCredit | AI-Native Lending Infrastructure for India",
    template: "%s | EmbeddedCredit",
  },
  description:
    "The AI lending operating system for India's 300 million underserved borrowers. From WhatsApp to disbursement in 15 minutes. 60 tools, 38 segments, one platform.",
  keywords: [
    "embedded credit",
    "AI lending",
    "NBFC",
    "lending infrastructure",
    "alternative data scoring",
    "WhatsApp lending",
    "micro lending",
    "India fintech",
  ],
  openGraph: {
    title: "EmbeddedCredit | AI-Native Lending Infrastructure",
    description:
      "WhatsApp to disbursement in 15 minutes. 60 tools. 38 segments. 80-90% cost reduction.",
    type: "website",
    locale: "en_IN",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
