import type { Metadata } from "next";
import { Toaster } from "sonner";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ragi Disease Detection",
  description: "AI-powered finger millet disease diagnosis",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body>
        {children}
        <Toaster richColors position="top-right" />
      </body>
    </html>
  );
}
