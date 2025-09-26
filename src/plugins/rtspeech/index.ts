import { registerPlugin } from '@capacitor/core';

import type { RealTimeSpeechPlugin } from './definitions';

const RealTimeSpeech = registerPlugin<RealTimeSpeechPlugin>('RealTimeSpeech');

export * from './definitions';
export { RealTimeSpeech };