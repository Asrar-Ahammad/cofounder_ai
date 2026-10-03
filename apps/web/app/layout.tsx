import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Cofunder — AI Co-Founder Suite",
  description: "Supervisor-led swarm of specialist agents sharing one persistent business brain",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} dark`}>
      <body className="antialiased bg-[#09090b] text-[#fafafa] min-h-screen">
        {children}
      </body>
    </html>
  );
}
