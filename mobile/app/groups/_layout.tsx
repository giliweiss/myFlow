import { Stack } from 'expo-router';
import { strings } from '../../src/i18n/he';
import { stackScreenOptionsWithBack } from '../../src/navigation/stackScreenOptions';

export default function GroupsLayout() {
  return (
    <Stack screenOptions={stackScreenOptionsWithBack()}>
      <Stack.Screen name="new" options={{ title: strings.groups.newGroup }} />
      <Stack.Screen name="[id]" options={{ headerShown: false }} />
    </Stack>
  );
}
