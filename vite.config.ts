import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

// /** @type {import('vite').Plugin} */
// const viteServerConfig = {
// 	name: 'log-request-middleware',
// 	configureServer(server) {
// 		server.middlewares.use((req, res, next) => {
// 			res.setHeader('Access-Control-Allow-Origin', '*');
// 			res.setHeader('Access-Control-Allow-Methods', 'GET');
// 			res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
// 			res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
// 			next();
// 		});
// 	}
// };

export default defineConfig({
	plugins: [
		sveltekit()
	],
	define: {
		APP_VERSION: JSON.stringify(process.env.npm_package_version)
	},
	worker: {
		format: 'es'
	},
	optimizeDeps: {
		include: ['core-js']
	},
	server: {
		fs: {
			allow: [
				'./static',
			],
		}
	},
	build: {
    // Enable code compression
    minify: 'terser',
    terserOptions: {
      // Customize Terser Configuration
      compress: {
        drop_console: true, // Remove console statement
        drop_debugger: true // Remove the debugger statement
      }
    }
  }
});
