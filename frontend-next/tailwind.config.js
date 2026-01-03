/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'void': {
          950: '#030712',
          900: '#0a0f1a',
          800: '#111827',
          700: '#1e293b',
          600: '#334155',
        },
        'risk': {
          low: '#10b981',
          'low-glow': '#34d399',
          medium: '#f59e0b',
          'medium-glow': '#fbbf24',
          high: '#ef4444',
          'high-glow': '#f87171',
        },
        'cyber': {
          blue: '#06b6d4',
          purple: '#8b5cf6',
          pink: '#ec4899',
        }
      },
      fontFamily: {
        'display': ['Orbitron', 'monospace'],
        'mono': ['JetBrains Mono', 'monospace'],
        'body': ['Outfit', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'scan': 'scan 4s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
        'radar': 'radar 4s linear infinite',
      },
      keyframes: {
        scan: {
          '0%, 100%': { transform: 'translateY(-100%)' },
          '50%': { transform: 'translateY(100%)' },
        },
        glow: {
          '0%': { opacity: '0.5', filter: 'blur(10px)' },
          '100%': { opacity: '1', filter: 'blur(20px)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        radar: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
      },
      backgroundImage: {
        'grid-pattern': 'linear-gradient(rgba(6, 182, 212, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(6, 182, 212, 0.03) 1px, transparent 1px)',
        'radial-glow': 'radial-gradient(ellipse at center, var(--glow-color) 0%, transparent 70%)',
      },
    },
  },
  plugins: [],
}
