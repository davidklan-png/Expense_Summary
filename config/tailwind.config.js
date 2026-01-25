/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./web_app.py",
    "./src/**/*.{py,html,js}",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        // Primary brand color
        primary: {
          50: '#E3F2FD',
          100: '#BBDEFB',
          200: '#90CAF9',
          300: '#64B5F6',
          400: '#42A5F5',
          500: '#1f77b4', // Main brand color
          600: '#1565C0',
          700: '#0D47A1',
          800: '#0A3D91',
          900: '#063060',
        },
        // Secondary/accent color (teal/green for success)
        secondary: {
          50: '#E0F2F1',
          100: '#B2DFDB',
          200: '#80CBC4',
          300: '#4DB6AC',
          400: '#26A69A',
          500: '#009688',
          600: '#00897B',
          700: '#00695C',
          800: '#00564A',
          900: '#003D33',
        },
        // Accent color (orange/amber for CTAs)
        accent: {
          50: '#FFF8E1',
          100: '#FFECB3',
          200: '#FFE082',
          300: '#FFD54F',
          400: '#FFCA28',
          500: '#FFC107',
          600: '#FFB300',
          700: '#F57C00',
          800: '#EF6C00',
          900: '#E65100',
        },
        // Neutral grays
        neutral: {
          50: '#FAFAFA',
          100: '#F5F5F5',
          200: '#EEEEEE',
          300: '#E0E0E0',
          400: '#BDBDBD',
          500: '#9E9E9E',
          600: '#757575',
          700: '#616161',
          800: '#424242',
          900: '#212121',
        },
        // Semantic colors
        success: {
          light: '#d4edda',
          DEFAULT: '#28a745',
          dark: '#1e7e34',
          border: '#c3e6cb',
        },
        error: {
          light: '#f8d7da',
          DEFAULT: '#dc3545',
          dark: '#bd2130',
          border: '#f5c6cb',
        },
        warning: {
          light: '#fff3cd',
          DEFAULT: '#ffc107',
          dark: '#e0a800',
          border: '#ffc107',
        },
        info: {
          light: '#d1ecf1',
          DEFAULT: '#17a2b8',
          dark: '#117a8b',
          border: '#bee5eb',
        },
      },
      fontFamily: {
        sans: ['Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'sans-serif'],
        mono: ['Fira Code', 'Monaco', 'Consolas', 'monospace'],
      },
      fontSize: {
        // H1 - Main page title
        'h1': ['2.5rem', { lineHeight: '1.2', fontWeight: '700' }],
        // H2 - Section headers
        'h2': ['2rem', { lineHeight: '1.3', fontWeight: '600' }],
        // H3 - Subsection headers
        'h3': ['1.5rem', { lineHeight: '1.4', fontWeight: '600' }],
        // H4 - Card headers
        'h4': ['1.25rem', { lineHeight: '1.5', fontWeight: '600' }],
        // H5 - Small headers
        'h5': ['1.125rem', { lineHeight: '1.5', fontWeight: '600' }],
        // H6 - Tiny headers
        'h6': ['1rem', { lineHeight: '1.5', fontWeight: '600' }],
        // Body text
        'body': ['1rem', { lineHeight: '1.6', fontWeight: '400' }],
        'body-sm': ['0.875rem', { lineHeight: '1.5', fontWeight: '400' }],
        // Caption
        'caption': ['0.75rem', { lineHeight: '1.4', fontWeight: '400' }],
        // Button text
        'btn': ['0.875rem', { lineHeight: '1', fontWeight: '600' }],
      },
      spacing: {
        // 8px baseline grid
        'xs': '0.25rem',   // 4px
        'sm': '0.5rem',    // 8px
        'md': '1rem',      // 16px
        'lg': '1.5rem',    // 24px
        'xl': '2rem',      // 32px
        '2xl': '3rem',     // 48px
        '3xl': '4rem',     // 64px
        // Component-specific
        'btn-x': '1.5rem',      // 24px
        'btn-y': '0.625rem',    // 10px
        'card': '1.5rem',       // 24px
        'container': '2rem',    // 32px
        'input-x': '0.75rem',   // 12px
        'input-y': '0.625rem',  // 10px
      },
      borderRadius: {
        'sm': '0.25rem',   // 4px
        'DEFAULT': '0.5rem',   // 8px
        'md': '0.5rem',    // 8px
        'lg': '0.75rem',   // 12px
        'xl': '1rem',      // 16px
        '2xl': '1.5rem',   // 24px
        'full': '9999px',  // Pills
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'DEFAULT': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'slide-up': {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'slide-down': {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'scale-in': {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
      animation: {
        'fade-in': 'fade-in 0.2s ease-out',
        'slide-up': 'slide-up 0.3s ease-out',
        'slide-down': 'slide-down 0.3s ease-out',
        'scale-in': 'scale-in 0.2s ease-out',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
