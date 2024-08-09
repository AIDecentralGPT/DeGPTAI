export { matchers } from './matchers.js';

export const nodes = [
	() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8'),
	() => import('./nodes/9'),
	() => import('./nodes/10'),
	() => import('./nodes/11'),
	() => import('./nodes/12'),
	() => import('./nodes/13'),
	() => import('./nodes/14'),
	() => import('./nodes/15'),
	() => import('./nodes/16'),
	() => import('./nodes/17'),
	() => import('./nodes/18'),
	() => import('./nodes/19'),
	() => import('./nodes/20'),
	() => import('./nodes/21'),
	() => import('./nodes/22')
];

export const server_loads = [];

export const dictionary = {
		"/(app)": [4,[2]],
		"/(app)/admin": [5,[2]],
		"/auth": [17],
		"/(app)/crypto": [7,[2]],
		"/(app)/c/[id]": [6,[2]],
		"/error": [18],
		"/modelfiles/create": [19],
		"/prompts/create": [20],
		"/s/[id]": [21],
		"/userVerifying": [22],
		"/(app)/workspace": [8,[2,3]],
		"/(app)/workspace/documents": [9,[2,3]],
		"/(app)/workspace/modelfiles": [10,[2,3]],
		"/(app)/workspace/modelfiles/create": [11,[2,3]],
		"/(app)/workspace/modelfiles/edit": [12,[2,3]],
		"/(app)/workspace/playground": [13,[2,3]],
		"/(app)/workspace/prompts": [14,[2,3]],
		"/(app)/workspace/prompts/create": [15,[2,3]],
		"/(app)/workspace/prompts/edit": [16,[2,3]]
	};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};

export { default as root } from '../root.svelte';