const config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#FEFCF7",
        foreground: "#2D3748",
        card: "#FFFFFF",
        terracotta: {
          DEFAULT: "#E07A5F",
          light: "#F0A98C",
        },
        pine: {
          DEFAULT: "#3D7A65",
          light: "#5A9A85",
        },
        muted: {
          DEFAULT: "#8D99AE",
          light: "#A8B0BD",
        },
      },
    },
  },
  plugins: [],
};

export default config;