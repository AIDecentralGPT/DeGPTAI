import { v4 as uuidv4 } from 'uuid';
import sha256 from 'js-sha256';
import { getOllamaModels } from '$lib/apis/ollama';
import { getOpenAIModels } from '$lib/apis/openai';
import { getLiteLLMModels } from '$lib/apis/litellm';
import { getDeModels } from '$lib/apis/de';

export const getModels = async (token: string) => {
	let models = await Promise.all([
		// getOllamaModels(token).catch((error) => {
		// 	console.log(error);
		// 	return null;
		// }),
		// getOpenAIModels(token).catch((error) => {
		// 	console.log(error);
		// 	return null;
		// }),
		// getLiteLLMModels(token).catch((error) => {
		// 	console.log(error);
		// 	return null;
		// })
		getDeModels(token).catch((error) => {
			console.log(error);
			return null;
		}),

	]);

	console.log("models", models);


	models = models.filter((models) => models).reduce((a, e, i, arr) => a.concat(e), []);



	return models;
};

//////////////////////////
// Helper functions
//////////////////////////

export const sanitizeResponseContent = (content: string) => {
	return content
		.replace(/<\|[a-z]*$/, '')
		.replace(/<\|[a-z]+\|$/, '')
		.replace(/<$/, '')
		.replaceAll(/<\|[a-z]+\|>/g, ' ')
		.replaceAll('<', '&lt;')
		.trim();
};

export const revertSanitizedResponseContent = (content: string) => {
	return content.replaceAll('&lt;', '<');
};

export const capitalizeFirstLetter = (string) => {
	return string.charAt(0).toUpperCase() + string.slice(1);
};

export const splitStream = (splitOn) => {
	let buffer = '';
	return new TransformStream({
		transform(chunk, controller) {
			buffer += chunk;
			const parts = buffer.split(splitOn);
			parts.slice(0, -1).forEach((part) => controller.enqueue(part));
			buffer = parts[parts.length - 1];
		},
		flush(controller) {
			if (buffer) controller.enqueue(buffer);
		}
	});
};

export const convertMessagesToHistory = (messages) => {
	const history = {
		messages: {},
		currentId: null
	};

	let parentMessageId = null;
	let messageId = null;

	for (const message of messages) {
		messageId = uuidv4();

		if (parentMessageId !== null) {
			history.messages[parentMessageId].childrenIds = [
				...history.messages[parentMessageId].childrenIds,
				messageId
			];
		}

		history.messages[messageId] = {
			...message,
			id: messageId,
			parentId: parentMessageId,
			childrenIds: []
		};

		parentMessageId = messageId;
	}

	history.currentId = messageId;
	return history;
};

export const getGravatarURL = (email) => {
	// Trim leading and trailing whitespace from
	// an email address and force all characters
	// to lower case
	const address = String(email).trim().toLowerCase();

	// Create a SHA256 hash of the final string
	const hash = sha256(address);

	// Grab the actual image URL
	return `https://www.gravatar.com/avatar/${hash}`;
};

export const canvasPixelTest = () => {
	// Test a 1x1 pixel to potentially identify browser/plugin fingerprint blocking or spoofing
	// Inspiration: https://github.com/kkapsner/CanvasBlocker/blob/master/test/detectionTest.js
	const canvas = document.createElement('canvas');
	const ctx = canvas.getContext('2d');
	canvas.height = 1;
	canvas.width = 1;
	const imageData = new ImageData(canvas.width, canvas.height);
	const pixelValues = imageData.data;

	// Generate RGB test data
	for (let i = 0; i < imageData.data.length; i += 1) {
		if (i % 4 !== 3) {
			pixelValues[i] = Math.floor(256 * Math.random());
		} else {
			pixelValues[i] = 255;
		}
	}

	ctx.putImageData(imageData, 0, 0);
	const p = ctx.getImageData(0, 0, canvas.width, canvas.height).data;

	// Read RGB data and fail if unmatched
	for (let i = 0; i < p.length; i += 1) {
		if (p[i] !== pixelValues[i]) {
			console.log(
				'canvasPixelTest: Wrong canvas pixel RGB value detected:',
				p[i],
				'at:',
				i,
				'expected:',
				pixelValues[i]
			);
			console.log('canvasPixelTest: Canvas blocking or spoofing is likely');
			return false;
		}
	}

	return true;
};

