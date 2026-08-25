import { Stack } from 'expo-router';
import { stackScreenOptionsWithBack } from '../../../../src/navigation/stackScreenOptions';

export default function LessonsLayout() {
  return (
    <Stack screenOptions={stackScreenOptionsWithBack()}>
      <Stack.Screen name="new" options={{ headerShown: false }} />
      <Stack.Screen name="[lessonId]" options={{ headerShown: false }} />
    </Stack>
  );
}
