import { Stack } from 'expo-router';

export default function LessonDetailLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Lesson Detail' }} />
      <Stack.Screen name="review" options={{ title: 'Add Review' }} />
    </Stack>
  );
}
