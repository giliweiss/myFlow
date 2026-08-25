import Constants from 'expo-constants';
import { Platform } from 'react-native';

function getMetroHost(): string | null {
  const expoGoConfig = Constants.expoGoConfig as { debuggerHost?: string } | null;
  if (expoGoConfig?.debuggerHost) {
    return expoGoConfig.debuggerHost.split(':')[0];
  }

  const manifest = Constants.manifest as { debuggerHost?: string } | null;
  if (manifest?.debuggerHost) {
    return manifest.debuggerHost.split(':')[0];
  }

  return null;
}

export function getApiUrl(): string {
  if (Platform.OS === 'web') {
    return process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';
  }

  const metroHost = getMetroHost();
  if (__DEV__ && metroHost) {
    return `http://${metroHost}:8000`;
  }

  return process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';
}
