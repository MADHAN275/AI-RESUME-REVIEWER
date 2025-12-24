/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#2563EB", // Blue 600
        secondary: "#1E293B", // Slate 800
        accent: "#F59E0B", // Amber 500
        background: "#F8FAFC", // Slate 50
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
