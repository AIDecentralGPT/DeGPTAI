/** @type {import('tailwindcss').Config} */
export default {
	darkMode: 'class',
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				gray: {
					50: '#f9f9f9',
					100: '#ececec',
					200: '#e3e3e3',
					300: '#cdcdcd',
					400: '#b4b4b4',
					500: '#9b9b9b',
					600: '#676767',
					700: '#4e4e4e',
					800: '#333',
					850: '#262626',
					900: 'var(--color-gray-900, #171717)',
					950: 'var(--color-gray-950, #0d0d0d)'
				},
				primary: {
					DEFAULT: 'rgba(184, 142, 86, 1)',  // 你可以根据需要更改默认颜色
					light: 'rgba(184, 142, 86, 1)',
					dark: 'rgba(184, 142, 86, 1)',
			},
			},


			typography: {
				DEFAULT: {
					css: {
						pre: false,
						code: false,
						'pre code': false,
						'code::before': false,
						'code::after': false,
						// 修改默认的 prose 样式中 hr 标签的 margin
						hr: {
							marginTop: '0.1em',
							marginBottom: '0.1em',
						}
					}
				}
			}
		}
	},
	plugins: [require('@tailwindcss/typography')]
};
