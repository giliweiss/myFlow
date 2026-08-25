import { Tabs } from 'expo-router';
import { theme } from '../../src/theme';
import { strings } from '../../src/i18n/he';

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        headerStyle: {
          backgroundColor: theme.colors.surface,
        },
        headerTintColor: theme.colors.primary,
        headerTitleStyle: {
          fontFamily: 'Rubik_600SemiBold',
          fontSize: 18,
          color: theme.colors.textPrimary,
        },
        tabBarStyle: {
          display: 'none',
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: strings.groups.myGroups,
          headerShown: true,
          headerTitleAlign: 'center',
        }}
      />
    </Tabs>
  );
}
