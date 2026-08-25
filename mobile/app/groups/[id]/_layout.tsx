import { Stack } from 'expo-router';
import { strings } from '../../../src/i18n/he';
import { stackScreenOptionsWithBack } from '../../../src/navigation/stackScreenOptions';

export default function GroupDetailLayout() {
  return (
    <Stack screenOptions={stackScreenOptionsWithBack()}>
      <Stack.Screen name="index" options={{ title: strings.groups.groupHub }} />
      <Stack.Screen name="settings" options={{ title: strings.common.settings }} />
      <Stack.Screen name="history" options={{ title: strings.lessons.lessonHistory }} />
      <Stack.Screen name="progress" options={{ title: strings.progress.progress }} />
      <Stack.Screen name="lessons" options={{ headerShown: false }} />
    </Stack>
  );
}
