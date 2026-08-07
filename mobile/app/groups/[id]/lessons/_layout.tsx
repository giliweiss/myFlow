import { Stack } from 'expo-router';

export default function LessonsLayout() {
  return (
    <Stack>
      <Stack.Screen name="new" options={{ title: 'Create Lesson' }} />
      <Stack.Screen name="[lessonId]" options={{ title: 'Lesson' }} />
    </Stack>
  );
}
