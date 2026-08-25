import { Stack } from 'expo-router';
import { strings } from '../../../../../src/i18n/he';
import { stackScreenOptionsWithBack } from '../../../../../src/navigation/stackScreenOptions';

export default function NewLessonLayout() {
  return (
    <Stack screenOptions={stackScreenOptionsWithBack()}>
      <Stack.Screen
        name="index"
        options={{ title: strings.lessons.buildLesson }}
      />
      <Stack.Screen
        name="manual"
        options={{ title: strings.lessons.buildModeManual }}
      />
      <Stack.Screen
        name="ai"
        options={{ title: strings.lessons.buildModeAi }}
      />
    </Stack>
  );
}
