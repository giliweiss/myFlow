import { Stack } from 'expo-router';
import { stackScreenOptionsWithBack } from '../../../src/navigation/stackScreenOptions';
import { strings } from '../../../src/i18n/he';

export default function CatalogLayout() {
  return (
    <Stack screenOptions={stackScreenOptionsWithBack()}>
      <Stack.Screen
        name="[id]"
        options={{ title: strings.exercises.exerciseDetail }}
      />
    </Stack>
  );
}
