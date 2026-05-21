import type { Config } from "tailwindcss";
import animate from "tailwindcss-animate";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#070b12",
        foreground: "#edf7f1",
        border: "rgba(255,255,255,0.14)",
        muted: "#91a39a",
        primary: "#7cf7b2",
        accent: "#73d7ff",
        card: "rgba(14,23,31,0.72)",
      },
      boxShadow: {
        glow: "0 0 42px rgba(124, 247, 178, 0.18)",
      },
      backgroundImage: {
        mesh:
          "radial-gradient(circle at 18% 18%, rgba(124,247,178,.18), transparent 30%), radial-gradient(circle at 82% 10%, rgba(115,215,255,.16), transparent 32%), linear-gradient(135deg, #070b12 0%, #0b1412 52%, #08111a 100%)",
      },
    },
  },
  plugins: [animate],
};

export default config;
