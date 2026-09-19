import type { NativeStackNavigationOptions } from 'expo-router/build/react-navigation/native-stack/types';
import { theme } from '../theme';
import { HeaderBackButton } from './HeaderBackButton';

const baseStackScreenOptions: NativeStackNavigationOptions = {
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
  headerTitleAlign: 'center',
};

export function stackScreenOptions(
  options: { showBack?: boolean } = {},
): NativeStackNavigationOptions {
  if (!options.showBack) {
    return baseStackScreenOptions;
  }

  return {
    ...baseStackScreenOptions,
    headerBackVisible: false,
    headerLeft: () => <HeaderBackButton />,
  };
}

export function stackScreenOptionsWithBack(): NativeStackNavigationOptions {
  return stackScreenOptions({ showBack: true });
}
