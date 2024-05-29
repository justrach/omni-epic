import type { Metadata } from "next";
import { Crimson_Text, Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";
const inter = Inter({ subsets: ["latin"] });

let title = 'OMNI EPIC |  Maxence Faldor | Jenny Zhang | Jeff Clune | Antoine Cully | ';
let description = 'Coming soon';
let ogimage = 'https://omni-epic.vercel.app/main.png';
let url = 'https://omni-epic.vercel.app/';
let sitename = 'omni epic';
// lamo this is stupid
export const metadata: Metadata = {
   keywords :[
   "omni-epic",
   "video game ai",
    "open-endedness",
    "interestingness",
    "human notions",
    "environments",
    "programmed",
    "code",
  ],
  metadataBase: new URL(url),
  title,
  description,
  icons: {
    icon: '/favicon.ico',
  },
  openGraph: {
    images: [ogimage],
    title,
    description,
    url: url,
    siteName: sitename,
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    images: [ogimage],
    title,
    description,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <main>{children}</main>
        <Toaster />
      </body>
    </html>
  );
}
