/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        abyss: { 900: '#04121f', 800: '#071e30', 700: '#0b2a42', 600: '#123a56' },
        sonar: { 400: '#22d3ee', 500: '#06b6d4' },
      },
    },
  },
  plugins: [],
}
