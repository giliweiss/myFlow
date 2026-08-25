import { Stack } from 'expo-router';
import { theme } from '../../src/theme';
import { strings } from '../../src/i18n/he';

export default function GroupsLayout() {
  const screenOptions = {
    headerStyle: {
      backgroundColor: theme.colors.surface,
    },
    headerTintColor: theme.colors.primary,
    headerTitleStyle: {
      fontFamily: 'Rubik_600SemiBold',
      fontSize: 18,
      color: theme.colors.textPrimary,
    },
    contentStyle: {
      backgroundColor: theme.colors.background,
    },
  };

  return (
    <Stack screenOptions={screenOptions}>
      <Stack.Screen name="new" options={{ title: strings.groups.newGroup }} />
      <Stack.Screen name="[id]" options={{ headerShown: false }} />
    </Stack>
  );
}
