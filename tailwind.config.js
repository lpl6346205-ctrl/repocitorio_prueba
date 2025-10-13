/** @type {import('tailwindcss').Config} */
module.exports = {
  // This array specifies which files Tailwind should scan for utility classes
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-blue': '#4F46E5', /* Indigo-600 */
        'primary-dark': '#1F2937', /* Gray-800 */
        'secondary-gray': '#E5E7EB', /* Gray-200 */
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}