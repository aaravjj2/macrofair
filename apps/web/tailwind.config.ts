import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        canvas: "#081725",
        panel: "#0f2638",
        ink: "#eef6fb",
        accent: "#f4a259",
        success: "#6ed39e",
        danger: "#ff6f61"
      },
      boxShadow: {
        panel: "0 18px 50px -20px rgba(0, 0, 0, 0.6)"
      }
    }
  },
  plugins: []
};

export default config;