export const generateInitialsImage = (name) => {
	const canvas = document.createElement('canvas');
	const ctx = canvas.getContext('2d');
	canvas.width = 100;
	canvas.height = 100;

	if (!canvasPixelTest()) {
		console.log(
			'generateInitialsImage: failed pixel test, fingerprint evasion is likely. Using default image.'
		);
		return '/user.png';
	}

	ctx.fillStyle = '#b78e55';
	ctx.fillRect(0, 0, canvas.width, canvas.height);

	ctx.fillStyle = '#FFFFFF';
	ctx.font = '40px Helvetica';
	ctx.textAlign = 'center';
	ctx.textBaseline = 'middle';

	const sanitizedName = name.trim();

	let initials = "";
	if (sanitizedName.length > 12) {
		initials = sanitizedName.substring(2, 4);
	} else {
		if (sanitizedName.length < 3) {
			initials = sanitizedName;
		} else {
			initials = sanitizedName.substring(0, 2);
		}
	}
	ctx.fillText(initials.toUpperCase(), canvas.width / 2, canvas.height / 2);

	return canvas.toDataURL();
};

export const copyToClipboard = async (text, isMarkdown) => {
	let result = false;
	const textArea = document.createElement('textarea');
	// 去掉 markdown 格式
	if (isMarkdown) {
		// 去掉-或* 即 li 标签
		text = text.replace(/^[ ]*[-*] /gm, "");
		// 去掉* 即 strong标签
		text = text.replace(/\*\*(.*?)\*\*/g, '$1');
		// 去掉# 即 h标签
		text = text.replace(/^#{1,6}\s/gm, '');
	}
	textArea.value = text;

	// Avoid scrolling to bottom
	textArea.style.top = '0';
	textArea.style.left = '0';
	textArea.style.position = 'fixed';

	document.body.appendChild(textArea);
	textArea.focus();
	textArea.select();

	try {
		const successful = document.execCommand('copy');
		const msg = successful ? 'successful' : 'unsuccessful';
		console.log('Fallback: Copying text command was ' + msg);
		result = true;
	} catch (err) {
		console.error('Fallback: Oops, unable to copy', err);
	}

	document.body.removeChild(textArea);
	return result;
};

export const compareVersion = (latest, current) => {
	return current === '0.0.0'
		? false
		: current.localeCompare(latest, undefined, {
			numeric: true,
			sensitivity: 'case',
			caseFirst: 'upper'
		}) < 0;
};

export const findWordIndices = (text) => {
	const regex = /\[([^\]]+)\]/g;
	const matches = [];
	let match;

	while ((match = regex.exec(text)) !== null) {
		matches.push({
			word: match[1],
			startIndex: match.index,
			endIndex: regex.lastIndex - 1
		});
	}

	return matches;
};

export const removeFirstHashWord = (inputString) => {
	// Split the string into an array of words
	const words = inputString.split(' ');

	// Find the index of the first word that starts with #
	const index = words.findIndex((word) => word.startsWith('#'));

	// Remove the first word with #
	if (index !== -1) {
		words.splice(index, 1);
	}

	// Join the remaining words back into a string
	const resultString = words.join(' ');

	return resultString;
};

export const transformFileName = (fileName) => {
	// Convert to lowercase
	const lowerCaseFileName = fileName.toLowerCase();

	// Remove special characters using regular expression
	const sanitizedFileName = lowerCaseFileName.replace(/[^\w\s]/g, '');

	// Replace spaces with dashes
	const finalFileName = sanitizedFileName.replace(/\s+/g, '-');

	return finalFileName;
};

export const calculateSHA256 = async (file) => {
	// Create a FileReader to read the file asynchronously
	const reader = new FileReader();

	// Define a promise to handle the file reading
	const readFile = new Promise((resolve, reject) => {
		reader.onload = () => resolve(reader.result);
		reader.onerror = reject;
	});

	// Read the file as an ArrayBuffer
	reader.readAsArrayBuffer(file);

	try {
		// Wait for the FileReader to finish reading the file
		const buffer = await readFile;

		// Convert the ArrayBuffer to a Uint8Array
		const uint8Array = new Uint8Array(buffer);

		// Calculate the SHA-256 hash using Web Crypto API
		const hashBuffer = await crypto.subtle.digest('SHA-256', uint8Array);

		// Convert the hash to a hexadecimal string
		const hashArray = Array.from(new Uint8Array(hashBuffer));
		const hashHex = hashArray.map((byte) => byte.toString(16).padStart(2, '0')).join('');

		return `${hashHex}`;
	} catch (error) {
		console.error('Error calculating SHA-256 hash:', error);
		throw error;
	}
};

export const getImportOrigin = (_chats) => {
	// Check what external service chat imports are from
	if ('mapping' in _chats[0]) {
		return 'openai';
	}
	return 'webui';
};

