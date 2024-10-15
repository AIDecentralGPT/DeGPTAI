import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import legacy from "@vitejs/plugin-legacy";

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
		sveltekit(),
		legacy({
			targets: ['chrome 52'],
			additionalLegacyPolyfills: ['regenerator-runtime/runtime'],
			renderLegacyChunks: true,
			polyfills: [
			  'es.symbol',
			  'es.promise',
			  'es.promise.finally',
			  'es/map',
			  'es/set',
			  'es.array.filter',
			  'es.array.for-each',
			  'es.array.flat-map',
			  'es.object.define-properties',
			  'es.object.define-property',
			  'es.object.get-own-property-descriptor',
			  'es.object.get-own-property-descriptors',
			  'es.object.keys',
			  'es.object.to-string',
			  'web.dom-collections.for-each',
			  'esnext.global-this',
			  'esnext.string.match-all'
			]
		  }    
		)
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
		},
	},
});
