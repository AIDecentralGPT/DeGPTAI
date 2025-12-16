import { registerPlugin } from '@capacitor/core';

import type { VoicePlugin } from './definitions';

const VoiceRecord = registerPlugin<VoicePlugin>('VoiceRecord');

export * from './definitions';
export { VoiceRecord };