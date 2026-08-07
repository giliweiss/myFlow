import { Stack } from 'expo-router';

export default function GroupsLayout() {
  return (
    <Stack>
      <Stack.Screen name="new" options={{ title: 'New Group' }} />
      <Stack.Screen name="[id]" options={{ title: 'Group' }} />
    </Stack>
  );
}
