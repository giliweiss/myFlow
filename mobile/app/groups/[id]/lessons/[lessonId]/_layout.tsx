import { Stack } from 'expo-router';
import { strings } from '../../../../../src/i18n/he';
import { stackScreenOptionsWithBack } from '../../../../../src/navigation/stackScreenOptions';

export default function LessonDetailLayout() {
  return (
    <Stack screenOptions={stackScreenOptionsWithBack()}>
      <Stack.Screen name="index" options={{ title: strings.lessons.lessonDetail }} />
      <Stack.Screen name="review" options={{ title: strings.lessons.addReview }} />
    </Stack>
  );
}
