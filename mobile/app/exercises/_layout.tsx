import { Stack } from 'expo-router';
import { stackScreenOptionsWithBack } from '../../src/navigation/stackScreenOptions';
import { strings } from '../../src/i18n/he';

export default function ExercisesLayout() {
  return (
    <Stack screenOptions={stackScreenOptionsWithBack()}>
      <Stack.Screen
        name="index"
        options={{ title: strings.exercises.catalogTitle }}
      />
      <Stack.Screen name="catalog" options={{ headerShown: false }} />
      <Stack.Screen name="mine" options={{ headerShown: false }} />
    </Stack>
  );
}
