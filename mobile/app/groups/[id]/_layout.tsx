import { Stack } from 'expo-router';

export default function GroupDetailLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Group Detail' }} />
      <Stack.Screen name="settings" options={{ title: 'Group Settings' }} />
      <Stack.Screen name="history" options={{ title: 'Lesson History' }} />
      <Stack.Screen name="progress" options={{ title: 'Progress' }} />
      <Stack.Screen name="lessons" options={{ headerShown: false }} />
    </Stack>
  );
}
