import { Stack } from 'expo-router';
import { stackScreenOptionsWithBack } from '../../../src/navigation/stackScreenOptions';
import { strings } from '../../../src/i18n/he';

export default function MineExercisesLayout() {
  return (
    <Stack screenOptions={stackScreenOptionsWithBack()}>
      <Stack.Screen
        name="new"
        options={{ title: strings.exercises.newExercise }}
      />
      <Stack.Screen
        name="[id]"
        options={{ title: strings.exercises.editExercise }}
      />
    </Stack>
  );
}
