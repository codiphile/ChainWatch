import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ChainWatch | Supply Chain Risk Monitor',
  description: 'AI-powered supply chain risk monitoring and intelligence platform',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-noise">{children}</body>
    </html>
  );
}
