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
    // 开启代码压缩
    minify: 'terser',
		rollupOptions: {
			output: {
				assetFileNames: 'assets/[name]-[hash][extname]',
				chunkFileNames: 'chunks/[name]-[hash].js',
				entryFileNames: 'entries/[name]-[hash].js'
			}
		},
    terserOptions: {
      // 自定义 terser 配置
      compress: {
        // drop_console: true, // 移除 console 语句
        drop_debugger: true // 移除 debugger 语句
      }
    }
  }
});
