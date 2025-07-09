import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/kit/vite';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: vitePreprocess(),
	kit: {
		// adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
		// If your environment is not supported or you settled on a specific environment, switch out the adapter.
		// See https://kit.svelte.dev/docs/adapters for more information about adapters.
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: 'index.html',
			// 新增预渲染选项（确保哈希正常工作）
			precompress: true // 如果不需要gzip压缩可以设为false
		}),
		// 确保输出文件带哈希（默认已启用，显式声明更明确）
		version: {
			name: Date.now().toString() // 每次构建生成唯一版本ID
		}
	},
	onwarn: (warning, handler) => {
		const { code, _ } = warning;
		if (code === 'css-unused-selector') return;
		if (warning.code.startsWith('a11y-')) return;
		handler(warning);
	},
};

export default config;