const convertOpenAIMessages = (convo) => {
	// Parse OpenAI chat messages and create chat dictionary for creating new chats
	const mapping = convo['mapping'];
	const messages = [];
	let currentId = '';
	let lastId = null;

	for (let message_id in mapping) {
		const message = mapping[message_id];
		currentId = message_id;
		try {
			if (
				messages.length == 0 &&
				(message['message'] == null ||
					(message['message']['content']['parts']?.[0] == '' &&
						message['message']['content']['text'] == null))
			) {
				// Skip chat messages with no content
				continue;
			} else {
				const new_chat = {
					id: message_id,
					parentId: lastId,
					childrenIds: message['children'] || [],
					role: message['message']?.['author']?.['role'] !== 'user' ? 'assistant' : 'user',
					content:
						message['message']?.['content']?.['parts']?.[0] ||
						message['message']?.['content']?.['text'] ||
						'',
					model: 'gpt-3.5-turbo',
					done: true,
					context: null
				};
				messages.push(new_chat);
				lastId = currentId;
			}
		} catch (error) {
			console.log('Error with', message, '\nError:', error);
		}
	}

	let history = {};
	messages.forEach((obj) => (history[obj.id] = obj));

	const chat = {
		history: {
			currentId: currentId,
			messages: history // Need to convert this to not a list and instead a json object
		},
		models: ['gpt-3.5-turbo'],
		messages: messages,
		options: {},
		timestamp: convo['create_time'],
		title: convo['title'] ?? 'New Chat'
	};
	return chat;
};

const validateChat = (chat) => {
	// Because ChatGPT sometimes has features we can't use like DALL-E or migh have corrupted messages, need to validate
	const messages = chat.messages;

	// Check if messages array is empty
	if (messages.length === 0) {
		return false;
	}

	// Last message's children should be an empty array
	const lastMessage = messages[messages.length - 1];
	if (lastMessage.childrenIds.length !== 0) {
		return false;
	}

	// First message's parent should be null
	const firstMessage = messages[0];
	if (firstMessage.parentId !== null) {
		return false;
	}

	// Every message's content should be a string
	for (let message of messages) {
		if (typeof message.content !== 'string') {
			return false;
		}
	}

	return true;
};

export const convertOpenAIChats = (_chats) => {
	// Create a list of dictionaries with each conversation from import
	const chats = [];
	let failed = 0;
	for (let convo of _chats) {
		const chat = convertOpenAIMessages(convo);

		if (validateChat(chat)) {
			chats.push({
				id: convo['id'],
				user_id: '',
				title: convo['title'],
				chat: chat,
				timestamp: convo['timestamp']
			});
		} else {
			failed++;
		}
	}
	console.log(failed, 'Conversations could not be imported');
	return chats;
};

export const isValidHttpUrl = (string) => {
	let url;

	try {
		url = new URL(string);
	} catch (_) {
		return false;
	}

	return url.protocol === 'http:' || url.protocol === 'https:';
};

export const removeEmojis = (str) => {
	// Regular expression to match emojis
	const emojiRegex = /[\uD800-\uDBFF][\uDC00-\uDFFF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDE4F]/g;

	// Replace emojis with an empty string
	return str.replace(emojiRegex, '');
};

export const extractSentences = (text) => {
	// Split the paragraph into sentences based on common punctuation marks
	const sentences = text.split(/(?<=[.!?])/);

	return sentences
		.map((sentence) => removeEmojis(sentence.trim()))
		.filter((sentence) => sentence !== '');
};

export const blobToFile = (blob, fileName) => {
	// Create a new File object from the Blob
	const file = new File([blob], fileName, { type: blob.type });
	return file;
};

/**
 * This function is used to replace placeholders in a template string with the provided prompt.
 * The placeholders can be in the following formats:
 * - `{{prompt}}`: This will be replaced with the entire prompt.
 * - `{{prompt:start:<length>}}`: This will be replaced with the first <length> characters of the prompt.
 * - `{{prompt:end:<length>}}`: This will be replaced with the last <length> characters of the prompt.
 * - `{{prompt:middletruncate:<length>}}`: This will be replaced with the prompt truncated to <length> characters, with '...' in the middle.
 *
 * @param {string} template - The template string containing placeholders.
 * @param {string} prompt - The string to replace the placeholders with.
 * @returns {string} The template string with the placeholders replaced by the prompt.
 */
export const promptTemplate = (template: string, prompt: string): string => {
	return template.replace(
		/{{prompt}}|{{prompt:start:(\d+)}}|{{prompt:end:(\d+)}}|{{prompt:middletruncate:(\d+)}}/g,
		(match, startLength, endLength, middleLength) => {
			if (match === '{{prompt}}') {
				return prompt;
			} else if (match.startsWith('{{prompt:start:')) {
				return prompt.substring(0, startLength);
			} else if (match.startsWith('{{prompt:end:')) {
				return prompt.slice(-endLength);
			} else if (match.startsWith('{{prompt:middletruncate:')) {
				if (prompt.length <= middleLength) {
					return prompt;
				}
				const start = prompt.slice(0, Math.ceil(middleLength / 2));
				const end = prompt.slice(-Math.floor(middleLength / 2));
				return `${start}...${end}`;
			}
			return '';
		}
	);
};

