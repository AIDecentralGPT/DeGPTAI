// 全局变量
let audioContext: any = null;
let audioWorkletNode: any = null;
let isPlaying = false;
let pcmQueue: any = []; // 用于缓存待播放的PCM数据
const PCM_CONFIG = {
  sampleRate: 12000,
	channels: 2,
	bitDepth: 16,
};

// 初始化音频上下文和Worklet
export const initAudioContext = async () => {
  if (audioContext) return;
  
  audioContext = new AudioContext();
  
  // 加载并注册音频处理器
  await audioContext.audioWorklet.addModule('pcm-processor.js');
  
  // 创建Worklet节点
  audioWorkletNode = new AudioWorkletNode(audioContext, 'pcm-processor');
  
  // 连接到扬声器
  audioWorkletNode.connect(audioContext.destination);
  
  // 监听处理器发送的需要更多数据的消息
  audioWorkletNode.port.onmessage = (e) => {
    if (e.data.type === 'need-more-data') {
      // 可以在这里请求更多数据
      console.log('需要更多PCM数据');
    }
  };
};

// 解码Base64到PCM并添加到播放队列
export const updatePCMData = (newBase64: string) => {
  if (!audioContext || !audioWorkletNode) {
    console.error('音频上下文未初始化');
    return;
  }
  
  const pcmData = decodeBase64ToPCM(newBase64);
  if (pcmData) {
    // 将PCM数据添加到队列
    pcmQueue.push(...pcmData);
    
    // 如果尚未播放，开始播放
    if (!isPlaying) {
      startPlayback();
    }
  }
};

// 开始播放
export const startPlayback = () => {
  if (isPlaying || !audioContext) return;
  
  // 如果音频上下文处于暂停状态，恢复它
  if (audioContext.state === 'suspended') {
    audioContext.resume();
  }
  
  isPlaying = true;
  
  // 启动数据处理循环
  processPCMQueue();
};

// 处理PCM队列数据
export const processPCMQueue = () => {
  if (!isPlaying || pcmQueue.length === 0) return;
  
  // 向音频处理器发送数据
  audioWorkletNode.port.postMessage({
    type: 'new-data',
    data: pcmQueue.splice(0, 4096) // 每次发送4096个样本
  });
  // 继续处理队列
  requestAnimationFrame(processPCMQueue);
};

// 停止播放
export const stopPlayback = () => {
  isPlaying = false;
  pcmQueue = [];
};

// Base64解码为PCM数据（假设16位PCM）
function decodeBase64ToPCM(base64: string) {
  try {
    const binaryString = atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    
    // 转换为16位有符号整数
    const pcmData = new Int16Array(bytes.buffer);
    return pcmData;
  } catch (e) {
    console.error('解码PCM数据失败:', e);
    return null;
  }
}
