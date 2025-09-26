import { registerPlugin } from '@capacitor/core';

import type { AliSpeechPlugin } from './definitions';

const AliSpeech = registerPlugin<AliSpeechPlugin>('AliSpeech');

export * from './definitions';
export { AliSpeech };