export const approximateToHumanReadable = (nanoseconds: number) => {
	const seconds = Math.floor((nanoseconds / 1e9) % 60);
	const minutes = Math.floor((nanoseconds / 6e10) % 60);
	const hours = Math.floor((nanoseconds / 3.6e12) % 24);

	const results: string[] = [];

	if (seconds >= 0) {
		results.push(`${seconds}s`);
	}

	if (minutes > 0) {
		results.push(`${minutes}m`);
	}

	if (hours > 0) {
		results.push(`${hours}h`);
	}

	return results.reverse().join(' ');
};

export const getTimeRange = (timestamp) => {
	const now = new Date();
	const date = new Date(timestamp * 1000); // Convert Unix timestamp to milliseconds

	// Calculate the difference in milliseconds
	const diffTime = now.getTime() - date.getTime();
	const diffDays = diffTime / (1000 * 3600 * 24);

	const nowDate = now.getDate();
	const nowMonth = now.getMonth();
	const nowYear = now.getFullYear();

	const dateDate = date.getDate();
	const dateMonth = date.getMonth();
	const dateYear = date.getFullYear();

	if (nowYear === dateYear && nowMonth === dateMonth && nowDate === dateDate) {
		return 'Today';
	} else if (nowYear === dateYear && nowMonth === dateMonth && nowDate - dateDate === 1) {
		return 'Yesterday';
	} else if (diffDays <= 7) {
		return 'Previous 7 days';
	} else if (diffDays <= 30) {
		return 'Previous 30 days';
	} else if (nowYear === dateYear) {
		return date.toLocaleString('default', { month: 'long' });
	} else {
		return date.getFullYear().toString();
	}
};

// 封装获取可见性状态属性名的函数，提高代码复用性
function getVisibilityStateProperty(): string {
	if (typeof document.hidden!== 'undefined') {
			return 'visibilityState';
	} else if (typeof document.msHidden!== 'undefined') {
			return 'msVisibilityState';
	} else if (typeof document.webkitHidden!== 'undefined') {
			return 'webkitVisibilityState';
	}
	return 'visibilityState'; // 默认返回标准属性名
}

// 封装判断页面是否可见的函数，使代码逻辑更清晰
function isPageCurrentlyVisible(): boolean {
	const visibilityStateProperty = getVisibilityStateProperty();
	return (document[visibilityStateProperty]?? 'visible') === 'visible';
}

const timeoutIdMap = new Map();
export const addTextSlowly = async (updateTarget, target, text, model) => {
	// 检查页面当前可见状态
	const isVisible = isPageCurrentlyVisible();
	if (isVisible) {
		console.log('页面切换到前台，变为可见' + model);
	} else {
		console.log('页面切换到后台或切换了选项卡，变为不可见' + model);
	}
	for (const char of text) {
		target += char;
		// 这里可以设置一个适当的延迟来模拟逐字符显示(判断是否前台显示)
		// await new Promise(resolve => setTimeout(resolve, 12.5)); // 40token/1s
		if (isVisible) {
			await new Promise<void>((resolve) => {
				const timeoutId = setTimeout(() => {
					resolve();
					timeoutIdMap.delete(model); // 定时完成后移除ID
				}, 12.5);
				timeoutIdMap.set(model, timeoutId);
			});
			updateTarget(target)
		} else {
			if (timeoutIdMap.has(model)) {
				clearTimeout(timeoutIdMap.get(model));
				timeoutIdMap.delete(model);
			}
		}
	}
	// 更新界面或进行其他操作
	return target;
}


export const checkUniapp = () => {
	// 在uni-app环境中，判断是否是打包的app
	try {
		if (typeof plus !== "undefined") {
			return true;
		} else {
			return false;
		}
	} catch(e) {
		return false;
	}
}

export const checkPlatform = () => {
	// 在uni-app环境中，判断是否是打包的app
	try {
		const userAgent = navigator.userAgent.toLowerCase();
		if (userAgent.indexOf('iphone') !== -1 || userAgent.indexOf('ipad') !== -1 || userAgent.indexOf('ipod') !== -1) {
			return 'ios';
		} else if (userAgent.indexOf('android') !== -1) {
			return 'android';
		} else {
			return 'other';
		}
	} catch(e) {
		return 'other';
	}
}


